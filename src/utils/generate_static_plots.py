import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import os
from collections import Counter
import re

# Configuration
OUTPUT_DIR = "deliverables"
STATS_CSV = os.path.join(OUTPUT_DIR, "hashtag_centrality_stats.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📊 Chargement des statistiques...")
try:
    df = pd.read_csv(STATS_CSV)
except FileNotFoundError:
    print(f"❌ Erreur: Fichier {STATS_CSV} introuvable. Exécutez l'analyse de réseau en premier.")
    exit(1)

# 1. Bar Chart : Top 15 Hashtags les plus influents (PageRank)
print("📈 Génération du graphique d'influence (PageRank)...")
plt.figure(figsize=(10, 8))
top_pagerank = df.sort_values(by="pagerank", ascending=False).head(15)

# Style seaborn
sns.set_theme(style="whitegrid")
ax = sns.barplot(data=top_pagerank, x="pagerank", y="hashtag", palette="viridis")

plt.title("Top 15 Most Influential Hashtags (PageRank)", fontsize=16, fontweight='bold')
plt.xlabel("Influence Score (PageRank)", fontsize=12)
plt.ylabel("Hashtags", fontsize=12)

# Ajouter les valeurs sur les barres
for i, v in enumerate(top_pagerank["pagerank"]):
    ax.text(v + 0.001, i + 0.1, f"{v:.3f}", color='black', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "plot_top_influence.png"), dpi=300)
plt.close()

# 2. Bar Chart : Top 15 par Fréquence (pour comparer)
print("📈 Génération du graphique de fréquence...")
plt.figure(figsize=(10, 8))
top_freq = df.sort_values(by="frequency", ascending=False).head(15)

ax2 = sns.barplot(data=top_freq, x="frequency", y="hashtag", palette="magma")
plt.title("Top 15 Most Used Hashtags (Raw Frequency)", fontsize=16, fontweight='bold')
plt.xlabel("Number of Occurrences", fontsize=12)
plt.ylabel("Hashtags", fontsize=12)

for i, v in enumerate(top_freq["frequency"]):
    ax2.text(v + 1, i + 0.1, str(int(v)), color='black', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "plot_top_frequency.png"), dpi=300)
plt.close()

# 3. Tableau des Communautés (Top 3 hashtags par communauté principale)
print("🏘️ Génération du résumé des communautés narratives...")
# Garder les communautés avec le plus de hashtags
top_communities = df['community'].value_counts().head(5).index

community_summary = []
for com in top_communities:
    com_df = df[df['community'] == com].sort_values(by='pagerank', ascending=False)
    top_tags = ", ".join(com_df['hashtag'].head(5).tolist())
    size = len(com_df)
    community_summary.append({
        "Communauté (ID)": f"Cluster {com}",
        "Taille (Nb Hashtags)": size,
        "Hashtags Principaux": top_tags
    })

com_df_summary = pd.DataFrame(community_summary)
com_df_summary.to_csv(os.path.join(OUTPUT_DIR, "community_summary.csv"), index=False)

print("✅ Graphiques statiques générés avec succès dans le dossier 'deliverables' !")
