"""
Page 2: Echo Chambers & Polarization Analysis
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
from app.config import get_cluster_name
from app.data_loader import load_community_metrics, load_graph_files
from app.utils import render_network_graph


def render_page_2():
    """Display page 2: Echo Chambers & Polarization."""
    st.header("Echo Chambers & Polarization Analysis")
    st.markdown("""
    How do users interact? We constructed a massive cross-platform directed graph using replies and mentions to detect echo chambers via **Louvain Modularity**.
    """)
    
    csv_path = "deliverables/week_6/community_polarization_metrics.csv"
    metrics_df = load_community_metrics()
    
    tab1, tab2, tab3 = st.tabs(["Interaction Network", "Polarization Heatmap", "Topological Metrics"])
    
    with tab1:
        _render_network_tab(metrics_df)
    
    with tab2:
        _render_polarization_heatmap_tab(metrics_df)
    
    with tab3:
        _render_topological_metrics_tab()


def _render_network_tab(metrics_df):
    """Render the Interaction Network tab."""
    st.subheader("Interactive Cross-Platform Network")
    st.info("**How to read this graph:**\n* **Nodes (Circles):** Individual users or posts. Size is based on their *Degree* (influence/number of connections).\n* **Colors:** Represent distinct 'Echo Chambers' (Louvain clusters). Click on the legend items to filter clusters in or out.\n* **Edges (Lines):** Direct interactions (mentions, replies, quotes).")
    st.markdown("Zoom and pan to explore the topology of political discourse. Noise has been filtered out (only users with ≥2 connections are shown) to reveal the true core structure.")
    
    gml_path = "deliverables/week_5/cross_platform_merged.gml"
    layout_path = "deliverables/week_5/layout_positions.json"
    
    exists, msg = load_graph_files(gml_path, layout_path)
    if exists:
        @st.cache_data(show_spinner="Loading massive Plotly WebGL graph...")
        def render_cached_graph():
            return render_network_graph(gml_path, layout_path)
        
        fig = render_cached_graph()
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("""
        **Key Topological Takeaways:**
        *   **Bipartite Clustering**: Nodes represent users and discussion venues (subreddits/videos). The clear spatial separation between groups visually proves strong political self-segregation.
        *   **Louvain Echo Chambers**: Colors represent distinct partitioned communities. The lack of bridging connections between different color groups mathematically confirms the existence of isolated echo chambers.
        """)
        
        # Metrics table
        if metrics_df is not None:
            st.markdown("---")
            st.markdown("### Echo Chamber Polarization Metrics")
            st.dataframe(
                metrics_df[['Community', 'We_Them_Ratio', 'Mean_Toxicity', 'Polarization_Index']]
                .style.format(precision=2)
                .background_gradient(cmap='RdYlGn_r', subset=['Mean_Toxicity'], vmin=0.35, vmax=0.55)
                .background_gradient(cmap='RdYlGn_r', subset=['Polarization_Index'], vmin=0.05, vmax=0.50)
                .background_gradient(cmap='RdYlGn_r', subset=['We_Them_Ratio'], vmin=0.15, vmax=1.10),
                use_container_width=True
            )
    else:
        st.warning(msg)


def _render_polarization_heatmap_tab(metrics_df):
    """Render the Polarization Heatmap tab."""
    st.subheader("Community Polarization Heatmap")
    if metrics_df is not None:
        top_polar = metrics_df.loc[metrics_df['Polarization_Index'].idxmax()]
        st.error(f"**Highest Polarization Detected:** {top_polar['Community']} with an index of **{top_polar['Polarization_Index']:.3f}**.")
        
        original_df = metrics_df.set_index('Community')[['We_Them_Ratio', 'Mean_Toxicity', 'Polarization_Index']]
        normalized_df = (original_df - original_df.min()) / (original_df.max() - original_df.min() + 1e-9)
        
        fig_hm = px.imshow(
            normalized_df,
            color_continuous_scale=['#2E7D32', '#FBC02D', '#D32F2F'],
            aspect="auto",
            labels=dict(x="Metrics", y="Echo Chamber")
        )
        
        fig_hm.update_traces(
            text=original_df.values,
            texttemplate="%{text:.2f}",
            customdata=original_df.values,
            hovertemplate="<b>Echo Chamber:</b> %{y}<br><b>Metric:</b> %{x}<br><b>Actual Value:</b> %{customdata:.2f}<extra></extra>"
        )
        
        fig_hm.update_layout(
            coloraxis_showscale=False,
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font_color="white",
            margin=dict(t=20, l=10, r=10, b=20),
            height=400
        )
        st.plotly_chart(fig_hm, use_container_width=True)
        
        st.markdown("""
        **Heatmap Interpretation & Insights:**
        *   **Visualizing Extremes**: This heatmap highlights the concentration of tribal behavior across communities. Red cells represent highly elevated scores (high toxicity/polarization), while green cells indicate healthier, less-polarized discussion environments.
        *   **Linguistic & Toxicity Corroboration**: It reveals whether a community is simply internally cohesive (high *We/Them Ratio* but low *Toxicity*) or actively hostile (high scores in both categories). Communities exhibiting elevated values in both dimensions highlight critical echo chambers.
        """)
    else:
        st.info("Metrics data not available.")


def _render_topological_metrics_tab():
    """Render the Topological Metrics tab."""
    st.subheader("Topological Modularity Metrics")
    if os.path.exists("deliverables/week_5/echo_chamber_metrics.txt"):
        with open("deliverables/week_5/echo_chamber_metrics.txt", "r") as f:
            metrics = f.read()
        st.code(metrics, language="text")
    else:
        st.info("Metrics file missing. Please run Week 5 graph script.")
    
    st.subheader("Echo Chamber Size Distribution")
    gml_path = "deliverables/week_5/cross_platform_merged.gml"
    if os.path.exists(gml_path):
        G_core = nx.read_gml(gml_path)
        degrees = dict(G_core.degree())
        core_nodes = [n for n in G_core.nodes() if degrees.get(n, 1) >= 2]
        
        comm_sizes = {}
        for n in core_nodes:
            comm = G_core.nodes[n].get('community', 0)
            comm_sizes[comm] = comm_sizes.get(comm, 0) + 1
        
        comm_data = []
        for comm, size in comm_sizes.items():
            comm_data.append({"Echo Chamber": get_cluster_name(comm), "Core Members": size})
        
        df_comm = pd.DataFrame(comm_data).sort_values("Core Members", ascending=False)
        
        fig_size = px.bar(
            df_comm, x="Echo Chamber", y="Core Members",
            color="Echo Chamber",
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_size.update_layout(
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font_color="white",
            showlegend=False,
            xaxis_title="",
            yaxis_title="Core Nodes Count"
        )
        st.plotly_chart(fig_size, use_container_width=True)
