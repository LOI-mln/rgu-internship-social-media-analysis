📊 RGU Internship: Cross-platform Social Media Analysis

This project is part of a 10-week internship at Robert Gordon University (RGU). The objective is to collect, process, and analyze data from Reddit and YouTube to study online communication dynamics, sentiment, and toxicity.

🎯 Project Objectives

    Data Collection: Automated scraping via Reddit (PRAW) and YouTube (yt-dlp) APIs.

    NLP Analysis: Using language models (Hugging Face) for toxicity scoring and sentiment analysis.

    Visualization: Creating dashboards to compare behaviors across platforms.

📂 Project Structure
Plaintext

.
├── data/       # Raw and processed data (ignored by Git)
├── docs/       # Documentation and internship reports
├── src/        # Python source code (scrapers, analysis)
├── tests/      # Test scripts
├── .env        # Private API keys (ignored by Git)
├── .gitignore  # Files to exclude from the repo
└── README.md   # Project overview

🛠 Installation
Prerequisites

    Python 3.10 or higher

    A Reddit account (for API access)

1. Clone the project
   Bash

git clone <your-repo-url>
cd <folder-name>

2. Set up the virtual environment
   Bash

python3 -m venv venv

# Activate on Mac/Linux:

source venv/bin/activate

# Activate on Windows:

.\venv\Scripts\activate

3. Install dependencies
   Bash

pip install praw yt-dlp transformers torch pandas python-dotenv

⚙️ Configuration

Create a .env file at the root of the project to store your credentials:
Plaintext

REDDIT_CLIENT_ID="your_id"
REDDIT_CLIENT_SECRET="your_secret"
REDDIT_USER_AGENT="RGU_Internship_Scraper_v1.0"

🚀 Usage

To test the scrapers (Week 1):

    Reddit: python src/test_reddit.py

    YouTube: python src/test_youtube.py

🗓 Roadmap (Overview)

    Phase 1: Setup and Scraping (Weeks 1-2)

    Phase 2: Exploratory Analysis & NLP (Weeks 3-6)

    Phase 3: Dashboard & Reporting (Weeks 7-9)

    Phase 4: Defense & Finalization (Week 10)

Author: Milan LOI - Intern at RGU
