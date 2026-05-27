import os
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm

print("🔴 Loading Hateful Memes Dataset from HuggingFace...")
# Charger le jeu de données
# Nous prenons la partition d'entraînement. 8500 exemples.
dataset = load_dataset('cs5242-hateful-memes/hateful-memes-data', split='train')

print(f"Dataset loaded! Total examples: {len(dataset)}")

# Créer les répertoires
images_dir = "data/raw/hateful_memes_images"
os.makedirs(images_dir, exist_ok=True)

metadata = []

print("🔴 Extracting images and metadata...")
# Traiter un échantillon (ex., 2000 mèmes) pour garder les choses gérables pour CLIP local, 
# ou traiter tout si désiré. Faisons-en 2000 pour des tests plus rapides, mais vous pouvez le changer.
max_examples = 2000
subset = dataset.select(range(min(max_examples, len(dataset))))

for example in tqdm(subset):
    meme_id = example.get('id', example.get('id', 'unknown'))
    text = example.get('text', '')
    label = example.get('label', 0) # 0: non haineux, 1: haineux
    img = example.get('image', example.get('img', None)) # Essayer à la fois 'image' et 'img'
    
    # Définir le chemin de sauvegarde
    image_filename = f"{meme_id}.png"
    image_path = os.path.join(images_dir, image_filename)
    
    try:
        # Si le jeu de données fournit un objet PIL Image
        if hasattr(img, 'save'):
            img.save(image_path)
        # Si c'est une chaîne de chemin de fichier (rare mais arrive si local ou cache hf)
        elif isinstance(img, str):
            import shutil
            shutil.copy(img, image_path)
    except Exception as e:
        print(f"Failed to save image {meme_id}: {e}")
        continue
        
    # Ajouter aux métadonnées
    metadata.append({
        "id": meme_id,
        "text": text,
        "label": label,
        "image_path": image_path
    })

# Sauvegarder les métadonnées en CSV
df = pd.DataFrame(metadata)
csv_path = "data/raw/hateful_memes.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Extraction complete! Saved {len(df)} memes.")
print(f"Metadata saved at: {csv_path}")
print(f"Images saved at: {images_dir}/")
