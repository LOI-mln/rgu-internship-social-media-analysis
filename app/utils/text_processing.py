"""
Text processing utilities for linguistic analysis.
"""

import re
from typing import Tuple
import pandas as pd
from app.config import WE_PRONOUNS, THEM_PRONOUNS


def get_pronoun_regex() -> Tuple[str, str]:
    """
    Create regex patterns for pronouns.
    
    Returns:
        Tuple of (we_regex, them_regex)
    """
    we_regex = r'\b(?:' + '|'.join(WE_PRONOUNS) + r')\b'
    them_regex = r'\b(?:' + '|'.join(THEM_PRONOUNS) + r')\b'
    return we_regex, them_regex


def count_pronouns_in_text(text: str) -> Tuple[int, int]:
    """
    Count 'we' and 'them' pronouns in text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Tuple of (we_count, them_count)
    """
    if not isinstance(text, str) or not text.strip():
        return 0, 0
    
    text_lower = text.lower()
    we_regex, them_regex = get_pronoun_regex()
    
    we_count = len(re.findall(we_regex, text_lower))
    them_count = len(re.findall(them_regex, text_lower))
    
    return we_count, them_count


def calculate_we_them_ratio(df: pd.DataFrame, laplace_smoothing: int = 10) -> pd.Series:
    """
    Calculate we/them ratio with Laplace smoothing.
    
    Args:
        df: DataFrame with 'we_count' and 'them_count' columns
        laplace_smoothing: Smoothing value (default 10)
    
    Returns:
        Series with ratios
    """
    return (df['we_count'] + laplace_smoothing) / (df['them_count'] + laplace_smoothing)
