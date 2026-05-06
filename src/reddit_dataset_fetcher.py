from datasets import load_dataset
import pandas as pd

dataset = load_dataset("mo-mittal/reddit_political_subs", trust_remote_code=True)
df = dataset['train'].to_pandas()
df.to_csv("data/raw/reddit_political.csv", index=False)
print(f"Saved! {len(df)} rows, columns: {df.columns.tolist()}")