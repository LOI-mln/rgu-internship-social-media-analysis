import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("🔴 Task 6: Evaluation of We/Them alignment...")

# Charger le jeu de données scoré
try:
    df = pd.read_csv("data/cleaned/hateful_memes_clip_scored.csv")
except FileNotFoundError:
    print("Error: The file hateful_memes_clip_scored.csv was not found.")
    exit(1)

# Créer le dossier pour les figures
os.makedirs("docs/figures", exist_ok=True)

# Définir le style
sns.set_theme(style="whitegrid")

# 1. Boîte à moustaches : Similarité cosinus par toxicité (Haineux vs Non haineux)
plt.figure(figsize=(8, 6))
sns.boxplot(x='label', y='clip_similarity', data=df, hue='label', palette='Set2', legend=False)
plt.title("Text/Image Alignment by Meme Toxicity", fontsize=14)
plt.xlabel("Label (0: Non-Hateful, 1: Hateful)", fontsize=12)
plt.ylabel("Cosine Similarity (CLIP)", fontsize=12)
plt.tight_layout()
plt.savefig("docs/figures/cosine_similarity_by_label.png", dpi=300)
plt.close()

# 2. Graphique à barres : Distribution des étiquettes visuelles "Nous/Eux"
plt.figure(figsize=(10, 6))
ax = sns.countplot(y='visual_label', data=df, hue='visual_label', palette='pastel', legend=False)
plt.title("Visual Prediction (Zero-Shot) of Memes", fontsize=14)
plt.xlabel("Number of Memes", fontsize=12)
plt.ylabel("Visual Category (We/Them)", fontsize=12)
plt.tight_layout()
plt.savefig("docs/figures/visual_predictions_distribution.png", dpi=300)
plt.close()

# 3. Métriques globales
hateful_mean_sim = df[df['label'] == 1]['clip_similarity'].mean()
nonhateful_mean_sim = df[df['label'] == 0]['clip_similarity'].mean()

print(f"✅ Evaluation complete!")
print(f"📊 Mean alignment score for Non-Hateful memes: {nonhateful_mean_sim:.4f}")
print(f"📊 Mean alignment score for Hateful memes    : {hateful_mean_sim:.4f}")
print("\nThe graphs have been generated and saved in the 'docs/figures/' folder.")
