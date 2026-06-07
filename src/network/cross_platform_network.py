import pandas as pd
import networkx as nx
import community.community_louvain as louvain
import os

# Configuration
OUTPUT_DIR = "deliverables/week_5"
os.makedirs(OUTPUT_DIR, exist_ok=True)
METRICS_FILE = os.path.join(OUTPUT_DIR, "echo_chamber_metrics.txt")
COMBINED_GRAPH_GML = os.path.join(OUTPUT_DIR, "cross_platform_merged.gml")

def build_youtube_graph():
    print("Building YouTube interaction graph...")
    G = nx.DiGraph()
    try:
        df = pd.read_csv("data/cleaned/youtube_cleaned.csv")
        for _, row in df.dropna(subset=['author', 'video_id']).iterrows():
            u = f"yt_user_{row['author']}"
            v = f"yt_video_{row['video_id']}"
            G.add_edge(u, v, type='reply', platform='YouTube')
        print(f"   -> YouTube Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        print(f"Error loading YouTube data: {e}")
    return G

def build_reddit_graph():
    print("Building Reddit interaction graph...")
    G = nx.DiGraph()
    try:
        df = pd.read_csv("data/cleaned/reddit_political_cleaned.csv")
        for _, row in df.dropna(subset=['author', 'subreddit']).iterrows():
            u = f"rd_user_{row['author']}"
            v = f"rd_subreddit_{row['subreddit']}"
            G.add_edge(u, v, type='post', platform='Reddit')
        print(f"   -> Reddit Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    except Exception as e:
        print(f"Error loading Reddit data: {e}")
    return G

def main():
    print("Starting Week 5 Analysis: Reddit and YouTube Graph Merge & Modularity")
    
    # 1. Build graphs
    yt_graph = build_youtube_graph()
    rd_graph = build_reddit_graph()
    
    # 2. Merge graphs
    print("\nMerging graphs into a cross-platform network...")
    merged_graph = nx.compose(yt_graph, rd_graph)
    print(f"   -> Merged Graph: {merged_graph.number_of_nodes()} nodes, {merged_graph.number_of_edges()} edges")
    
    # 3. Detect echo chambers (Modularity)
    print("\nDetecting echo chambers (Modularity)...")
    undirected_G = merged_graph.to_undirected()
    
    # Remove isolated nodes (degree < 2) to filter topological noise
    low_degree = [node for node, degree in undirected_G.degree() if degree < 2]
    undirected_G.remove_nodes_from(low_degree)
    print(f"   -> Core Graph (degree >= 2): {undirected_G.number_of_nodes()} nodes, {undirected_G.number_of_edges()} edges")
    
    # Remove these nodes from the directed graph as well to keep them aligned
    nodes_to_remove = set(merged_graph.nodes()) - set(undirected_G.nodes())
    merged_graph.remove_nodes_from(nodes_to_remove)
    
    # Run Louvain clustering on the pruned undirected graph
    partition = louvain.best_partition(undirected_G)
    
    # Compute Modularity
    modularity_score = louvain.modularity(partition, undirected_G)
    print(f"   -> Louvain Modularity Score (Q): {modularity_score:.4f}")
    
    # Set communities as node attributes in the directed graph
    nx.set_node_attributes(merged_graph, partition, 'community')
    
    # 4. Save results
    print(f"\nSaving merged graph to {COMBINED_GRAPH_GML}...")
    nx.write_gml(merged_graph, COMBINED_GRAPH_GML)
    
    with open(METRICS_FILE, "w") as f:
        f.write("Week 5 - Echo Chamber & Graph Merge Metrics (Reddit & YouTube)\n")
        f.write("="*55 + "\n")
        f.write(f"Total Core Nodes: {merged_graph.number_of_nodes()}\n")
        f.write(f"Total Core Edges: {merged_graph.number_of_edges()}\n")
        f.write(f"Number of detected communities: {len(set(partition.values()))}\n")
        f.write(f"Modularity Score (Q): {modularity_score:.4f}\n")
        f.write("\nInterpretation:\n")
        f.write("- Modularity > 0.3 indicates strong community structure.\n")
        f.write("- Louvain community clustering partitions Reddit and YouTube participants into dense discussion clusters.\n")
        
    print("Week 5 tasks completed successfully.")

if __name__ == "__main__":
    main()
