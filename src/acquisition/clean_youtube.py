import pandas as pd
import re
import os

negative_words = ['bad', 'worst', 'hate', 'stupid', 'idiot', 'fake', 'liar', 'worse', 'terrible', 'awful', 'angry']
we_words = ['we', 'us', 'our', 'ours', 'ourselves']
them_words = ['they', 'them', 'their', 'theirs', 'themselves']

def count_words(text, word_list):
    text = str(text).lower()
    return sum(len(re.findall(r'\b' + word + r'\b', text)) for word in word_list)

def main():
    print("Processing youtube_actual_politic.csv...")
    input_path = "data/raw/youtube_actual_politic.csv"
    if not os.path.exists(input_path):
        print(f"Error: Raw file {input_path} not found.")
        return
        
    df = pd.read_csv(input_path)
    df = df.dropna(subset=['text', 'author'])
    
    # Calculate counts
    df['we_count'] = df['text'].apply(lambda x: count_words(x, we_words))
    df['them_count'] = df['text'].apply(lambda x: count_words(x, them_words))
    df['negativity_score'] = df['text'].apply(lambda x: count_words(x, negative_words))
    df['lang'] = 'en'
    
    # Video upload date mapping: assigns each comment the upload date of
    # its source video. This replaces the approximate comment timestamps
    # returned by yt-dlp (which are derived from relative text such as
    # '4 years ago' and cluster on a single date per video).
    VIDEO_UPLOAD_DATES = {
        # Original dataset videos (2025-2026)
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
        # Scraped political videos (2018-2024)
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
    
    # Replace comment timestamps with video upload dates for temporal analysis
    df['video_upload_date'] = df['video_id'].map(VIDEO_UPLOAD_DATES)
    mapped_count = df['video_upload_date'].notna().sum()
    if mapped_count > 0:
        upload_ts = pd.to_datetime(df['video_upload_date'], errors='coerce')
        mask = upload_ts.notna()
        df.loc[mask, 'timestamp'] = upload_ts[mask].astype(int) // 10**9
        print(f"  Mapped {mapped_count}/{len(df)} comments to video upload dates.")
    df = df.drop(columns=['video_upload_date'], errors='ignore')
    
    output_dir = "data/cleaned"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "youtube_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned YouTube dataset successfully saved to {output_path}. Total rows: {len(df)}")

if __name__ == "__main__":
    main()
