"""
Utilities for NetworkX graph rendering with Plotly.
"""

import json
import networkx as nx
import plotly.graph_objects as go
from typing import Dict, Any
import pandas as pd
from app.config import COLORS_PALETTE, get_cluster_name


def render_network_graph(gml_path: str, layout_path: str, min_degree: int = 2) -> go.Figure:
    """
    Render NetworkX graph with Plotly WebGL.
    
    Args:
        gml_path: Path to GML file
        layout_path: Path to layout JSON file
        min_degree: Minimum node degree to display
    
    Returns:
        Plotly Figure
    """
    G = nx.read_gml(gml_path)
    with open(layout_path, "r", encoding="utf-8") as f:
        pos = json.load(f)
    
    # Filter nodes by degree
    degrees = dict(G.degree())
    core_nodes = {str(n) for n in G.nodes() if degrees.get(n, 1) >= min_degree}
    
    # Build edges
    edge_x, edge_y = [], []
    for edge in G.edges():
        u, v = str(edge[0]), str(edge[1])
        if u in pos and v in pos and u in core_nodes and v in core_nodes:
            x0, y0 = pos[u]['x'], pos[u]['y']
            x1, y1 = pos[v]['x'], pos[v]['y']
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scattergl(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='rgba(15,23,42,0.15)'),
        hoverinfo='none', mode='lines'
    )
    
    # Group nodes by community
    community_nodes: Dict[int, List[Any]] = {}
    for node in G.nodes():
        n_str = str(node)
        if n_str in pos and n_str in core_nodes:
            comm = G.nodes[node].get('community', 0)
            if comm not in community_nodes:
                community_nodes[comm] = []
            community_nodes[comm].append(node)
    
    traces = [edge_trace]
    
    for comm in sorted(community_nodes.keys()):
        comm_name = get_cluster_name(comm)
        nodes_in_comm = community_nodes[comm]
        
        c_x, c_y, c_text, c_size = [], [], [], []
        for n in nodes_in_comm:
            n_str = str(n)
            x, y = pos[n_str]['x'], pos[n_str]['y']
            c_x.append(x)
            c_y.append(y)
            deg = degrees.get(n, 1)
            
            # Format display name
            if n_str.startswith("tw_"):
                display_name = f"Twitter ({n_str[3:]})"
            elif n_str.startswith("ig_"):
                display_name = f"Instagram ({n_str[3:]})"
            elif n_str.startswith("rd_"):
                display_name = f"Reddit ({n_str[3:]})"
            elif n_str.startswith("yt_"):
                display_name = f"YouTube ({n_str[3:]})"
            else:
                display_name = n_str
            
            c_text.append(f"<b>User:</b> {display_name}<br><b>Degree:</b> {deg}<br><b>Cluster:</b> {comm_name}")
            c_size.append(min(35, max(4, deg / 1.2)))
        
        comm_color = COLORS_PALETTE[comm % len(COLORS_PALETTE)]
        
        node_trace = go.Scattergl(
            x=c_x, y=c_y,
            mode='markers',
            hoverinfo='text',
            text=c_text,
            name=comm_name,
            marker=dict(
                showscale=False,
                color=comm_color,
                size=c_size,
                line_width=0.3,
                line=dict(color='rgba(0,0,0,0.15)')
            )
        )
        traces.append(node_trace)
    
    fig = go.Figure(data=traces, layout=go.Layout(
        showlegend=True,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        plot_bgcolor='#F8FAFC',
        paper_bgcolor='#F8FAFC',
        legend=dict(
            font=dict(color="#0F172A"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ))
    
    return fig
