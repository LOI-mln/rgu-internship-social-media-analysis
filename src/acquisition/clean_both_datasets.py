import pandas as pd
import os
import sys

# Add the src directory to the import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.common import count_words, scale_timestamps, WE_WORDS, THEM_WORDS, NEGATIVE_WORDS

def clean_youtube():
    print("Cleaning YouTube political dataset...")
    input_path = "data/raw/youtube_actual_politic.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    df = pd.read_csv(input_path)
    df = df.dropna(subset=['text', 'author'])
    
    # NLP features
    df['we_count'] = df['text'].apply(lambda x: count_words(x, WE_WORDS))
    df['them_count'] = df['text'].apply(lambda x: count_words(x, THEM_WORDS))
    df['negativity_score'] = df['text'].apply(lambda x: count_words(x, NEGATIVE_WORDS))
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
    df['we_count'] = df['full_text'].apply(lambda x: count_words(x, WE_WORDS))
    df['them_count'] = df['full_text'].apply(lambda x: count_words(x, THEM_WORDS))
    df['negativity_score'] = df['full_text'].apply(lambda x: count_words(x, NEGATIVE_WORDS))
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
    print("Cleaning YouTube political dataset...")
    input_path = "data/raw/youtube_actual_politic.csv"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    df = pd.read_csv(input_path)
    df = df.dropna(subset=['text', 'author'])
    
    # NLP features
    df['we_count'] = df['text'].apply(lambda x: count_words(x, WE_WORDS))
    df['them_count'] = df['text'].apply(lambda x: count_words(x, THEM_WORDS))
    df['negativity_score'] = df['text'].apply(lambda x: count_words(x, NEGATIVE_WORDS))
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
    df['we_count'] = df['full_text'].apply(lambda x: count_words(x, WE_WORDS))
    df['them_count'] = df['full_text'].apply(lambda x: count_words(x, THEM_WORDS))
    df['negativity_score'] = df['full_text'].apply(lambda x: count_words(x, NEGATIVE_WORDS))
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
