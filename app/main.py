"""
Streamlit main application: We vs Them - Social Media Polarization Dashboard
Main entry point orchestrating the user interface.
"""

import os
import streamlit as st
import streamlit.components.v1 as components

from app.config import PAGE_CONFIG, UPLOADED_DIR
from app.styles import get_custom_css
from app.pages import render_page_1, render_page_2, render_page_3, render_page_4


def main():
    """Main function orchestrating the Streamlit application."""
    # Page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Cache invalidation based on uploaded files state
    _setup_cache_invalidation()
    
    # Apply custom styling
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Dashboard Header
    st.title("We vs Them: Social Media Polarization")
    st.markdown("An interactive dashboard analyzing political discourse, echo chambers, and toxicity across multiple platforms.")
    
    # Sidebar Navigation
    st.sidebar.markdown("## Dashboard Navigation")
    selected_page = st.sidebar.radio(
        "Navigation Menu",
        [
            "1. Overview & AI Baselines",
            "2. Echo Chambers & Polarization",
            "3. Cross-Platform Metrics",
            "4. Import New Dataset"
        ],
        label_visibility="collapsed"
    )
    
    # Sidebar System Configuration
    st.sidebar.markdown("---")
    _render_sidebar_config()
    
    # Route to selected page
    if selected_page.startswith("1."):
        render_page_1()
    elif selected_page.startswith("2."):
        render_page_2()
    elif selected_page.startswith("3."):
        render_page_3()
    elif selected_page.startswith("4."):
        render_page_4()


def _setup_cache_invalidation():
    """Setup cache invalidation based on uploaded files state."""
    current_uploaded_files = sorted(os.listdir(UPLOADED_DIR)) if os.path.exists(UPLOADED_DIR) else []
    
    if "uploaded_files_state" not in st.session_state:
        st.session_state["uploaded_files_state"] = current_uploaded_files
    elif st.session_state["uploaded_files_state"] != current_uploaded_files:
        st.session_state["uploaded_files_state"] = current_uploaded_files
        st.cache_data.clear()


def _render_sidebar_config():
    """Render system configuration in the sidebar."""
    st.sidebar.markdown("### System Configuration")
    st.sidebar.markdown("""
    <div style="background-color: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 12px; font-family: 'Inter', sans-serif;">
        <div style="font-size: 11px; color: #8E9AA8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Database Metrics</div>
        <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
            <span style="color: #8E9AA8;">Total Corpus:</span>
            <span style="font-weight: 700; color: #FAFAFA;">32,223</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
            <span style="color: #8E9AA8;">- YouTube:</span>
            <span style="font-weight: 600; color: #FAFAFA;">24,860</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 8px;">
            <span style="color: #8E9AA8;">- Reddit:</span>
            <span style="font-weight: 600; color: #FAFAFA;">7,363</span>
        </div>
        <hr style="border: 0; border-top: 1px solid rgba(255, 255, 255, 0.05); margin: 8px 0;">
        <div style="font-size: 11px; color: #8E9AA8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Classifier & Graph</div>
        <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
            <span style="color: #8E9AA8;">Toxicity Model:</span>
            <span style="font-weight: 700; color: #3B82F6;">DistilBERT</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px;">
            <span style="color: #8E9AA8;">Graph Modularity:</span>
            <span style="font-weight: 700; color: #3B82F6;">Q = 0.6071</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="margin-top: 20px; font-size: 11px; color: #5C6878; font-family: 'Inter', sans-serif; text-align: center;">
        Milan Loi &bull; Supervisor: Dr. Shahana Bano
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
