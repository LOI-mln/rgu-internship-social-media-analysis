# 📊 Rapport de Travaux - Semaine 4

Ce document détaille l'implémentation des analyses de réseau pour le projet d'analyse des médias sociaux (Reddit et YouTube).

## 🛠️ Travaux réalisés

### 1. Construction de la Matrice de Co-occurrence
Nous avons mis en place un extracteur de hashtags qui analyse le texte des publications Reddit et des commentaires YouTube.
- **Fenêtre d'analyse** : 20 jetons (tokens). Cela signifie que deux hashtags sont considérés comme co-occurrents s'ils apparaissent à moins de 20 mots l'un de l'autre dans le même texte.
- **Données sources** : `reddit_political_cleaned.csv` et `youtube_cleaned.csv`.

### 2. Création du Graphe
À l'aide de la bibliothèque **NetworkX**, nous avons construit un graphe non orienté pondéré :
- **Nœuds** : Les hashtags uniques.
- **Arêtes** : Lien entre deux hashtags s'ils co-occurrent.
- **Poids** : Nombre de co-occurrences observées.

### 3. Analyse des Métriques de Centralité
Les métriques suivantes ont été calculées pour identifier les hashtags les plus influents :
- **Centralité de Degré** : Mesure le nombre de connexions directes d'un hashtag.
- **Centralité d'Intermédiarité (Betweenness)** : Identifie les hashtags qui servent de "ponts" entre différents groupes de discussion.
- **PageRank** : Évalue l'importance relative d'un hashtag au sein de la structure globale du réseau.

### 4. Détection de Communautés
Nous avons appliqué l'algorithme de **Louvain** pour identifier des "clusters" narratifs. Ces groupes représentent des thèmes ou des opinions qui ont tendance à être discutés ensemble.

---

## 📦 Livrables Produits

### 📈 Statistiques de Centralité
Un fichier CSV contenant l'ensemble des métriques calculées.
- **Fichier** : [hashtag_centrality_stats.csv](file:///Users/milan/projects/rgu-internship-social-media-analysis/deliverables/hashtag_centrality_stats.csv)

### 🌐 Visualisation Interactive du Réseau
Une carte interactive générée avec **Pyvis** permettant d'explorer les relations entre les hashtags. Les couleurs représentent les différentes communautés détectées.
- **Fichier** : [hashtag_network.html](file:///Users/milan/projects/rgu-internship-social-media-analysis/deliverables/hashtag_network.html)

---

## 🚀 Comment exécuter l'analyse à nouveau
Si vous souhaitez relancer l'analyse avec de nouvelles données, utilisez la commande suivante dans le terminal :
```bash
source .venv/bin/activate
python src/hashtag_network_analysis.py
```
