import pandas as pd
import os
import sys

# Add the src directory to the import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.common import count_words, WE_WORDS, THEM_WORDS, NEGATIVE_WORDS, map_comments_to_video_dates

def main():
    print("Processing youtube_actual_politic.csv...")
    input_path = "data/raw/youtube_actual_politic.csv"
    if not os.path.exists(input_path):
        print(f"Error: Raw file {input_path} not found.")
        return
        
    df = pd.read_csv(input_path)
    df = df.dropna(subset=['text', 'author'])
    
    # Calculate counts
    df['we_count'] = df['text'].apply(lambda x: count_words(x, WE_WORDS))
    df['them_count'] = df['text'].apply(lambda x: count_words(x, THEM_WORDS))
    df['negativity_score'] = df['text'].apply(lambda x: count_words(x, NEGATIVE_WORDS))
    df['lang'] = 'en'
    
    # Map comments to video upload dates for better temporal analysis
    df = map_comments_to_video_dates(df, 'video_id', 'timestamp')
    
    output_dir = "data/cleaned"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "youtube_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned YouTube dataset successfully saved to {output_path}. Total rows: {len(df)}")

if __name__ == "__main__":
    main()
