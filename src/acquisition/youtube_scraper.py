"""
Unified YouTube scraper for political videos.
Consolidates v1 and v2 into a single reliable implementation.

Uses yt-dlp to scrape YouTube comments with full support for political videos
covering major events from 2018 to 2026.
"""

import subprocess
import json
import pandas as pd
import os
import sys
from typing import List, Dict, Optional

# Add the src directory to the import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.common import map_comments_to_video_dates


# Verified real YouTube video IDs covering major political events 2018-2026
# Grouped by year/topic for documentation
POLITICAL_VIDEO_IDS: List[str] = [
    # 2018 - Trump immigration, Midterms, UN
    "BHe0LkMsV_g",  # DACA immigration reform
    "4KIpnPapquY",  # Trump at UN General Assembly - BBC
    "2Cm8Su-bbmw",  # Trump tells NATO allies to pay up - BBC

    # 2019 - Brexit, Trump Impeachment
    "eXBV8YU2TeI",  # Brexit "next steps" debate
    "eidqxI2l_iA",  # Super Saturday: MPs Brexit debate
    "VwCxyWcBSx8",  # Trump on Impeachment Hearing
    "6XcXaS55Qpk",  # Trump impeachment testimony
    "bGkr9n6DwSg",  # Goldman's impeachment opening

    # 2020 - COVID lockdown, Election, George Floyd
    "LlJIwTd9fqI",  # Boris Johnson UK lockdown
    "vJycNmK7KPk",  # COVID PM statement - BBC
    "CweqW7Pzxz8",  # First debate Trump vs Biden
    "wW1lY5jFNcQ",  # 2020 Presidential Debate
    "u3v2VQEa--w",  # George Floyd protests London
    "YfoEisa0DEc",  # George Floyd political fallout

    # 2021 - Capitol riot, Afghanistan withdrawal
    "jWJVMoe7OY0",  # Capitol riot Day of Rage - NYT
    "hMSK0lI_shA",  # Biden Afghanistan withdrawal
    "CS1IdVC-n7Y",  # Biden defended Afghanistan

    # 2022 - Russia/Ukraine war, UK PM crisis
    "MVu8QbxafJE",  # Putin war on Ukraine - Vox
    "icRHnVKyrcw",  # Ukraine 2022 documentary
    "b-9czRep8hA",  # Liz Truss resigns as PM
    "1kNSoNrthKg",  # Why Liz Truss PM time ended - BBC

    # 2023 - Israel-Hamas October 7 war
    "Ulg-96K3qMc",  # Hamas October 7 minute-by-minute
    "PcQaG4sC9BM",  # NBC Special Report Israel-Hamas war
    "Fp-QHzpsjWo",  # Israel-Hamas War summarized

    # 2024 - US Election, Gaza crisis
    "2ec4Oa2L1fo",  # Harris v Trump debate
    "MUYepJ5fNp8",  # Key moments Trump Harris - BBC

    # 2025-2026 - Gaza conflict escalation
    "u8C6l9sa_fM",  # Netanyahu orders Gaza strike - BBC
    "2xwXLWhLYx0",  # US ships Strait of Hormuz - BBC
    "IA8YL_Datm0",  # Gaza: Dying for Food - BBC
    "p9ONnNFdNtQ",  # Inside Gaza devastation - BBC
    "E7FLymwDCk8",  # Gaza is Burning - Al Jazeera
    "51BvCUpcBTc",  # Israel man-made famine - Al Jazeera
    "_0atzea-mPY",  # October 7 - Al Jazeera
    "6_RdnVtfZPY",  # Hong Kong protests - Vox
]


def scrape_comments(video_id: str, max_comments: int = 500) -> Optional[pd.DataFrame]:
    """
    Scrape YouTube comments from a specific video.
    
    Args:
        video_id: YouTube video ID
        max_comments: Maximum number of comments to scrape
    
    Returns:
        DataFrame with comments, or None on error
    """
    try:
        output_template = json.dumps({
            'id': '%(id)s',
            'text': '%(text)s',
            'author': '%(author)s',
            'timestamp': '%(timestamp)s',
            'author_id': '%(author_id)s',
            'author_thumbnail': '%(author_thumbnail)s',
            'author_is_uploader': '%(author_is_uploader)s',
            'like_count': '%(like_count)s',
            'is_favorited': '%(is_favorited)s',
        })
        
        # Use yt-dlp to extract comments
        cmd = [
            'yt-dlp',
            '--extractor-args', f'youtube:max_comments={max_comments}',
            '--dump-single-json',
            '-j',
            f'https://www.youtube.com/watch?v={video_id}',
            '-o', json.dumps({'default': output_template})
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"  ✗ Video {video_id}: {result.stderr[:100]}")
            return None
        
        # Parse output
        lines = result.stdout.strip().split('\n')
        comments = []
        
        for line in lines:
            try:
                comment = json.loads(line)
                comments.append({
                    'id': comment.get('id', ''),
                    'text': comment.get('text', ''),
                    'author': comment.get('author', 'Unknown'),
                    'timestamp': comment.get('timestamp', 0),
                    'author_id': comment.get('author_id', ''),
                    'likes': comment.get('like_count', 0),
                    'video_id': video_id,
                })
            except json.JSONDecodeError:
                continue
        
        if comments:
            print(f"  ✓ Video {video_id}: Scraped {len(comments)} comments")
            return pd.DataFrame(comments)
        else:
            print(f"  ~ Video {video_id}: No comments found")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"  ✗ Video {video_id}: Timeout")
        return None
    except Exception as e:
        print(f"  ✗ Video {video_id}: {str(e)[:100]}")
        return None


def main():
    """Scrape all political videos and consolidate them into a single CSV."""
    print("YouTube Comment Scraper - Political Videos 2018-2026")
    print(f"Scraping {len(POLITICAL_VIDEO_IDS)} videos...")
    
    all_comments = []
    
    for idx, video_id in enumerate(POLITICAL_VIDEO_IDS, 1):
        print(f"\n[{idx}/{len(POLITICAL_VIDEO_IDS)}] Processing {video_id}...")
        df_comments = scrape_comments(video_id, max_comments=500)
        
        if df_comments is not None and not df_comments.empty:
            all_comments.append(df_comments)
    
    if not all_comments:
        print("Error: No comments were scraped from any video.")
        return
    
    # Combine all comments
    df_combined = pd.concat(all_comments, ignore_index=True)
    
    # Map to video upload dates for better temporal analysis
    df_combined = map_comments_to_video_dates(df_combined)
    
    # Save
    os.makedirs("data/raw", exist_ok=True)
    output_path = "data/raw/youtube_political.csv"
    df_combined.to_csv(output_path, index=False)
    
    print(f"\n✓ Scraping complete!")
    print(f"  Total comments: {len(df_combined)}")
    print(f"  Total videos: {df_combined['video_id'].nunique()}")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
