"""
Page 1: Exploratory Data Analysis & Baseline
"""

import streamlit as st


def render_page_1():
    """Display page 1: Overview & Baselines."""
    st.header("Exploratory Data Analysis & Baseline")
    
    st.subheader("Lexical Baseline & Negativity Analysis")
    st.markdown("""
    Before deploying complex AI, we established a baseline using standard lexicons.
    **Hypothesis:** Is there a direct link between negative words and user engagement?
    """)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Reddit (Spearman ρ)", "0.014", "No Correlation")
    c2.metric("YouTube (Spearman ρ)", "0.005", "No Correlation")
    c3.metric("Conclusion", "Failed", "Requires Contextual AI")
    
    st.markdown("""
    **Interpretation & Insights:**
    *   **Keyword Limitations**: Simple keyword counting fails to capture sarcasm, political dog-whistles, or conversational context. The Spearman correlation coefficients are statistically indistinguishable from zero, showing no monotonic relationship between engagement and simple negative word frequencies.
    *   **Need for Sequence Modeling**: This failure justifies the deployment of deep learning text classifiers (such as the Google Perspective API and DistilBERT toxicity models) that process entire sentences contextually instead of matching static dictionaries.
    """)
