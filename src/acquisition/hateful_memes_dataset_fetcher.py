import os
import pandas as pd
from datasets import load_dataset

print("🔴 Loading Hateful Memes metadata from HuggingFace...")

# Load metadata (text + label) from the public neuralcatcher version
# Note: this version only contains image paths, not the images themselves.
dataset = load_dataset('neuralcatcher/hateful_memes', split='train')

print(f"✅ {len(dataset)} metadata entries successfully loaded!")

# Save texts and labels
metadata = []
for example in dataset:
    metadata.append({
        "id": example['id'],
        "text": example['text'],
        "label": example['label'], # 1 = Hateful, 0 = Non-hateful
        "image_path": example['img'] # Only the filename (for example, 'img/12345.png')
    })

df = pd.DataFrame(metadata)
os.makedirs("data/raw", exist_ok=True)
csv_path = "data/raw/hateful_memes_metadata.csv"
df.to_csv(csv_path, index=False)

print(f"✅ CSV file saved to: {csv_path}")
print("⚠️ WARNING: The images themselves were not downloaded due to Meta's licensing.")
print("You must manually download them from DrivenData.org and place them in a data/raw/img/ folder")
