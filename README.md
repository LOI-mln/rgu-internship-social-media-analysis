# RGU Internship: Cross-Platform Social Media Analysis

This project was developed during a 10-week internship at Robert Gordon University (RGU).
It collects, cleans, analyzes, and visualizes social media data from several platforms in order to study online polarization, echo chambers, toxicity, and "we vs them" discourse patterns.

Author: Milan Loi

## Main Features

- Data acquisition from YouTube, Reddit, and public datasets.
- Cleaning and normalization of social media text data.
- NLP indicators for in-group and out-group language.
- Toxicity and polarization analysis.
- Hashtag and cross-platform network analysis.
- Streamlit dashboard for interactive visualization.
- Scripts for generating figures, reports, and presentation materials.

## Project Structure

```text
.
├── app/                         # Refactored Streamlit dashboard
├── src/                         # Data acquisition, NLP, network, and utility scripts
│   ├── acquisition/             # Scrapers and dataset fetchers
│   ├── common/                  # Shared text and YouTube utilities
│   ├── network/                 # Graph and community detection scripts
│   ├── nlp/                     # CLIP, toxicity, and polarization analysis
│   └── utils/                   # Plot, DOCX, and presentation generation scripts
├── data/                        # Raw and cleaned datasets, ignored by Git
├── deliverables/                # Minimal dashboard runtime artifacts only
├── docs/                        # Reports, papers, and documentation
├── tests/                       # Validation scripts
├── app.py                       # Main Streamlit entry point
├── run_demos.sh                 # Interactive demo launcher
├── .env                         # Local secrets and API keys, ignored by Git
├── .gitignore
└── README.md
```

## Requirements

Recommended environment:

- Python 3.10 or newer
- Git
- pip
- A terminal or shell
- Optional: YouTube scraping requires `yt-dlp`
- Optional: Perspective API requires a Google/Perspective API key

Main Python packages used by the project include:

```text
streamlit
pandas
numpy
plotly
matplotlib
seaborn
networkx
python-louvain
pyvis
python-dotenv
tqdm
datasets
transformers
torch
Pillow
python-docx
python-pptx
yt-dlp
google-api-python-client
```

If a `requirements.txt` file is available, prefer installing from it. If it is missing, generate it from the working machine before migration:

```bash
pip freeze > requirements.txt
```

## Installation on a New Machine

### 1. Clone the repository

```bash
git clone https://github.com/loi-mln/rgu-internship-social-media-analysis.git
cd rgu-internship-social-media-analysis
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If `requirements.txt` exists:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet:

```bash
pip install streamlit pandas numpy plotly matplotlib seaborn networkx python-louvain pyvis python-dotenv tqdm datasets transformers torch Pillow python-docx python-pptx yt-dlp google-api-python-client
```

## Environment Variables

Create a `.env` file at the project root if you use API-based scripts.

Example:

```env
PERSPECTIVE_API_KEY=your_perspective_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=RGU_Internship_Scraper_v1.0
```

Important: never commit `.env` to Git. It contains private credentials.

## Migrating the Project to Another Machine

Use this checklist when moving the project.

### On the current machine

1. Save the latest code:

```bash
git status
git add .
git commit -m "Prepare project for migration"
git push
```

2. Export dependencies:

```bash
source .venv/bin/activate
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add Python dependencies"
git push
```

3. Copy local files ignored by Git.

The following paths are usually not fully stored in Git and may need to be copied manually:

```text
data/
.env
docs/
```

Create a backup archive:

```bash
zip -r migration_backup.zip data docs .env
```

### On the new machine

1. Clone the repository.
2. Create and activate `.venv`.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy or unzip `migration_backup.zip` into the project root.
5. Run the dashboard:

```bash
streamlit run app.py
```

## Running the Dashboard

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard should open in the browser at:

```text
http://localhost:8501
```

## Running Demo Scripts

The project includes an interactive launcher:

```bash
chmod +x run_demos.sh
./run_demos.sh
```

The menu can launch:

- Streamlit dashboard
- CLIP multimodal evaluation
- polarization index computation
- cross-platform network analysis
- PowerPoint generation

## Useful Commands

Run the CLIP alignment evaluation:

```bash
python src/nlp/evaluate_alignment.py
```

Compute cluster polarization:

```bash
python src/nlp/week6_polarization.py
```

Generate the cross-platform graph:

```bash
python src/network/cross_platform_network.py
```

Generate static hashtag plots:

```bash
python src/utils/generate_static_plots.py
```

Generate the PowerPoint presentation:

```bash
python src/utils/generate_presentation.py
```

## Data Notes

The `data/` directory is ignored by Git because it can be large and may contain raw datasets.

Expected subfolders include:

```text
data/raw/
data/cleaned/
data/uploads/
```

If the dashboard shows missing data, check that the required CSV, GML, JSON, or generated metric files were copied into the same paths used on the original machine.

## Deliverables Policy

Most files in `deliverables/` are generated outputs and are not required to run the project.
They are ignored by Git to keep the repository lighter.

Only the dashboard runtime artifacts are kept:

```text
deliverables/week_5/cross_platform_merged.gml
deliverables/week_5/echo_chamber_metrics.txt
deliverables/week_5/layout_positions.json
deliverables/week_6/community_polarization_metrics.csv
```

Other figures, presentations, HTML exports, notebooks, and weekly snapshots can be regenerated with the scripts in `src/`.

## Troubleshooting

### `streamlit: command not found`

Activate the virtual environment and install dependencies:

```bash
source .venv/bin/activate
pip install streamlit
```

### Missing datasets

Copy the `data/` folder from the original machine, or rerun the acquisition and cleaning scripts.

### Missing API key

Create `.env` at the project root and add the required key, for example:

```env
PERSPECTIVE_API_KEY=your_key_here
```

### PyTorch or Transformers installation issues

Install PyTorch using the command recommended for your operating system from the official PyTorch website, then reinstall the remaining dependencies.

## Git Ignore Policy

The repository intentionally ignores:

```text
data/
deliverables/
.env
.venv/
venv/
__pycache__/
*.pyc
*.log
.DS_Store
```

This keeps the repository lighter and avoids committing secrets or generated cache files.
