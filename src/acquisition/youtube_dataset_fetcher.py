import subprocess, json, os, pandas as pd

# 1. Scrape BBC News videos about Gaza
os.makedirs("data", exist_ok=True)

urls = [
    "https://www.youtube.com/watch?v=p9ONnNFdNtQ",
    "https://www.youtube.com/watch?v=IA8YL_Datm0",
    "https://www.youtube.com/watch?v=2xwXLWhLYx0",
    "https://www.youtube.com/watch?v=Jakyor8TUB4",
    "https://www.youtube.com/watch?v=_GpMnIdnYr4",
    "https://www.youtube.com/watch?v=u8C6l9sa_fM",
    "https://www.youtube.com/watch?v=E7FLymwDCk8",
    "https://www.youtube.com/watch?v=MJqFLSpnKoU",
    "https://www.youtube.com/watch?v=-pMuAYM8EIc",
    "https://www.youtube.com/watch?v=51BvCUpcBTc"
]

for url in urls:
    subprocess.run([
        "yt-dlp",
        "--write-comments",
        "--skip-download",
        "--output", "data/raw/%(id)s.%(ext)s",
        url
    ])

# 2. Convert to CSV
all_comments = []

for file in os.listdir("data/raw"):
    if file.endswith(".info.json"):
        with open(f"data/raw/{file}") as f:
            data = json.load(f)
        video_id = data.get("id")
        title = data.get("title")
        for c in data.get("comments", []):
            c["video_id"] = video_id
            c["video_title"] = title
            all_comments.append(c)

df = pd.DataFrame(all_comments)
df.to_csv("data/raw/youtube_bbc_gaza.csv", index=False)
print(f"✅ {len(df)} comments saved to data/raw/youtube_bbc_gaza.csv")
