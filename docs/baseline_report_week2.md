# Baseline Metrics Report (Week 2)

## 1. Context & Objectives

As part of the **Week 2** requirements for the social media analysis internship, the goal was to prepare the data through a rigorous cleaning pipeline and establish a baseline metric for evaluating the relationship between negativity and user engagement on platforms like YouTube and Reddit.

## 2. Data Cleaning Pipeline

The datasets processed were derived from two primary platforms:

- **Reddit** (`reddit_political.csv`)
- **YouTube** (`youtube_actual_politic.csv`, `youtube_bbc_gaza.csv`)

The cleaning pipeline steps included:

1. **Null Values Handling**: Stripping explicitly empty or unreadable lines (e.g., dropping empty texts or titles).
2. **Deduplication**: Removing identical texts to avoid skewing word frequencies and correlations.
3. **Language Filtering**: Implementing `langdetect` to isolate purely English (`'en'`) content for standardization before NLP tasks.

**Post-Cleaning Result:**

- High-quality, English-only datasets cleanly formatted for exploratory analysis and successfully saved in `data/cleaned/`.

## 3. Baseline Metric Analysis: Negativity × Engagement

### Methodology

To set a primitive baseline before utilizing advanced machine learning APIs (such as Perspective API planned for Phase 3), an approach using a naive dictionary of negative words (e.g., _bad, hate, stupid, idiot, fake_, etc.) was implemented.
We computed the correlation between the frequency of these negative words (negativity_score) and the text's corresponding engagement (score + num_comments for Reddit; like_count for YouTube).

### Results (Spearman Rank Correlation)

- **Reddit Dataset:** `ρ = 0.0148`, `p-value = 0.2246`
- **YouTube Dataset:** `ρ = 0.0050`, `p-value = 0.6326`

### Interpretation

The Spearman correlation coefficients (`rho`) are essentially zero for both platforms. Furthermore, the high `p-values` (>0.05) indicate that these results are statistically insignificant.

**Conclusion:**
There is no measurable monotonic relationship between simple negative vocabulary usage and user engagement metrics. This baseline outcome highlights the severe limitations of basic lexicon matching for sentiment/toxicity analysis. It serves as strong empirical evidence justifying the project's transition toward sophisticated ML models (Perspective API) which can detect contextual toxicity, dog-whistling, and subtle hostility that a simple word matching approach ignores.

## 4. Next Steps (Roadmap Phase 2)

With the dataset fully cleaned and the baseline established, the project will move onto Phase 2:

- Implementing advanced feature extraction (NLP sentiment analysis).
- Building interaction/co-occurrence networks.
- Setting up the Streamlit dashboard infrastructure to prepare for comparative visualization.
