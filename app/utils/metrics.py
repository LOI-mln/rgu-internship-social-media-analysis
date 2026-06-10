"""
Polarization and engagement metrics calculation.
"""

import pandas as pd
import networkx as nx
from typing import Dict, List


def calculate_platform_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate comparative metrics by platform.
    
    Args:
        df: DataFrame with 'platform', 'we_count', 'them_count', 'text' columns
    
    Returns:
        DataFrame of aggregated metrics by platform
    """
    metrics = []
    
    for platform in df['platform'].unique():
        platform_df = df[df['platform'] == platform]
        
        we_total = platform_df['we_count'].sum()
        them_total = platform_df['them_count'].sum()
        ratio = we_total / them_total if them_total > 0 else 1.0
        
        avg_words = platform_df['text'].astype(str).apply(lambda x: len(x.split())).mean()
        
        metrics.append({
            'Platform': platform,
            'We_Them_Ratio': ratio,
            'Topic_Density': avg_words
        })
    
    return pd.DataFrame(metrics)


def get_community_sizes(graph: nx.Graph) -> Dict[int, int]:
    """
    Get community size distribution.
    
    Args:
        graph: NetworkX graph with 'community' attribute on nodes
    
    Returns:
        Dict with {community_id: node_count}
    """
    comm_sizes = {}
    for node in graph.nodes():
        comm = graph.nodes[node].get('community', 0)
        comm_sizes[comm] = comm_sizes.get(comm, 0) + 1
    return comm_sizes
