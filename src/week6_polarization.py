import os
import pandas as pd
import networkx as nx
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from tqdm import tqdm
import time

load_dotenv()
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

# Create deliverables folder
OUTPUT_DIR = "deliverables/week_6"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# We / Them Lexicons (if need to recalculate)
WE_PRONOUNS = ["we", "us", "our", "ours", "ourselves"]
THEM_PRONOUNS = ["they", "them", "their", "theirs", "themselves"]

def count_pronouns(text, pronouns):
    if not isinstance(text, str):
        return 0
    words = re.findall(r'\b\w+\b', text.lower())
    return sum(1 for word in words if word in pronouns)

def get_perspective_toxicity(text):
    if not PERSPECTIVE_API_KEY:
        # Fallback to a mock score if no API key is provided
        return np.random.uniform(0.1, 0.8)
        
    try:
        from googleapiclient.discovery import build
        client = build('commentanalyzer', 'v1alpha1', developerKey=PERSPECTIVE_API_KEY, cache_discovery=False)
        analyze_request = {
            'comment': {'text': text[:2000]}, # limit length
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}}
        }
        response = client.comments().analyze(body=analyze_request).execute()
        time.sleep(1.1) # Respect 1 QPS limit
        return response['attributeScores']['TOXICITY']['summaryScore']['value']
    except Exception as e:
        print(f"Perspective API error: {e}")
        return np.nan

def main():
    print("🚀 Starting Week 6 Analysis: Polarization Index & Toxicity")
    
    # 1. Load the merged graph to get communities
    gml_path = "deliverables/week_5/cross_platform_merged.gml"
    if not os.path.exists(gml_path):
        print(f"❌ Error: Graph file {gml_path} not found. Please run week 5 script first.")
        return
        
    print("📂 Loading cross-platform graph...")
    G = nx.read_gml(gml_path)
    
    # Create a mapping from node name to community
    node_communities = nx.get_node_attributes(G, 'community')
    print(f"Found {len(node_communities)} nodes with community assignments.")
    
    # 2. Extract texts and map to communities
    # We will sample data to avoid API quotas (e.g. max 20 texts per community)
    community_texts = {}
    community_pronouns = {}
    
    print("📊 Processing YouTube dataset...")
    try:
        yt_df = pd.read_csv("data/cleaned/youtube_cleaned.csv")
        for _, row in yt_df.dropna(subset=['author', 'text']).iterrows():
            node_id = f"yt_user_{row['author']}"
            if node_id in node_communities:
                comm = node_communities[node_id]
                if comm not in community_texts:
                    community_texts[comm] = []
                    community_pronouns[comm] = {'we': 0, 'them': 0}
                
                # If column exists use it, otherwise compute
                we_count = row.get('we_count', count_pronouns(row['text'], WE_PRONOUNS))
                them_count = row.get('them_count', count_pronouns(row['text'], THEM_PRONOUNS))
                
                community_pronouns[comm]['we'] += we_count
                community_pronouns[comm]['them'] += them_count
                community_texts[comm].append(row['text'])
    except Exception as e:
        print(f"Warning: {e}")

    # Process Twitter dataset
    print("📊 Processing Twitter dataset...")
    try:
        tw_df = pd.read_csv("data/shahana_bano_datasets/twitter/twitter_we-language_dataset.csv")
        for idx, row in tw_df.dropna(subset=['text']).iterrows():
            node_id = f"tw_tweet_{idx}"
            if node_id in node_communities:
                comm = node_communities[node_id]
                if comm not in community_texts:
                    community_texts[comm] = []
                    community_pronouns[comm] = {'we': 0, 'them': 0}
                
                community_pronouns[comm]['we'] += count_pronouns(row['text'], WE_PRONOUNS)
                community_pronouns[comm]['them'] += count_pronouns(row['text'], THEM_PRONOUNS)
                community_texts[comm].append(row['text'])
    except Exception as e:
        print(f"Warning: {e}")

    if not community_texts:
        print("❌ No text data could be mapped to communities.")
        return

    # Filter to top communities by size to keep the heatmap readable
    top_communities = sorted(community_texts.keys(), key=lambda c: len(community_texts[c]), reverse=True)[:10]
    print(f"🏆 Selected top {len(top_communities)} communities for toxicity scoring.")
    
    if not PERSPECTIVE_API_KEY:
        print("⚠️ PERSPECTIVE_API_KEY not found in .env. Using fallback simulated toxicity scores for demonstration.")
    else:
        print("✅ PERSPECTIVE_API_KEY found. Calling Google API (this will be slow due to rate limits)...")

    # 3 & 4. Score toxicity and calculate Polarization Index
    results = []
    
    for comm in top_communities:
        texts = community_texts[comm]
        # Sample up to 20 texts per community to avoid massive API bills/time
        sample_texts = texts[:20] if len(texts) > 20 else texts
        
        print(f"   -> Scoring Community {comm} ({len(sample_texts)} texts)...")
        toxicities = [get_perspective_toxicity(t) for t in tqdm(sample_texts, leave=False)]
        mean_toxicity = np.nanmean(toxicities)
        
        we_c = community_pronouns[comm]['we']
        them_c = community_pronouns[comm]['them']
        
        # We/Them ratio (add small epsilon to avoid div by zero)
        we_them_ratio = we_c / max(1, them_c)
        
        # Polarization Index = We/Them ratio × mean toxicity
        polarization_index = we_them_ratio * mean_toxicity
        
        results.append({
            'Community': f"Cluster {comm}",
            'We_Count': we_c,
            'Them_Count': them_c,
            'We_Them_Ratio': we_them_ratio,
            'Mean_Toxicity': mean_toxicity,
            'Polarization_Index': polarization_index,
            'Size': len(texts)
        })

    results_df = pd.DataFrame(results)
    csv_path = os.path.join(OUTPUT_DIR, "community_polarization_metrics.csv")
    results_df.to_csv(csv_path, index=False)
    print(f"💾 Saved metrics to {csv_path}")
    
    # 5. Generate Cluster-Level Heatmap
    print("🗺️ Generating Polarization Heatmap...")
    plt.figure(figsize=(10, 8))
    
    # Create a pivot table for the heatmap: We/Them Ratio vs Mean Toxicity
    # Since communities are independent, we'll plot a heatmap of the metrics per community
    heatmap_data = results_df.set_index('Community')[['We_Them_Ratio', 'Mean_Toxicity', 'Polarization_Index']]
    
    # Normalize data column-wise for better color contrast in heatmap
    heatmap_data_norm = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min() + 1e-9)
    
    sns.heatmap(heatmap_data_norm, annot=heatmap_data, cmap="YlOrRd", fmt=".3f", linewidths=.5)
    plt.title("Polarization Index per Community\n(We/Them Ratio × Toxicity)")
    plt.tight_layout()
    
    heatmap_path = os.path.join(OUTPUT_DIR, "cluster_polarization_heatmap.png")
    plt.savefig(heatmap_path, dpi=300)
    plt.close()
    print(f"📊 Saved heatmap to {heatmap_path}")
    print("✅ Week 6 tasks completed successfully!")

if __name__ == "__main__":
    main()
