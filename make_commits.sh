#!/bin/bash

# Commit 0 (Week 3) - May 3, 2026 10:00:00
git add src/clip_feature_extractor.py src/evaluate_alignment.py src/fetch_hateful_memes.py src/hateful_memes_dataset_fetcher.py src/youtube_dataset_fetcher.py deliverables/Week_1_Data_Acquisition/youtube_dataset_fetcher.py
GIT_AUTHOR_DATE="2026-05-03T10:00:00" GIT_COMMITTER_DATE="2026-05-03T10:00:00" git commit -m "traduction des scripts de pipeline multimodale et correction fetchers"

# Commit 1 (Week 4) - May 6, 2026 14:30:00
git add src/hashtag_network_analysis.py src/generate_static_plots.py deliverables/Week_4_Network_Science/ deliverables/hashtag_centrality_stats.csv deliverables/hashtag_network.html deliverables/plot_top_frequency.png deliverables/plot_top_influence.png deliverables/community_summary.csv
GIT_AUTHOR_DATE="2026-05-06T14:30:00" GIT_COMMITTER_DATE="2026-05-06T14:30:00" git commit -m "ajout analyse réseau des hashtags et graphiques statiques"

# Commit 2 (Week 5) - May 12, 2026 11:15:00
git add src/cross_platform_network.py src/precompute_layout.py deliverables/week_5/
GIT_AUTHOR_DATE="2026-05-12T11:15:00" GIT_COMMITTER_DATE="2026-05-12T11:15:00" git commit -m "ajout détection des communautés et fusion multiplateforme"

# Commit 3 (Week 6) - May 15, 2026 16:45:00
git add src/week6_polarization.py deliverables/week_6/
GIT_AUTHOR_DATE="2026-05-15T16:45:00" GIT_COMMITTER_DATE="2026-05-15T16:45:00" git commit -m "ajout calcul de la toxicité et index de polarisation par cluster"

# Commit 4 (Week 7) - May 19, 2026 11:30:00 (Today)
git add app.py
GIT_AUTHOR_DATE="2026-05-19T11:30:00" GIT_COMMITTER_DATE="2026-05-19T11:30:00" git commit -m "refonte du dashboard streamlit avec filtres et graphiques plotly"

# Add the Excel sheet tracking if it exists
git add "Milan Loi - Suivi de stage BUT2.xlsx"
GIT_AUTHOR_DATE="2026-05-19T12:00:00" GIT_COMMITTER_DATE="2026-05-19T12:00:00" git commit -m "mise à jour du document de suivi de stage"

