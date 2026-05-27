import os
import pandas as pd
from datasets import load_dataset

print("🔴 Loading Hateful Memes metadata from HuggingFace...")

# Charger les métadonnées (texte + étiquette) à partir de la version publique de neuralcatcher
# Note : Cette version ne contient que les chemins des images, pas les images elles-mêmes !
dataset = load_dataset('neuralcatcher/hateful_memes', split='train')

print(f"✅ {len(dataset)} metadata entries successfully loaded!")

# Sauvegarder les textes et les étiquettes
metadata = []
for example in dataset:
    metadata.append({
        "id": example['id'],
        "text": example['text'],
        "label": example['label'], # 1 = Haineux, 0 = Non haineux
        "image_path": example['img'] # Juste le nom de fichier (ex., 'img/12345.png')
    })

df = pd.DataFrame(metadata)
os.makedirs("data/raw", exist_ok=True)
csv_path = "data/raw/hateful_memes_metadata.csv"
df.to_csv(csv_path, index=False)

print(f"✅ CSV file saved to: {csv_path}")
print("⚠️ WARNING: The images themselves were not downloaded due to Meta's licensing.")
print("You must manually download them from DrivenData.org and place them in a data/raw/img/ folder")
