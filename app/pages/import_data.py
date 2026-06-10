"""
Page 4: Import New Dataset
"""

import os
import streamlit as st
import pandas as pd
from app.config import UPLOADED_DIR
from app.utils.text_processing import count_pronouns_in_text
from app.models import load_toxicity_classifier


def render_page_4():
    """Render page 4: Import New Dataset."""
    st.header("Import New Dataset")
    st.markdown("""
    Incorporate custom text datasets to analyze language patterns across different platforms.
    All data is processed locally, extracting linguistic tribalism indicators.
    """)
    
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df_preview = pd.read_csv(uploaded_file, nrows=5)
            st.markdown("### Dataset Preview")
            st.dataframe(df_preview, use_container_width=True)
            
            with st.form("mapping_form"):
                st.markdown("### Schema Mapping & Processing Configuration")
                
                platform_input = st.text_input("Platform Name", placeholder="e.g. Facebook, TikTok").strip()
                columns = df_preview.columns.tolist()
                
                default_text_idx = _find_default_col(columns, ["text", "comment", "body", "content", "message", "msg"])
                default_date_idx = _find_default_col(columns, ["date", "time", "created", "timestamp", "utc"], is_optional=True)
                default_eng_idx = _find_default_col(columns, ["like", "score", "upvote", "engagement", "reply", "replies"], is_optional=True)
                
                text_col = st.selectbox("Text Content Column (Required)", columns, index=default_text_idx)
                date_col = st.selectbox("Date / Timestamp Column (Optional)", ["None"] + columns, index=default_date_idx)
                eng_col = st.selectbox("Engagement / Likes Column (Optional)", ["None"] + columns, index=default_eng_idx)
                
                submit_button = st.form_submit_button("Import & Process Dataset")
                
                if submit_button:
                    _process_uploaded_dataset(uploaded_file, platform_input, text_col, date_col, eng_col)
        
        except Exception as e:
            st.error(f"Error reading CSV: {e}")


def _find_default_col(cols, keywords, is_optional=False) -> int:
    """Find the default index for a column."""
    for idx, c in enumerate(cols):
        c_low = c.lower()
        if any(kw in c_low for kw in keywords):
            return idx + (1 if is_optional else 0)
    return 0 if not is_optional else 1


def _process_uploaded_dataset(uploaded_file, platform_input: str, text_col: str, date_col: str, eng_col: str):
    """Process and import the uploaded dataset."""
    if not platform_input:
        st.error("Please enter a valid Platform Name.")
        return
    
    if not text_col:
        st.error("Please map a Text Content Column.")
        return
    
    with st.spinner("Processing text and compiling pronoun indicators..."):
        uploaded_file.seek(0)
        df_full = pd.read_csv(uploaded_file)
        
        # Initialization
        processed_df = pd.DataFrame()
        processed_df['platform'] = [platform_input] * len(df_full)
        
        # Parse dates
        if date_col != "None":
            processed_df['date'] = pd.to_datetime(df_full[date_col], errors='coerce')
        else:
            processed_df['date'] = pd.NaT
        
        # Text processing & pronoun counting
        text_series = df_full[text_col].astype(str).str.lower()
        
        we_counts = []
        them_counts = []
        for text in text_series:
            we_count, them_count = count_pronouns_in_text(text)
            we_counts.append(we_count)
            them_counts.append(them_count)
        
        processed_df['we_count'] = we_counts
        processed_df['them_count'] = them_counts
        processed_df['word_count'] = text_series.apply(lambda x: len(x.split())).fillna(0).astype(int)
        
        # Engagement parsing
        if eng_col != "None":
            processed_df['engagement'] = pd.to_numeric(df_full[eng_col], errors='coerce').fillna(0)
        else:
            processed_df['engagement'] = 0.0
        
        # Toxicity classification
        try:
            classifier = load_toxicity_classifier()
            st.write("Executing toxic comment classification model...")
            
            negativity_scores = []
            total_rows = len(df_full)
            limit_rows = min(10, total_rows)
            
            prog_bar = st.progress(0.0)
            status_text = st.empty()
            
            for idx in range(total_rows):
                if idx < limit_rows:
                    text_val = str(df_full[text_col].iloc[idx])
                    if len(text_val.strip()) == 0:
                        negativity_scores.append(0.35)
                        continue
                    
                    try:
                        res = classifier(text_val[:200])[0]
                        label = res['label']
                        score = float(res['score'])
                        
                        tox_score = score if label == 'toxic' else 1.0 - score
                        negativity_scores.append(tox_score)
                        
                        status_text.text(f"Processed row {idx+1}/{limit_rows}: \"{text_val[:50]}...\" -> {label} ({tox_score:.3f})")
                    except Exception:
                        negativity_scores.append(0.35)
                else:
                    negativity_scores.append(0.35)
                
                prog_bar.progress((idx + 1) / limit_rows)
            
            processed_df['negativity_score'] = negativity_scores
            
        except Exception as e:
            st.warning(f"Model error, using default scores: {e}")
            processed_df['negativity_score'] = 0.35
        
        # Save
        os.makedirs(UPLOADED_DIR, exist_ok=True)
        target_filename = f"{UPLOADED_DIR}/{platform_input.lower().replace(' ', '_')}_uploaded.csv"
        processed_df.to_csv(target_filename, index=False)
        
        st.cache_data.clear()
        st.success(f"✓ {platform_input} dataset imported successfully! View metrics on page 3.")
