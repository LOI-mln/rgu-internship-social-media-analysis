import pandas as pd
import re
import os

negative_words = ['bad', 'worst', 'hate', 'stupid', 'idiot', 'fake', 'liar', 'worse', 'terrible', 'awful', 'angry']
we_words = ['we', 'us', 'our', 'ours', 'ourselves']
them_words = ['they', 'them', 'their', 'theirs', 'themselves']

def count_words(text, word_list):
    text = str(text).lower()
    return sum(len(re.findall(r'\b' + word + r'\b', text)) for word in word_list)

def scale_timestamps(series_or_datetime, target_start='2018-01-01 00:00:00', target_end='2026-05-31 23:59:59'):
    dt_series = pd.to_datetime(series_or_datetime, errors='coerce')
    min_val = dt_series.min()
    max_val = dt_series.max()
    
    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return dt_series
        
    target_min = pd.to_datetime(target_start)
    target_max = pd.to_datetime(target_end)
    
    scaled_series = target_min + (dt_series - min_val) / (max_val - min_val) * (target_max - target_min)
    return scaled_series

def clean_youtube():
    print("Cleaning YouTube political dataset...")
    input_path = "data/raw/youtube_actual_politic.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    df = pd.read_csv(input_path)
    df = df.dropna(subset=['text', 'author'])
    
    # NLP features
    df['we_count'] = df['text'].apply(lambda x: count_words(x, we_words))
    df['them_count'] = df['text'].apply(lambda x: count_words(x, them_words))
    df['negativity_score'] = df['text'].apply(lambda x: count_words(x, negative_words))
    df['lang'] = 'en'
    
    # Timestamp alignment: scale timestamps to 2018-2026 range
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    df = df.dropna(subset=['datetime'])
    df['datetime_scaled'] = scale_timestamps(df['datetime'])
    df['timestamp'] = df['datetime_scaled'].astype('int64') // 10**9
    df = df.drop(columns=['datetime', 'datetime_scaled'])
    
    output_path = "data/cleaned/youtube_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"YouTube cleaning complete: saved {len(df)} rows to {output_path}")

def clean_reddit():
    print("Cleaning Reddit political dataset...")
    input_path = "data/raw/reddit_political.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    df = pd.read_csv(input_path)
    
    # Compile full_text
    df['full_text'] = df['title'].fillna('') + ' ' + df['selftext'].fillna('')
    df = df.drop_duplicates(subset=['full_text'])
    df = df.dropna(subset=['full_text', 'author'])
    
    # NLP features
    df['we_count'] = df['full_text'].apply(lambda x: count_words(x, we_words))
    df['them_count'] = df['full_text'].apply(lambda x: count_words(x, them_words))
    df['negativity_score'] = df['full_text'].apply(lambda x: count_words(x, negative_words))
    df['lang'] = 'en'
    
    # Timestamp alignment: scale timestamps to 2018-2026 range
    df['created_utc'] = pd.to_datetime(df['created_utc'], errors='coerce')
    df = df.dropna(subset=['created_utc'])
    df['created_utc'] = scale_timestamps(df['created_utc'])
    
    # Convert back to standard string format
    df['created_utc'] = df['created_utc'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    output_path = "data/cleaned/reddit_political_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"Reddit cleaning complete: saved {len(df)} rows to {output_path}")

def main():
    os.makedirs("data/cleaned", exist_ok=True)
    clean_youtube()
    clean_reddit()
    print("Both datasets cleaned and aligned successfully.")

if __name__ == "__main__":
    main()

