"""
Common utilities for text processing.
Centralizes duplicated functions across the different scripts.
"""

import re
import pandas as pd
from typing import List, Dict, Union, Tuple


# ==============================================================================
# LEXICONS
# ==============================================================================

NEGATIVE_WORDS = ['bad', 'worst', 'hate', 'stupid', 'idiot', 'fake', 'liar', 'worse', 'terrible', 'awful', 'angry']
WE_WORDS = ['we', 'us', 'our', 'ours', 'ourselves']
THEM_WORDS = ['they', 'them', 'their', 'theirs', 'themselves']


# ==============================================================================
# TEXT PROCESSING FUNCTIONS
# ==============================================================================

def count_words(text: str, word_list: List[str]) -> int:
    """
    Count the number of occurrences of words from a list in a text.
    Uses word boundaries to avoid false positives.
    
    Args:
        text: Text to analyze
        word_list: List of words to search for
    
    Returns:
        Total number of occurrences
    """
    text = str(text).lower()
    return sum(len(re.findall(r'\b' + word + r'\b', text)) for word in word_list)


def count_pronouns(text: str, pronouns: List[str]) -> int:
    """
    Count pronouns in a text (alternative implementation).
    
    Args:
        text: Text to analyze
        pronouns: List of pronouns
    
    Returns:
        Number of pronouns found
    """
    if not isinstance(text, str):
        return 0
    words = re.findall(r'\b\w+\b', text.lower())
    return sum(1 for word in words if word in pronouns)


def extract_pronoun_counts(text: str) -> Dict[str, int]:
    """
    Extract all pronoun counts in a single pass.
    
    Args:
        text: Text to analyze
    
    Returns:
        Dict with 'we_count', 'them_count', and 'negativity_score'
    """
    return {
        'we_count': count_words(text, WE_WORDS),
        'them_count': count_words(text, THEM_WORDS),
        'negativity_score': count_words(text, NEGATIVE_WORDS)
    }


def scale_timestamps(
    series_or_datetime: Union[pd.Series, pd.Timestamp],
    target_start: str = '2018-01-01 00:00:00',
    target_end: str = '2026-05-31 23:59:59'
) -> pd.Series:
    """
    Rescale timestamps to a target range.
    Useful for harmonizing timestamps across platforms.
    
    Args:
        series_or_datetime: Date series or single timestamp
        target_start: Target start date
        target_end: Target end date
    
    Returns:
        Rescaled series
    """
    dt_series = pd.to_datetime(series_or_datetime, errors='coerce')
    min_val = dt_series.min()
    max_val = dt_series.max()
    
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return dt_series
    
    target_min = pd.to_datetime(target_start)
    target_max = pd.to_datetime(target_end)
    
    scaled_series = target_min + (dt_series - min_val) / (max_val - min_val) * (target_max - target_min)
    return scaled_series
