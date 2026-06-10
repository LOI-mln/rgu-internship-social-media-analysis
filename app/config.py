"""
Central configuration and application constants.
"""

from typing import Dict

# ==============================================================================
# CLUSTER NAMES & COMMUNITY LABELS
# ==============================================================================

CLUSTER_NAMES: Dict[int, str] = {
    0: "Conservative Hub",
    1: "Progressive Network",
    2: "Mainstream Media & News",
    3: "Alt-Right Echo Chamber",
    4: "Neutral / Discussion",
    5: "Far-Left Network",
    6: "Conspiracy & Fringe",
    7: "Local Politics",
    8: "International Discourse",
    9: "Climate Change & Environmental Awareness"
}


from typing import Dict, Union


def get_cluster_name(comm_id: Union[int, str]) -> str:
    """
    Retrieve cluster name by ID.
    
    Args:
        comm_id: Cluster ID (int or str)
    
    Returns:
        Cluster name or generic fallback
    """
    return CLUSTER_NAMES.get(int(comm_id), f"Cluster {comm_id}")


# ==============================================================================
# PRONOUN PATTERNS
# ==============================================================================

WE_PRONOUNS = ["we", "us", "our", "ours", "ourselves"]
THEM_PRONOUNS = ["they", "them", "their", "theirs", "themselves"]

# ==============================================================================
# PATHS
# ==============================================================================

DATA_DIR = "data"
UPLOADED_DIR = f"{DATA_DIR}/uploaded"
CLEANED_DIR = f"{DATA_DIR}/cleaned"
DELIVERABLES_DIR = "deliverables"

# ==============================================================================
# POLITICAL EVENTS FOR TEMPORAL ANALYSIS
# ==============================================================================

POLITICAL_EVENTS: Dict[str, str] = {
    "2018Q4": "US Midterms",
    "2019Q4": "Trump Impeach.",
    "2020Q4": "US Election",
    "2021Q1": "Capitol Riot",
    "2022Q4": "US Midterms",
    "2023Q4": "Gaza Conflict",
    "2024Q4": "US Election",
    "2025Q1": "Trump Inaug."
}

# ==============================================================================
# UI CONFIGURATION
# ==============================================================================

PAGE_CONFIG = {
    "page_title": "Echo Chambers & Polarization",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

COLORS_PALETTE = ["#FF416C", "#1E90FF", "#32CD32", "#FFD700", "#FF8C00", "#8A2BE2", "#00CED1", "#FF1493"]
