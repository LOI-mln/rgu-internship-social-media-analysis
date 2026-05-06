import os
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

print("🔴 Loading Hateful Memes Dataset from HuggingFace...")
# Load the dataset
# We take the train split. 8500 examples.
dataset = load_dataset('cs5242-hateful-memes/hateful-memes-data', split='train')

print(f"Dataset loaded! Total examples: {len(dataset)}")

# Create directories
images_dir = "data/raw/hateful_memes_images"
os.makedirs(images_dir, exist_ok=True)

metadata = []

print("🔴 Extracting images and metadata...")
# Process a sample (e.g., 2000 memes) to keep things manageable for local CLIP, 
# or process all if desired. Let's do 2000 for faster testing, but you can change it.
max_examples = 2000
subset = dataset.select(range(min(max_examples, len(dataset))))

for example in tqdm(subset):
    meme_id = example.get('id', example.get('id', 'unknown'))
    text = example.get('text', '')
    label = example.get('label', 0) # 0: non-hateful, 1: hateful
    img = example.get('image', example.get('img', None)) # Try both 'image' and 'img'
    
    # Define save path
    image_filename = f"{meme_id}.png"
    image_path = os.path.join(images_dir, image_filename)
    
    try:
        # If the dataset provides a PIL Image object
        if hasattr(img, 'save'):
            img.save(image_path)
        # If it's a file path string (rare but happens if local or hf cache)
        elif isinstance(img, str):
            import shutil
            shutil.copy(img, image_path)
    except Exception as e:
        print(f"Failed to save image {meme_id}: {e}")
        continue
        
    # Append to metadata
    metadata.append({
        "id": meme_id,
        "text": text,
        "label": label,
        "image_path": image_path
    })

# Save metadata to CSV
df = pd.DataFrame(metadata)
csv_path = "data/raw/hateful_memes.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Extraction complete! Saved {len(df)} memes.")
print(f"Metadata saved at: {csv_path}")
print(f"Images saved at: {images_dir}/")
