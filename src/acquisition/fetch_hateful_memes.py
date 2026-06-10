import os
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

print("🔴 Loading Hateful Memes Dataset from HuggingFace...")
# Load the dataset
# Use the training split, which contains 8,500 examples.
dataset = load_dataset('cs5242-hateful-memes/hateful-memes-data', split='train')

print(f"Dataset loaded! Total examples: {len(dataset)}")

# Create the directories
images_dir = "data/raw/hateful_memes_images"
os.makedirs(images_dir, exist_ok=True)

metadata = []

print("🔴 Extracting images and metadata...")
# Process a sample (for example, 2,000 memes) to keep local CLIP runs manageable,
# or process everything if desired. Use 2,000 for faster tests, but this can be changed.
max_examples = 2000
subset = dataset.select(range(min(max_examples, len(dataset))))

for example in tqdm(subset):
    meme_id = example.get('id', example.get('id', 'unknown'))
    text = example.get('text', '')
    label = example.get('label', 0) # 0: non-hateful, 1: hateful
    img = example.get('image', example.get('img', None)) # Try both 'image' and 'img'
    
    # Define the save path
    image_filename = f"{meme_id}.png"
    image_path = os.path.join(images_dir, image_filename)
    
    try:
        # If the dataset provides a PIL Image object
        if hasattr(img, 'save'):
            img.save(image_path)
        # If this is a file path string (rare, but possible with local or HF cache data)
        elif isinstance(img, str):
            import shutil
            shutil.copy(img, image_path)
    except Exception as e:
        print(f"Failed to save image {meme_id}: {e}")
        continue
        
    # Add to metadata
    metadata.append({
        "id": meme_id,
        "text": text,
        "label": label,
        "image_path": image_path
    })

# Save metadata as CSV
df = pd.DataFrame(metadata)
csv_path = "data/raw/hateful_memes.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Extraction complete! Saved {len(df)} memes.")
print(f"Metadata saved at: {csv_path}")
print(f"Images saved at: {images_dir}/")
