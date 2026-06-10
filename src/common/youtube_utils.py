"""
Common utilities for YouTube scrapers.
Consolidates v1 and v2 into a unified implementation.
"""

import pandas as pd
import os
from typing import Optional, Dict


# ==============================================================================
# VIDEO METADATA
# ==============================================================================

VIDEO_UPLOAD_DATES: Dict[str, str] = {
    # BBC & Al Jazeera - Gaza conflict 2025-2026
    'u8C6l9sa_fM': '2025-10-28',  # Netanyahu orders strike Gaza - BBC
    '2xwXLWhLYx0': '2026-04-14',  # US-sanctioned ships Strait of Hormuz - BBC
    'IA8YL_Datm0': '2025-09-23',  # Gaza: Dying for Food - BBC
    'Jakyor8TUB4': '2026-04-13',  # US prepares blockade Strait of Hormuz - BBC
    '_GpMnIdnYr4': '2026-04-12',  # Iran-US peace talks fail - BBC
    'p9ONnNFdNtQ': '2025-10-07',  # Inside Gaza total devastation - BBC
    'E7FLymwDCk8': '2026-05-01',  # Gaza is Burning - Al Jazeera
    '51BvCUpcBTc': '2025-11-15',  # Israel man-made famine - Al Jazeera
    'MJqFLSpnKoU': '2026-04-20',  # US blockade on Iranian ports - BBC
    '-pMuAYM8EIc': '2026-04-15',  # US Blockade Hormuz Tinderbox - CNN
    # Historical political videos 2018-2024
    'BHe0LkMsV_g': '2018-01-01',  # DACA immigration reform 2018
    '4KIpnPapquY': '2018-09-25',  # Trump at UN General Assembly - BBC
    '2Cm8Su-bbmw': '2018-07-11',  # Trump tells NATO to pay up - BBC
    'eXBV8YU2TeI': '2019-02-27',  # Brexit next steps debate
    'eidqxI2l_iA': '2019-10-19',  # Super Saturday Brexit debate
    'VwCxyWcBSx8': '2019-11-15',  # Trump on Impeachment Hearing
    '6XcXaS55Qpk': '2019-11-20',  # Trump impeachment testimony
    'bGkr9n6DwSg': '2019-12-09',  # Goldman impeachment opening
    'LlJIwTd9fqI': '2020-03-23',  # Boris Johnson UK lockdown
    'vJycNmK7KPk': '2020-03-23',  # Coronavirus PM statement - BBC
    'CweqW7Pzxz8': '2020-09-30',  # First debate Trump vs Biden
    'wW1lY5jFNcQ': '2020-09-30',  # 2020 Presidential Debate
    'u3v2VQEa--w': '2020-06-03',  # George Floyd protests London
    'YfoEisa0DEc': '2020-05-29',  # Political fallout George Floyd
    'jWJVMoe7OY0': '2021-07-01',  # Day of Rage Capitol - NYT
    'hMSK0lI_shA': '2021-04-14',  # Biden Afghanistan withdrawal
    'CS1IdVC-n7Y': '2021-08-19',  # Biden defended Afghanistan
    'MVu8QbxafJE': '2022-03-02',  # Putin war on Ukraine - Vox
    'icRHnVKyrcw': '2022-09-24',  # Ukraine 2022 documentary
    'b-9czRep8hA': '2022-10-20',  # Liz Truss resigns
    '1kNSoNrthKg': '2022-10-21',  # Why Liz Truss time ended - BBC
    'Ulg-96K3qMc': '2023-10-07',  # Hamas October 7 breakdown
    'PcQaG4sC9BM': '2023-10-07',  # NBC Special Report Israel war
    'Fp-QHzpsjWo': '2023-03-30',  # Israel-Hamas War summarized
    '2ec4Oa2L1fo': '2024-09-11',  # Harris v Trump debate
    'MUYepJ5fNp8': '2024-09-11',  # Key moments Trump Harris - BBC
    '2tIXGym1I-s': '2026-05-29',  # Netanyahu tears up ceasefire
    'B9C7X8dPJtg': '2024-02-29',  # 40-day ceasefire in Gaza
    '6_RdnVtfZPY': '2019-06-11',  # Hong Kong protests - Vox
    '_0atzea-mPY': '2023-10-07',  # October 7 - Al Jazeera
}


def map_comments_to_video_dates(df: pd.DataFrame, video_id_col: str = 'video_id', timestamp_col: str = 'timestamp') -> pd.DataFrame:
    """
    Map comment timestamps to video publication dates.
    Improves temporal analysis by replacing yt-dlp approximations.
    
    Args:
        df: DataFrame with a video_id column
        video_id_col: Name of the column containing the video ID
        timestamp_col: Name of the timestamp column to update
    
    Returns:
        Modified DataFrame with mapped timestamps
    """
    df_copy = df.copy()
    df_copy['video_upload_date'] = df_copy[video_id_col].map(VIDEO_UPLOAD_DATES)
    
    mapped_count = df_copy['video_upload_date'].notna().sum()
    if mapped_count > 0:
        upload_ts = pd.to_datetime(df_copy['video_upload_date'], errors='coerce')
        mask = upload_ts.notna()
        df_copy.loc[mask, timestamp_col] = upload_ts[mask].astype(int) // 10**9
        print(f"  Mapped {mapped_count}/{len(df_copy)} comments to video upload dates.")
    
    df_copy = df_copy.drop(columns=['video_upload_date'], errors='ignore')
    return df_copy
