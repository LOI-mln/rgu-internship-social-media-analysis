"""
Data loading and preprocessing.
"""

import os
import pandas as pd
import streamlit as st
from typing import List, Optional
from app.config import UPLOADED_DIR, CLEANED_DIR
from app.utils.text_processing import count_pronouns_in_text, get_pronoun_regex


@st.cache_data(show_spinner=False, ttl=60)
def load_time_series_data() -> pd.DataFrame:
    """
    Load time series data from all platforms.
    
    Returns:
        Combined DataFrame with columns: date, platform, we_count, them_count
    """
    we_regex, them_regex = get_pronoun_regex()
    dfs: List[pd.DataFrame] = []
    
    # YouTube
    try:
        yt_df = pd.read_csv(f"{CLEANED_DIR}/youtube_cleaned.csv")
        yt_df['platform'] = 'YouTube'
        yt_df['date'] = pd.to_datetime(yt_df['timestamp'], unit='s', errors='coerce')
        dfs.append(yt_df[['date', 'platform', 'we_count', 'them_count']])
    except Exception:
        pass
    
    # Reddit
    try:
        rd_df = pd.read_csv(f"{CLEANED_DIR}/reddit_political_cleaned.csv")
        rd_df = rd_df[rd_df['author'] != 'PoliticsModeratorBot']
        rd_df['date'] = pd.to_datetime(rd_df['created_utc'], errors='coerce')
        rd_df['platform'] = 'Reddit'
        dfs.append(rd_df[['date', 'platform', 'we_count', 'them_count']])
    except Exception:
        pass
    
    # Twitter
    try:
        tw_df = pd.read_csv("data/shahana_bano_datasets/twitter/twitter_we-language_dataset.csv")
        tw_df['date'] = pd.to_datetime(tw_df['createdAt'], errors='coerce')
        tw_df['platform'] = 'Twitter'
        tw_text = tw_df['text'].astype(str).str.lower()
        tw_df['we_count'] = tw_text.str.count(we_regex)
        tw_df['them_count'] = tw_text.str.count(them_regex)
        dfs.append(tw_df[['date', 'platform', 'we_count', 'them_count']])
    except Exception:
        pass
    
    # Instagram
    try:
        ig_df = pd.read_csv("data/shahana_bano_datasets/instagram/instagram_comments_dataset.csv")
        ig_df['date'] = pd.to_datetime(ig_df['timestamp'], errors='coerce')
        ig_df['platform'] = 'Instagram'
        ig_text = ig_df['text'].astype(str).str.lower()
        ig_df['we_count'] = ig_text.str.count(we_regex)
        ig_df['them_count'] = ig_text.str.count(them_regex)
        dfs.append(ig_df[['date', 'platform', 'we_count', 'them_count']])
    except Exception:
        pass
    
    # Dynamic uploaded datasets
    if os.path.exists(UPLOADED_DIR):
        for filename in os.listdir(UPLOADED_DIR):
            if filename.endswith(".csv"):
                try:
                    up_df = pd.read_csv(os.path.join(UPLOADED_DIR, filename))
                    up_df['date'] = pd.to_datetime(up_df['date'], errors='coerce')
                    dfs.append(up_df[['date', 'platform', 'we_count', 'them_count']])
                except Exception:
                    pass
    
    if not dfs:
        return pd.DataFrame()
    
    combined = pd.concat(dfs, ignore_index=True)
    combined['date'] = pd.to_datetime(combined['date'], errors='coerce')
    
    # Extract month-year
    mask = combined['date'].notna()
    combined.loc[mask, 'month_year'] = combined.loc[mask, 'date'].dt.to_period('M').astype(str)
    
    return combined


def load_community_metrics() -> Optional[pd.DataFrame]:
    """
    Load polarization metrics for communities.
    
    Returns:
        DataFrame or None if file doesn't exist
    """
    metrics_path = "deliverables/week_6/community_polarization_metrics.csv"
    
    if not os.path.exists(metrics_path):
        return None
    
    df = pd.read_csv(metrics_path)
    from app.config import get_cluster_name
    df['Community'] = df['Community'].apply(lambda x: get_cluster_name(int(x.split()[-1])))
    
    return df


def load_graph_files(gml_path: str, layout_path: str) -> tuple[bool, str]:
    """
    Verify that graph files exist.
    
    Args:
        gml_path: Path to GML file
        layout_path: Path to layout JSON file
    
    Returns:
        Tuple (exist: bool, message: str)
    """
    if not os.path.exists(gml_path):
        return False, f"GML file not found: {gml_path}"
    if not os.path.exists(layout_path):
        return False, f"Layout file not found: {layout_path}"
    return True, "Files found"


@st.cache_data(show_spinner=False)
def load_clip_data() -> Optional[pd.DataFrame]:
    """
    Load precomputed CLIP data.
    
    Returns:
        DataFrame or None if file doesn't exist
    """
    clip_path = "data/cleaned/hateful_memes_clip_scored.csv"
    if not os.path.exists(clip_path):
        return None
    try:
        return pd.read_csv(clip_path)
    except Exception:
        return None

