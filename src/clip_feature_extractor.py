import os
import torch
import pandas as pd
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch.nn.functional as F
from tqdm import tqdm

print("🔴 Task 2: Loading CLIP model (openai/clip-vit-base-patch32)...")
device = "cuda" if torch.cuda.is_available() else "cpu"
# For Mac M1/M2 (Apple Silicon), 'mps' is available for hardware acceleration
if torch.backends.mps.is_available():
    device = "mps"

model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)
print(f"✅ CLIP model loaded on device: {device}")

# Load the dataset
print("🔴 Loading Hateful Memes metadata...")
df = pd.read_csv("data/raw/hateful_memes.csv")

# Task 5: Zero-Shot label definitions for meme classification
zero_shot_labels = ["a meme about us (in-group)", "a meme about them (out-group)", "a neutral image"]

similarities = []
visual_predictions = []

print("🔴 Tasks 3, 4 & 5: Feature extraction and similarity calculation...")
for index, row in tqdm(df.iterrows(), total=len(df)):
    image_path = row['image_path']
    text = str(row['text'])
    
    if not os.path.exists(image_path):
        similarities.append(None)
        visual_predictions.append(None)
        continue
        
    try:
        image = Image.open(image_path).convert("RGB")
        
        # 1. Cross-processing (Meme Image + Text) for Cosine Similarity
        inputs = processor(text=[text], images=image, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
            
            # Normalized embeddings
            image_embeds = outputs.image_embeds
            text_embeds = outputs.text_embeds
            
            # Task 4: Cosine Similarity between embedded text and the image itself
            cos_sim = F.cosine_similarity(image_embeds, text_embeds).item()
            similarities.append(cos_sim)
            
            # 2. Task 5: Zero-Shot classification of the image alone
            zero_shot_inputs = processor(text=zero_shot_labels, images=image, return_tensors="pt", padding=True).to(device)
            zs_outputs = model(**zero_shot_inputs)
            
            # Probabilities on the 3 labels (softmax)
            logits_per_image = zs_outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
            
            # Get the winning label
            best_label_idx = probs.argmax()
            visual_predictions.append(zero_shot_labels[best_label_idx])
            
    except Exception as e:
        print(f"Error with {image_path}: {e}")
        similarities.append(None)
        visual_predictions.append(None)

# Update the DataFrame
df['clip_similarity'] = similarities
df['visual_label'] = visual_predictions

# Export the result
output_path = "data/cleaned/hateful_memes_clip_scored.csv"
os.makedirs("data/cleaned", exist_ok=True)
df.to_csv(output_path, index=False)

print(f"✅ Tasks completed! Dataset exported to: {output_path}")
print(df[['text', 'clip_similarity', 'visual_label']].head(10))
