"""
scrape_youtube_political_v2.py
Scrapes real YouTube comments from verified political video IDs
found via yt-dlp search. Covers 2018-2024 political events.
"""

import subprocess
import json
import pandas as pd
import os
import sys

# Verified real YouTube video IDs from yt-dlp search results
# Grouped by approximate year/topic for documentation purposes
POLITICAL_VIDEOS = [
    # 2018 - Trump immigration policy, DACA
    "BHe0LkMsV_g",  # Future of DACA and immigration reform
    "4MewVLDVTX8",  # Trump defends immigration policy
    "4KIpnPapquY",  # Trump at the UN general assembly - BBC News
    "2Cm8Su-bbmw",  # Donald Trump tells Nato allies to pay up - BBC News

    # 2019 - Brexit debate, Trump impeachment
    "eXBV8YU2TeI",  # Brexit "next steps" debate: 27 February 2019
    "eidqxI2l_iA",  # Super Saturday: MPs debate Boris Johnson's deal
    "VwCxyWcBSx8",  # President Trump on Impeachment Hearing
    "6XcXaS55Qpk",  # Trump impeachment hearing testimony
    "bGkr9n6DwSg",  # Counsel Goldman's opening presentation impeachment

    # 2020 - COVID lockdown, US election debate, George Floyd
    "LlJIwTd9fqI",  # Boris Johnson announces complete UK lockdown
    "vJycNmK7KPk",  # Coronavirus: PM Boris Johnson lockdown statement BBC
    "CweqW7Pzxz8",  # First presidential debate Trump vs Biden 2020
    "wW1lY5jFNcQ",  # First 2020 Presidential Debate full
    "u3v2VQEa--w",  # George Floyd protests: Thousands rally in London
    "YfoEisa0DEc",  # Protests and political fallout after George Floyd

    # 2021 - Capitol riot, Afghanistan withdrawal
    "jWJVMoe7OY0",  # Day of Rage: How Trump Supporters Took the Capitol (NYT)
    "M4B8FYQq6rM",  # Timeline of the Capitol Attack January 6
    "hMSK0lI_shA",  # Biden announces full withdrawal from Afghanistan
    "CS1IdVC-n7Y",  # Biden defended Afghanistan withdrawal

    # 2022 - Russia/Ukraine war, Liz Truss resignation
    "MVu8QbxafJE",  # Putin's war on Ukraine explained (Vox)
    "icRHnVKyrcw",  # Ukraine 2022: Attack On Freedom documentary
    "b-9czRep8hA",  # Liz Truss resigns as PM - full statement
    "1kNSoNrthKg",  # Why did Liz Truss's time as UK PM end - BBC

    # 2023 - Israel-Hamas war October 7
    "Ulg-96K3qMc",  # Hamas October 7 Attack Minute-by-Minute
    "PcQaG4sC9BM",  # NBC Special Report: Israel declares war
    "Fp-QHzpsjWo",  # Israel-Hamas War 2023 Summarized

    # 2024 - US Election Trump vs Harris, Gaza ceasefire
    "2ec4Oa2L1fo",  # Harris v Trump debate highlights
    "MUYepJ5fNp8",  # Key moments Trump Harris debate BBC
    "2tIXGym1I-s",  # Netanyahu tears up Gaza ceasefire
    "B9C7X8dPJtg",  # 40-day ceasefire in Gaza negotiations
]


def scrape_comments(video_id, max_comments=500):
    """Use yt-dlp to extract comments from a YouTube video."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"  Scraping: {url}")
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-comments",
        "--dump-json",
        "--extractor-args", f"youtube:max_comments={max_comments},all,100,100",
        "--no-warnings",
        url,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if result.returncode != 0:
            err = result.stderr[:300] if result.stderr else "unknown error"
            print(f"    [FAIL] {err}")
            return []

        data = json.loads(result.stdout)
        comments_raw = data.get("comments") or []
        video_title = data.get("title", "")
        upload_date = data.get("upload_date", "")

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
        print(f"    OK: {len(comments)} comments | \"{video_title}\" (uploaded {upload_date})")
        return comments

    except subprocess.TimeoutExpired:
        print(f"    [FAIL] Timeout after 180s")
        return []
    except json.JSONDecodeError as e:
        print(f"    [FAIL] JSON parse error: {e}")
        return []
    except Exception as e:
        print(f"    [FAIL] {type(e).__name__}: {e}")
        return []


def main():
    raw_path = "data/raw/youtube_actual_politic.csv"
    existing_df = pd.read_csv(raw_path)
    existing_video_ids = set(existing_df["video_id"].unique())
    print(f"Existing dataset: {len(existing_df)} rows, {len(existing_video_ids)} unique videos\n")

    # Filter out videos already in the dataset
    videos_to_scrape = [v for v in POLITICAL_VIDEOS if v not in existing_video_ids]
    print(f"Videos to scrape: {len(videos_to_scrape)} (skipping {len(POLITICAL_VIDEOS) - len(videos_to_scrape)} already present)\n")

    all_comments = []
    for i, vid_id in enumerate(videos_to_scrape, 1):
        print(f"[{i}/{len(videos_to_scrape)}]")
        comments = scrape_comments(vid_id, max_comments=500)
        all_comments.extend(comments)
        print(f"    Running total: {len(all_comments)} comments\n")

    if not all_comments:
        print("No new comments scraped.")
        return

    new_df = pd.DataFrame(all_comments)
    print(f"\n{'='*60}")
    print(f"Total new comments scraped: {len(new_df)}")

    # Year distribution
    dates = pd.to_datetime(new_df["timestamp"], unit="s", errors="coerce")
    print("\nYear distribution of NEW comments:")
    print(dates.dt.year.value_counts().sort_index())

    # Video summary
    print("\nComments per video:")
    for vid_id in new_df["video_id"].unique():
        subset = new_df[new_df["video_id"] == vid_id]
        title = subset["video_title"].iloc[0]
        print(f"  {vid_id}: {len(subset):>4} comments | {title}")

    # Combine
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.to_csv(raw_path, index=False)
    print(f"\nSaved combined: {len(combined_df)} rows -> {raw_path}")

    # Final distribution
    all_dates = pd.to_datetime(combined_df["timestamp"], unit="s", errors="coerce")
    print("\nFinal year distribution (all data):")
    print(all_dates.dt.year.value_counts().sort_index())


if __name__ == "__main__":
    main()
