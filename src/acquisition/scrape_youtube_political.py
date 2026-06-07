"""
scrape_youtube_political.py
Scrapes real YouTube comments from political videos using yt-dlp.
Videos are selected to cover major political events across 2018-2026.
"""

import subprocess
import json
import pandas as pd
import os
import sys

# Real political YouTube video URLs covering major events across multiple years.
# Selected from BBC News, CNN, Al Jazeera, Sky News, and other major outlets.
POLITICAL_VIDEOS = [
    # 2018 - Trump-Kim summit, US Midterms
    "https://www.youtube.com/watch?v=5gII9dEbcvA",  # BBC: Trump-Kim summit Singapore
    "https://www.youtube.com/watch?v=QS2BdSA-mhk",  # BBC: Jamal Khashoggi case
    "https://www.youtube.com/watch?v=6ZbOEpIbY_g",  # CNN: 2018 Midterm elections

    # 2019 - Trump impeachment, Hong Kong, Brexit
    "https://www.youtube.com/watch?v=smKMZ1YvqGE",  # BBC: Trump impeachment explained
    "https://www.youtube.com/watch?v=6_RdnVtfZPY",  # BBC: Hong Kong protests
    "https://www.youtube.com/watch?v=eCwB0XPHV-8",  # Sky: Brexit deal Boris Johnson

    # 2020 - COVID, George Floyd, US Election Biden vs Trump
    "https://www.youtube.com/watch?v=i6rtGE-yShI",  # BBC: COVID first lockdown UK
    "https://www.youtube.com/watch?v=EbftCo_TLf0",  # CNN: George Floyd protests
    "https://www.youtube.com/watch?v=D0q4K5MZOkE",  # BBC: US Election 2020 results

    # 2021 - Capitol riot, Biden inauguration, Afghanistan withdrawal
    "https://www.youtube.com/watch?v=ibPLxFocUhQ",  # BBC: Capitol riot Jan 6
    "https://www.youtube.com/watch?v=q5iCPKDp4V4",  # BBC: Afghanistan Taliban Kabul
    "https://www.youtube.com/watch?v=eApUBk4Mfmc",  # CNN: Biden inauguration

    # 2022 - Russia invades Ukraine, UK PM crisis, Iran protests
    "https://www.youtube.com/watch?v=hNIGRLjJMjQ",  # BBC: Russia invades Ukraine
    "https://www.youtube.com/watch?v=vJ3jHaTnWVw",  # BBC: Ukraine war latest
    "https://www.youtube.com/watch?v=oWKc2c2W2rU",  # BBC: Iran Mahsa Amini protests

    # 2023 - Israel-Hamas Oct 7, Ukraine counteroffensive
    "https://www.youtube.com/watch?v=_0atzea-mPY",  # BBC: Hamas attack Oct 7
    "https://www.youtube.com/watch?v=nt2xJhwfsYY",  # Al Jazeera: Gaza war
    "https://www.youtube.com/watch?v=HH_JMPZgI2M",  # BBC: Ukraine counteroffensive

    # 2024 - US Election 2024, Gaza crisis, UK election
    "https://www.youtube.com/watch?v=6wM5MO8AraI",  # BBC: US Election 2024
    "https://www.youtube.com/watch?v=vq3K9sBMCOg",  # CNN: Trump vs Harris debate
    "https://www.youtube.com/watch?v=wj2f6x8i6tU",  # BBC: UK General Election 2024

    # 2025-2026 - Existing videos already in the dataset for these years
    "https://www.youtube.com/watch?v=u8C6l9sa_fM",  # BBC: Netanyahu orders strike Gaza
    "https://www.youtube.com/watch?v=2xwXLWhLYx0",  # BBC: US sanctions Strait of Hormuz
]


def scrape_comments(video_url, max_comments=500):
    """
    Use yt-dlp to extract comments from a YouTube video.
    Returns a list of comment dicts or an empty list on failure.
    """
    print(f"  Scraping: {video_url}")
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-comments",
        "--dump-json",
        "--extractor-args", f"youtube:max_comments={max_comments},all,100,100",
        "--no-warnings",
        video_url,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # 2 min timeout per video
        )
        if result.returncode != 0:
            print(f"    [WARN] yt-dlp failed for {video_url}: {result.stderr[:200]}")
            return []

        data = json.loads(result.stdout)
        comments_raw = data.get("comments", [])
        video_id = data.get("id", "")
        video_title = data.get("title", "")

        comments = []
        for c in comments_raw:
            comments.append({
                "id": c.get("id", ""),
                "parent": c.get("parent", "root"),
                "text": c.get("text", ""),
                "like_count": c.get("like_count", 0),
                "author_id": c.get("author_id", ""),
                "author": c.get("author", ""),
                "author_thumbnail": c.get("author_thumbnail", ""),
                "author_is_uploader": c.get("author_is_uploader", False),
                "author_is_verified": c.get("author_is_verified", False),
                "author_url": c.get("author_url", ""),
                "is_favorited": c.get("is_favorited", False),
                "_time_text": c.get("_time_text", ""),
                "timestamp": c.get("timestamp", 0),
                "is_pinned": c.get("is_pinned", False),
                "video_id": video_id,
                "video_title": video_title,
            })
        print(f"    Extracted {len(comments)} comments from: {video_title}")
        return comments

    except subprocess.TimeoutExpired:
        print(f"    [WARN] Timeout for {video_url}")
        return []
    except json.JSONDecodeError as e:
        print(f"    [WARN] JSON parse error for {video_url}: {e}")
        return []
    except Exception as e:
        print(f"    [WARN] Unexpected error for {video_url}: {e}")
        return []


def main():
    all_comments = []
    total_videos = len(POLITICAL_VIDEOS)

    # Skip videos that are already in the existing dataset
    raw_path = "data/raw/youtube_actual_politic.csv"
    existing_df = pd.read_csv(raw_path)
    existing_video_ids = set(existing_df["video_id"].unique())
    print(f"Existing dataset: {len(existing_df)} rows, {len(existing_video_ids)} unique videos")
    print(f"Scraping comments from {total_videos} political videos...\n")

    for i, url in enumerate(POLITICAL_VIDEOS, 1):
        # Extract video ID from URL to check if we already have it
        vid_id = url.split("watch?v=")[-1].split("&")[0] if "watch?v=" in url else ""
        if vid_id in existing_video_ids:
            print(f"[{i}/{total_videos}] SKIP (already in dataset): {vid_id}")
            continue

        print(f"[{i}/{total_videos}]")
        comments = scrape_comments(url, max_comments=500)
        all_comments.extend(comments)
        print(f"    Running total: {len(all_comments)} comments\n")

    if not all_comments:
        print("No new comments were scraped. Exiting.")
        return

    new_df = pd.DataFrame(all_comments)
    print(f"\nTotal new comments scraped: {len(new_df)}")

    # Show year distribution of scraped comments
    dates = pd.to_datetime(new_df["timestamp"], unit="s", errors="coerce")
    print("Year distribution of scraped comments:")
    print(dates.dt.year.value_counts().sort_index())

    # Combine with existing data
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.to_csv(raw_path, index=False)
    print(f"\nSaved combined dataset: {len(combined_df)} rows -> {raw_path}")

    # Final distribution
    all_dates = pd.to_datetime(combined_df["timestamp"], unit="s", errors="coerce")
    print("\nFinal year distribution:")
    print(all_dates.dt.year.value_counts().sort_index())


if __name__ == "__main__":
    main()
