import os
import pandas as pd
import networkx as nx
import community.community_louvain as louvain
from pyvis.network import Network
import re
from collections import Counter
import csv

# 1. Configuration
DATA_FILES = [
    ("data/cleaned/reddit_political_cleaned.csv", ["full_text"]),
    ("data/cleaned/youtube_cleaned.csv", ["text"]),
    ("data/shahana_bano_datasets/twitter/twitter_dataset.csv", ["Text"]),
    ("data/shahana_bano_datasets/instagram/instagram_dataset.csv", ["childCommentText", "parentText"]),
    ("data/shahana_bano_datasets/tiktok/tiktok_dataset.csv", ["text"])
]
WINDOW_SIZE = 20
OUTPUT_DIR = "deliverables"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "hashtag_centrality_stats.csv")
OUTPUT_HTML = os.path.join(OUTPUT_DIR, "hashtag_network.html")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Liste blanche de domaines Politique / Actualité / Social (correspondances exactes ou sous-chaînes)
DOMAIN_KEYWORDS = [
    "politi", "bernie", "trump", "biden", "elect", "vote", "democrat", "republic", 
    "gaza", "israel", "palest", "war", "peace", "bbc", "news", "parliament", "congress",
    "conservat", "liberal", "protest", "fascis", "nazi", "govern", "humanrights",
    "rightwing", "leftwing", "brexit", "president", "policy", 
    "court", "justice", "strike", "union", "feelthebern", "releasethetranscripts",
    "international", "arrest", "blacklivesmatter", "maga", "medicareforall",
    "deletethedon", "draintheswamp", "releasethememo", "sotu", "resistcapitalism",
    "pride", "equalityact", "khive", "notmeus", "capitalism", "socialism", "climate"
]

def text_to_tokens(text):
    """Tokeniser le texte tout en préservant les hashtags, en gardant UNIQUEMENT les hashtags liés au domaine."""
    if not isinstance(text, str):
        return []
    
    tokens = re.findall(r"#\w+|\w+", text.lower())
    valid_tokens = []
    
    for t in tokens:
        if t.startswith("#") and len(t) > 1:
            hashtag = t[1:]
            # Vérifier si le hashtag appartient au domaine politique
            if any(keyword in hashtag for keyword in DOMAIN_KEYWORDS):
                # Filtre extra strict pour éviter les fausses correspondances et le bruit reddit
                if hashtag in ["makeup", "awkward", "cutebeuty", "prankwars", "ukcomedy", "uktalent", "timewarpscan", "sucuk", "suçuk", "motherinlaw", "teamusatryout", "x200b", "submissions", "echobox", "selection", "this", "all", "we", "no", "click"]:
                    continue
                valid_tokens.append(t)
        else:
            valid_tokens.append(t)
            
    return valid_tokens

def build_cooccurrence_matrix(data_files, window_size):
    """Construire une matrice de co-occurrence de hashtags au niveau du document."""
    print(f"🔍 Building co-occurrence matrix (Document level)...")
    co_occurrence = Counter()
    hashtag_counts = Counter()

    for file_path, text_cols in data_files:
        if not os.path.exists(file_path):
            print(f"⚠️ Warning: {file_path} not found. Skipping.")
            continue
        
        print(f"📊 Processing {file_path}...")
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            continue
        
        for text_col in text_cols:
            if text_col not in df.columns:
                print(f"⚠️ Column {text_col} not found in {file_path}. Skipping column.")
                continue
                
            hashtags_in_col = 0
            for doc in df[text_col].dropna():
                tokens = text_to_tokens(doc)
                
                # Obtenir les hashtags valides uniques dans ce document
                doc_hashtags = list(set([t[1:] for t in tokens if t.startswith("#") and len(t) > 1]))
                
                for h in doc_hashtags:
                    hashtag_counts[h] += 1
                    hashtags_in_col += 1
                    
                # Co-occurrence de toutes les paires dans ce document
                for i in range(len(doc_hashtags)):
                    for j in range(i + 1, len(doc_hashtags)):
                        h1, h2 = sorted([doc_hashtags[i], doc_hashtags[j]])
                        co_occurrence[(h1, h2)] += 1
                        
            print(f"   ✨ Found {hashtags_in_col} hashtags in column '{text_col}'.")
                                
    return co_occurrence, hashtag_counts

def main():
    # 2. Construire les données de co-occurrence
    co_occurrence, hashtag_counts = build_cooccurrence_matrix(DATA_FILES, WINDOW_SIZE)
    
    if not co_occurrence:
        print("❌ No hashtag co-occurrences found. Check your data or window size.")
        # Nous pouvons toujours créer un graphe avec seulement des nœuds si nécessaire, mais l'utilisateur veut des connexions.
        if not hashtag_counts:
            return

    # 3. Creation du graphe (NetworkX)
    print(f"🕸️ Creating graph with {len(co_occurrence)} unique co-occurrences...")
    G = nx.Graph()
    
    MIN_FREQUENCY = 1
    MIN_EDGE_WEIGHT = 1
    print(f"🧹 Filtering for hashtags with frequency >= {MIN_FREQUENCY} and edge weight >= {MIN_EDGE_WEIGHT}...")
    
    for (h1, h2), weight in co_occurrence.items():
        # N'ajouter une arête que si les DEUX hashtags atteignent le seuil de fréquence minimum ET que l'arête est forte
        if weight >= MIN_EDGE_WEIGHT and hashtag_counts.get(h1, 0) >= MIN_FREQUENCY and hashtag_counts.get(h2, 0) >= MIN_FREQUENCY:
            G.add_edge(h1, h2, weight=weight)
    
    print(f"✅ Graph created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    
    # Ajouter les nœuds qui pourraient avoir des hashtags mais pas de co-occurrences
    for h, count in hashtag_counts.items():
        if count >= MIN_FREQUENCY:
            if h not in G:
                G.add_node(h, size=count)
            else:
                G.nodes[h]['size'] = count

    if G.number_of_nodes() == 0:
        print("❌ Graph is empty. No hashtags found.")
        return

    # 4. Calcul des métriques de centralité
    print("📈 Calculating centrality metrics...")
    degree_cent = nx.degree_centrality(G)
    
    # Betweenness et PageRank peuvent échouer sur des graphes très petits ou déconnectés
    try:
        betweenness_cent = nx.betweenness_centrality(G, weight='weight')
    except:
        betweenness_cent = {node: 0 for node in G.nodes()}
        
    try:
        pagerank = nx.pagerank(G, weight='weight')
    except:
        pagerank = {node: 0 for node in G.nodes()}

    # 5. Détection de communautés (Louvain)
    print("🏘️ Detecting communities...")
    try:
        partition = louvain.best_partition(G, weight='weight')
    except:
        partition = {node: 0 for node in G.nodes()}
    nx.set_node_attributes(G, partition, 'group')

    # 6. Sauvegarde des statistiques en CSV
    print(f"💾 Saving centrality stats to {OUTPUT_CSV}...")
    stats_data = []
    for node in G.nodes():
        stats_data.append({
            "hashtag": node,
            "degree_centrality": degree_cent.get(node, 0),
            "betweenness_centrality": betweenness_cent.get(node, 0),
            "pagerank": pagerank.get(node, 0),
            "community": partition.get(node, 0),
            "frequency": hashtag_counts.get(node, 0)
        })
    
    stats_df = pd.DataFrame(stats_data)
    stats_df = stats_df.sort_values(by="pagerank", ascending=False)
    stats_df.to_csv(OUTPUT_CSV, index=False)

    # 7. Visualisation (Pyvis)
    print(f"🌐 Generating interactive visualization at {OUTPUT_HTML}...")
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
    
    # Configurer la physique pour une meilleure disposition
    net.force_atlas_2based(gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.08, damping=0.4, overlap=0)
    net.show_buttons(filter_=['physics'])

    for node, attrs in G.nodes(data=True):
        group = attrs.get('group', 0)
        size = attrs.get('size', 1) * 2 # Mettre à l'échelle pour la visibilité
        net.add_node(node, label=f"#{node}", title=f"Hashtag: #{node}<br>Group: {group}<br>Frequency: {attrs.get('size', 0)}", group=group, size=size)

    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, value=data['weight'], title=f"Co-occurrences: {data['weight']}")

    # Sauvegarder la visualisation
    net.save_graph(OUTPUT_HTML)
    
    print("✅ Week 4 tasks completed successfully!")

if __name__ == "__main__":
    main()
