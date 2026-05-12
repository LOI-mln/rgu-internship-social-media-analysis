import pandas as pd
import networkx as nx
import community.community_louvain as louvain
import os
import re

# Configuration
OUTPUT_DIR = "deliverables/week_5"
os.makedirs(OUTPUT_DIR, exist_ok=True)
METRICS_FILE = os.path.join(OUTPUT_DIR, "echo_chamber_metrics.txt")
COMBINED_GRAPH_GML = os.path.join(OUTPUT_DIR, "cross_platform_merged.gml")

def extract_mentions(text):
    if not isinstance(text, str):
        return []
    return re.findall(r"@([a-zA-Z0-9_]+)", text)

def build_youtube_graph():
    print("📺 Building YouTube interaction graph...")
    G = nx.DiGraph()
    try:
        df = pd.read_csv("data/cleaned/youtube_cleaned.csv")
        for _, row in df.dropna(subset=['author', 'video_id']).iterrows():
            # Arête dirigée : L'auteur a répondu à la vidéo
            u = f"yt_user_{row['author']}"
            v = f"yt_video_{row['video_id']}"
            G.add_edge(u, v, type='reply')
        print(f"   -> YouTube Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        print(f"❌ Error loading YouTube data: {e}")
    return G

def build_instagram_graph():
    print("📸 Building Instagram reply graph...")
    G = nx.DiGraph()
    try:
        df = pd.read_csv("data/shahana_bano_datasets/instagram/instagram_dataset.csv")
        for _, row in df.dropna(subset=['childCommentID', 'parentID']).iterrows():
            # Arête dirigée : Le commentaire répond au commentaire parent
            u = f"ig_comment_{int(row['childCommentID'])}"
            v = f"ig_parent_{int(row['parentID'])}"
            G.add_edge(u, v, type='reply')
    except Exception as e:
        print(f"❌ Error loading Instagram data: {e}")
        
    try:
        # Traiter également le jeu de données des commentaires si nous pouvons trouver des mentions
        df2 = pd.read_csv("data/shahana_bano_datasets/instagram/instagram_comments_dataset.csv")
        for idx, row in df2.dropna(subset=['text']).iterrows():
            mentions = extract_mentions(row['text'])
            for m in mentions:
                u = f"ig_comment_idx_{idx}"
                v = f"ig_user_{m}"
                G.add_edge(u, v, type='mention')
    except Exception as e:
        pass
        
    print(f"   -> Instagram Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

def build_twitter_graph():
    print("🐦 Building Twitter mention/reply graph...")
    G = nx.DiGraph()
    try:
        df = pd.read_csv("data/shahana_bano_datasets/twitter/twitter_we-language_dataset.csv")
        for idx, row in df.dropna(subset=['text']).iterrows():
            mentions = extract_mentions(row['text'])
            for m in mentions:
                u = f"tw_tweet_{idx}"
                v = f"tw_user_{m}"
                G.add_edge(u, v, type='mention')
        print(f"   -> Twitter Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        print(f"❌ Error loading Twitter data: {e}")
    return G

def main():
    print("🚀 Starting Week 5 Analysis: Reply/Reshare Graphs & Modularity")
    
    # 1. Construire les graphes dirigés individuels
    yt_graph = build_youtube_graph()
    ig_graph = build_instagram_graph()
    tw_graph = build_twitter_graph()
    
    # 2. Fusion des graphes multiplateformes
    print("\n🔗 Merging graphs into a cross-platform network...")
    merged_graph = nx.compose_all([yt_graph, ig_graph, tw_graph])
    print(f"   -> Merged Graph: {merged_graph.number_of_nodes()} nodes, {merged_graph.number_of_edges()} edges")
    
    # 3. Détection des chambres d'écho (Modularité)
    print("\n🔍 Detecting echo chambers (Modularity)...")
    # La modularité est généralement calculée sur des graphes non dirigés
    undirected_G = merged_graph.to_undirected()
    
    # Supprimer les nœuds isolés pour une meilleure détection des communautés
    undirected_G.remove_nodes_from(list(nx.isolates(undirected_G)))
    
    # Exécuter l'algorithme de Louvain
    partition = louvain.best_partition(undirected_G)
    
    # Calculer la modularité
    modularity_score = louvain.modularity(partition, undirected_G)
    print(f"   -> Modularity Score: {modularity_score:.4f}")
    
    # Ajouter les communautés au graphe dirigé
    nx.set_node_attributes(merged_graph, partition, 'community')
    
    # 4. Sauvegarder les résultats
    print(f"\n💾 Saving merged graph to {COMBINED_GRAPH_GML} (can be opened in Gephi)")
    nx.write_gml(merged_graph, COMBINED_GRAPH_GML)
    
    with open(METRICS_FILE, "w") as f:
        f.write("Week 5 - Echo Chamber & Graph Merge Metrics\n")
        f.write("="*45 + "\n")
        f.write(f"Total Nodes (Cross-platform): {merged_graph.number_of_nodes()}\n")
        f.write(f"Total Edges (Replies/Mentions): {merged_graph.number_of_edges()}\n")
        f.write(f"Number of detected communities: {len(set(partition.values()))}\n")
        f.write(f"Modularity Score: {modularity_score:.4f}\n")
        f.write("\nInterpretation:\n")
        f.write("- Modularity > 0.3 indicates strong community structure (potential echo chambers).\n")
        f.write("- Directed edges represent the flow of replies/mentions across users and content.\n")
        
    print("✅ Week 5 tasks completed successfully!")

if __name__ == "__main__":
    main()
