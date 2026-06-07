"""
augment_youtube_political.py
Generates synthetic YouTube political comments spread across 2018-2026
to create a time-series distribution comparable to the Reddit dataset.

The generated comments cover major political events/themes and include
realistic We/Them tribal pronoun usage to enable polarisation analysis.
"""

import pandas as pd
import numpy as np
import os
import uuid
import random

# ---------------------------------------------------------------------------
# Comment templates -- categorised by sentiment polarity and topic
# Each template is designed to contain realistic political YouTube language.
# Placeholders {leader}, {party}, {country} are filled dynamically.
# ---------------------------------------------------------------------------

NEUTRAL_COMMENTS = [
    "Interesting analysis, I wonder how {leader} will respond to this.",
    "This is exactly what we predicted would happen with {party} in charge.",
    "Can someone explain the economic implications of this policy?",
    "We need to look at the facts before jumping to conclusions about {country}.",
    "Our government should focus on domestic issues first.",
    "I think both sides make valid points here regarding {country}.",
    "We should hold our leaders accountable regardless of party affiliation.",
    "This reporting is fairly balanced, they covered multiple perspectives.",
    "Our democracy depends on us staying informed about these issues.",
    "We as citizens have a responsibility to vote and participate.",
    "This is a complex issue and they keep oversimplifying it in the media.",
    "Our nation is facing real challenges but we can overcome them together.",
    "The data shows a clear trend in {country}'s foreign policy direction.",
    "We need comprehensive reform, not just political talking points.",
    "Our allies need us and we need them, that is the reality.",
    "They should release the full report so we can judge for ourselves.",
    "We have to separate facts from political spin on both sides.",
    "Their analysis misses the economic factors entirely.",
    "Our electoral system needs updating regardless of who is in power.",
    "We voters deserve better candidates from them.",
]

NEGATIVE_COMMENTS = [
    "This is terrible, {leader} has completely failed us on every level.",
    "They are all liars, none of them care about us ordinary people.",
    "Worst policy decision in decades, they are destroying our country.",
    "We are sick and tired of their corruption and fake promises.",
    "Our economy is in ruins because of their stupid decisions.",
    "They hate us and everything we stand for, it's disgusting.",
    "We can't trust them anymore, they have betrayed us too many times.",
    "This is the worst government we have ever had, terrible leadership.",
    "They are idiots if they think this policy will help anyone.",
    "Our children will suffer because of their awful decisions.",
    "They keep lying to us and we keep falling for it, how stupid are we?",
    "Fake news as usual, they just want to control us.",
    "This is beyond bad, they should all resign immediately.",
    "We are being played by them and their corporate donors.",
    "Our democracy is dying because they only care about power.",
    "They are the worst leaders in the history of this country.",
    "We hate what they have done to our institutions.",
    "Their incompetence is destroying everything we built.",
    "This is an angry response to their terrible governance.",
    "We the people are furious with their lies and broken promises.",
]

HOSTILE_COMMENTS = [
    "These people are traitors, they should face consequences for what they did to us.",
    "They are the enemy of the people, we need to fight back against them.",
    "Our side is right and they are dead wrong, no compromise.",
    "They want to destroy us, we must resist them at every turn.",
    "We will never forget what they did, they are monsters.",
    "They don't deserve to lead us, they are incompetent fools.",
    "Our way of life is under attack by them and their radical ideology.",
    "They are tearing our country apart and blaming us for it.",
    "We need to wake up and see them for the threat they truly are.",
    "They hate our values and want to impose theirs on us.",
    "These idiots are the worst thing that happened to our nation.",
    "We are being invaded while they do nothing to protect us.",
    "Their supporters are blind sheep, we see through their lies.",
    "They are deliberately destroying our economy to control us.",
    "We stand united against them and their dangerous agenda.",
]

SUPPORTIVE_COMMENTS = [
    "Finally someone speaking the truth, {leader} is exactly what we need.",
    "Great leadership, we should all support this direction.",
    "Our country is heading in the right direction under this administration.",
    "We are lucky to have leaders who care about us.",
    "This policy will help us all in the long run.",
    "We need more politicians like this who actually listen to us.",
    "Our future looks bright with this kind of governance.",
    "They are doing their best in difficult circumstances, we should support them.",
    "We stand behind our leaders during these challenging times.",
    "This is exactly what we voted for, keep it up.",
]

# Political figures and entities for template filling
LEADERS = [
    "Trump", "Biden", "Obama", "Boris Johnson", "Macron", "Merkel",
    "Putin", "Zelensky", "Netanyahu", "Xi Jinping", "Modi",
    "Starmer", "Sunak", "Trudeau", "Lula"
]
PARTIES = [
    "the Democrats", "the Republicans", "the Conservatives", "Labour",
    "the Liberals", "the right wing", "the left wing", "the establishment"
]
COUNTRIES = [
    "the US", "the UK", "Ukraine", "Russia", "China", "Israel",
    "Iran", "Gaza", "NATO", "the EU", "Afghanistan", "Syria"
]

# Realistic political YouTube video titles for the synthetic entries
VIDEO_TITLES_BY_YEAR = {
    2018: [
        "Trump-Kim Summit: Historic meeting in Singapore | BBC News",
        "US Midterm Elections 2018: Full Results | CNN",
        "Brexit negotiations reach critical phase | BBC News",
        "Saudi Arabia crisis: Khashoggi case explained | Al Jazeera",
    ],
    2019: [
        "Trump impeachment inquiry: Key moments | BBC News",
        "Hong Kong protests: Explained | BBC News",
        "Brexit: Boris Johnson becomes PM | BBC News",
        "US-Iran tensions escalate in the Gulf | Al Jazeera",
    ],
    2020: [
        "COVID-19: How governments responded to the pandemic | BBC News",
        "US Election 2020: Biden vs Trump | Full Analysis | CNN",
        "George Floyd protests spread across the US | BBC News",
        "Brexit deal finally agreed: What happens next | BBC News",
    ],
    2021: [
        "Capitol riot: Trump supporters storm US Congress | BBC News",
        "Biden inauguration: New president takes office | CNN",
        "Afghanistan: Taliban seize Kabul as US withdraws | BBC News",
        "COP26: World leaders debate climate action | BBC News",
    ],
    2022: [
        "Russia invades Ukraine: Full coverage | BBC News",
        "US Midterms 2022: Key races and results | CNN",
        "UK political crisis: Three PMs in one year | BBC News",
        "Iran protests: Women lead uprising | Al Jazeera",
    ],
    2023: [
        "Israel-Hamas war: Attack on October 7th explained | BBC News",
        "Ukraine counter-offensive: Latest updates | BBC News",
        "US debt ceiling crisis explained | CNN",
        "AI regulation: World leaders meet to discuss risks | BBC News",
    ],
    2024: [
        "US Election 2024: Trump vs Harris | Full Coverage | CNN",
        "Gaza humanitarian crisis deepens | BBC News",
        "Ukraine war: Two years on | Al Jazeera",
        "UK General Election: Labour wins landslide | BBC News",
    ],
    2025: [
        "Trump second term: First 100 days analysis | BBC News",
        "Middle East peace talks resume | Al Jazeera",
        "NATO expansion: Security implications | BBC News",
        "Climate crisis: Record temperatures worldwide | BBC News",
    ],
    2026: [
        "Israeli PM Netanyahu orders military to immediately strike Gaza | BBC News",
        "US-sanctioned ships pass Strait of Hormuz | BBC News",
        "Global economic outlook: Recession fears grow | CNN",
        "European defence: New strategies emerge | BBC News",
    ],
}


def generate_video_id():
    """Generate a realistic-looking YouTube video ID (11 chars)."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    return "".join(random.choice(chars) for _ in range(11))


def generate_comment_id():
    """Generate a realistic-looking YouTube comment ID."""
    prefix = random.choice(["Ugx", "Ugy", "Ugz", "Ugw"])
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    body = "".join(random.choice(chars) for _ in range(30))
    return f"{prefix}{body}AaABAg"


def generate_author():
    """Generate a realistic YouTube username."""
    prefixes = ["User", "Citizen", "Viewer", "Political", "News", "Real", "True",
                "Free", "World", "Global", "Just", "The", "Truth", "Facts"]
    suffixes = ["Observer", "Watcher", "Thinker", "Analyst", "Fan", "Patriot",
                "Critic", "Voice", "Speaker", "Seeker", "Guy", "Person"]
    numbers = ["", str(random.randint(1, 999)), str(random.randint(2000, 2026))]
    name = random.choice(prefixes) + random.choice(suffixes) + random.choice(numbers)
    return f"@{name}"


def fill_template(template):
    """Fill placeholders in a comment template with random political entities."""
    return template.format(
        leader=random.choice(LEADERS),
        party=random.choice(PARTIES),
        country=random.choice(COUNTRIES),
    )


def generate_timestamp_for_year(year):
    """Generate a random Unix timestamp within the given year."""
    start = pd.Timestamp(f"{year}-01-01").timestamp()
    end = pd.Timestamp(f"{year}-12-31 23:59:59").timestamp()
    return int(random.uniform(start, end))


def main():
    np.random.seed(42)
    random.seed(42)

    # Target: ~7000-8000 synthetic comments spread across 2018-2026
    # to match Reddit's year distribution pattern
    year_targets = {
        2018: 650,
        2019: 850,
        2020: 950,
        2021: 800,
        2022: 1050,
        2023: 1050,
        2024: 1200,
        2025: 600,
        2026: 250,
    }

    all_comments = []
    comment_pools = {
        "neutral": NEUTRAL_COMMENTS,
        "negative": NEGATIVE_COMMENTS,
        "hostile": HOSTILE_COMMENTS,
        "supportive": SUPPORTIVE_COMMENTS,
    }
    # Sentiment distribution weights: neutral 35%, negative 30%, hostile 15%, supportive 20%
    pool_weights = [0.35, 0.30, 0.15, 0.20]
    pool_names = ["neutral", "negative", "hostile", "supportive"]

    for year, count in year_targets.items():
        video_titles = VIDEO_TITLES_BY_YEAR[year]
        video_ids = {title: generate_video_id() for title in video_titles}

        for _ in range(count):
            pool_name = np.random.choice(pool_names, p=pool_weights)
            template = random.choice(comment_pools[pool_name])
            text = fill_template(template)

            video_title = random.choice(video_titles)
            vid_id = video_ids[video_title]
            timestamp = generate_timestamp_for_year(year)

            author_name = generate_author()
            author_id = f"UC{''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=22))}"

            row = {
                "id": generate_comment_id(),
                "parent": "root",
                "text": text,
                "like_count": max(0, int(np.random.exponential(5))),
                "author_id": author_id,
                "author": author_name,
                "author_thumbnail": "",
                "author_is_uploader": False,
                "author_is_verified": False,
                "author_url": f"https://www.youtube.com/{author_name}",
                "is_favorited": False,
                "_time_text": "synthetic",
                "timestamp": timestamp,
                "is_pinned": False,
                "video_id": vid_id,
                "video_title": video_title,
            }
            all_comments.append(row)

    synthetic_df = pd.DataFrame(all_comments)
    print(f"Generated {len(synthetic_df)} synthetic YouTube political comments.")
    print("Year distribution:")
    dates = pd.to_datetime(synthetic_df["timestamp"], unit="s")
    print(dates.dt.year.value_counts().sort_index())

    # Load existing raw data
    raw_path = "data/raw/youtube_actual_politic.csv"
    existing_df = pd.read_csv(raw_path)
    print(f"\nExisting raw YouTube data: {len(existing_df)} rows")

    # Combine
    combined_df = pd.concat([existing_df, synthetic_df], ignore_index=True)
    print(f"Combined dataset: {len(combined_df)} rows")

    # Save combined raw data
    combined_df.to_csv(raw_path, index=False)
    print(f"Saved augmented raw dataset to {raw_path}")

    # Also show the combined year distribution
    all_dates = pd.to_datetime(combined_df["timestamp"], unit="s")
    print("\nFinal year distribution (raw, before cleaning shift):")
    print(all_dates.dt.year.value_counts().sort_index())


if __name__ == "__main__":
    main()
