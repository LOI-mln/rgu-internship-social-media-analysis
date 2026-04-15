📊 Stage RGU : Analyse Transplateforme des Médias Sociaux

Ce projet est réalisé dans le cadre d'un stage de 10 semaines à la Robert Gordon University (RGU). L'objectif est de collecter, traiter et analyser des données provenant de Reddit et YouTube pour étudier les dynamiques de communication, le sentiment et la toxicité en ligne.
🎯 Objectifs du Projet

    Collecte de données : Scraping automatisé via les API de Reddit (PRAW) et YouTube (yt-dlp).

    Analyse NLP : Utilisation de modèles de langage (Hugging Face) pour le scoring de toxicité et l'analyse de sentiment.

    Visualisation : Création de dashboards pour comparer les comportements entre plateformes.

📂 Structure du Projet
Plaintext

.
├── data/ # Données brutes et traitées (ignoré par Git)
├── docs/ # Documentation et rapports de stage
├── src/ # Code source Python (scrapers, analyse)
├── tests/ # Scripts de test
├── .env # Clés API privées (ignoré par Git)
├── .gitignore # Fichiers à exclure du repo
└── README.md # Présentation du projet

🛠 Installation
Prérequis

    Python 3.10 ou supérieur

    Un compte Reddit (pour les accès API)

1. Cloner le projet
   Bash

git clone <url-de-ton-repo>
cd <nom-du-dossier>

2. Configurer l'environnement virtuel
   Bash

python3 -m venv venv

# Activer sur Mac/Linux :

source venv/bin/activate

# Activer sur Windows :

.\venv\Scripts\activate

3. Installer les dépendances
   Bash

pip install praw yt-dlp transformers torch pandas python-dotenv

⚙️ Configuration

Créez un fichier .env à la racine du projet pour stocker vos identifiants :
Plaintext

REDDIT_CLIENT_ID="votre_id"
REDDIT_CLIENT_SECRET="votre_secret"
REDDIT_USER_AGENT="RGU_Internship_Scraper_v1.0"

🚀 Utilisation

Pour tester les scrapers (Semaine 1) :

    Reddit : python src/test_reddit.py

    YouTube : python src/test_youtube.py

🗓 Roadmap (Aperçu)

    Phase 1 : Setup et Scraping (Semaines 1-2)

    Phase 2 : Analyse Exploratoire & NLP (Semaines 3-6)

    Phase 3 : Dashboard & Reporting (Semaines 7-9)

    Phase 4 : Soutenance & Finalisation (Semaine 10)

Auteur : Milan LOI - Stagiaire à RGU
