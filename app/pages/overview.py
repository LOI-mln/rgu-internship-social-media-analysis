"""
Page 1: Exploratory Data Analysis & Baseline
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from app.data_loader import load_clip_data


def render_page_1():
    """Display page 1: Overview & Baselines."""
    st.header("Exploratory Data Analysis & Baseline")
    
    tab1, tab2 = st.tabs(["Lexical Baseline", "Multimodal CLIP Analysis"])
    
    with tab1:
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
        
    with tab2:
        st.subheader("Multimodal CLIP Meme Analysis")
        st.markdown("""
        Standard NLP models process text in isolation. However, online propaganda and political memes rely on multimodality—combining seemingly harmless images with toxic text or vice versa. 
        
        To study these dynamics, we deploy OpenAI's CLIP model (`clip-vit-base-patch32`) to project both modalities into a shared vector space, allowing us to compute text-image similarity and perform zero-shot classification.
        """)
        
        clip_df = load_clip_data()
        if clip_df is not None:
            # Calculate mean statistics
            hateful_mean = clip_df[clip_df['label'] == 1]['clip_similarity'].mean()
            non_hateful_mean = clip_df[clip_df['label'] == 0]['clip_similarity'].mean()
            
            # Display stats
            st.markdown("### Model Metrics & Findings")
            st.markdown(f"""
            *   **Mean Cosine Similarity for Non-Hateful Memes:** `{non_hateful_mean:.4f}`
            *   **Mean Cosine Similarity for Hateful Memes:** `{hateful_mean:.4f}`
            """)
            
            # Interactive Box Plot
            st.markdown("### Text-Image Alignment Distribution")
            
            box_df = clip_df.copy()
            box_df['Toxicity Status'] = box_df['label'].map({0: 'Non-Hateful (0)', 1: 'Hateful (1)'})
            
            fig_box = px.box(
                box_df,
                x='Toxicity Status',
                y='clip_similarity',
                color='Toxicity Status',
                labels={'Toxicity Status': 'Toxicity Status', 'clip_similarity': 'Cosine Similarity (CLIP)'},
                color_discrete_sequence=['#3B82F6', '#60A5FA']
            )
            fig_box.update_layout(
                plot_bgcolor='#F8FAFC',
                paper_bgcolor='#F8FAFC',
                font_color="#0F172A",
                showlegend=False
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
            st.markdown("""
            **Interpretation of Text-Image Alignment:**
            *   **Semantic Mismatch**: Hateful memes exhibit a lower average cosine similarity compared to non-hateful memes. This indicates a greater disconnect between the image content and the text caption.
            *   **Subtle Propaganda**: Hostile actors frequently employ visual metaphors or completely benign images (e.g., historical pictures or neutral backgrounds) coupled with toxic textual descriptions to bypass automated filters, which is captured by the lower alignment score.
            """)
            
            st.markdown("---")
            
            # Interactive Bar Chart for zero-shot visual labels
            st.markdown("### Visual Zero-Shot Categorization")
            counts = clip_df['visual_label'].value_counts().reset_index()
            counts.columns = ['Visual Label', 'Meme Count']
            
            fig_bar = px.bar(
                counts,
                x='Meme Count',
                y='Visual Label',
                orientation='h',
                color='Visual Label',
                color_discrete_sequence=['#3B82F6', '#60A5FA', '#93C5FD']
            )
            fig_bar.update_layout(
                plot_bgcolor='#F8FAFC',
                paper_bgcolor='#F8FAFC',
                font_color="#0F172A",
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.markdown("""
            **Interpretation of Zero-Shot Classification:**
            *   **In-Group vs Out-Group Visual Dynamics**: Zero-shot classification categorizes the images into in-group, out-group, or neutral themes. Out-group classification indicates images designed to portray the out-group negatively, while in-group classification focuses on community identity and pride.
            """)
            
            st.markdown("---")
            
            # Interactive Explorer
            st.markdown("### Multimodal Meme Explorer")
            st.markdown("Select a meme ID to inspect the visual image, corresponding text, and calculated similarity metrics.")
            
            filter_type = st.selectbox("Meme Category Filter", ["All", "Non-Hateful (Label 0)", "Hateful (Label 1)"])
            if filter_type == "Non-Hateful (Label 0)":
                filtered_df = clip_df[clip_df['label'] == 0]
            elif filter_type == "Hateful (Label 1)":
                filtered_df = clip_df[clip_df['label'] == 1]
            else:
                filtered_df = clip_df
                
            selected_id = st.selectbox("Meme ID Selection", filtered_df['id'].tolist()[:50])
            selected_row = filtered_df[filtered_df['id'] == selected_id].iloc[0]
            
            import os
            image_path = selected_row['image_path']
            if os.path.exists(image_path):
                st.image(image_path, width=400)
            else:
                st.info("Visual meme image not found locally (raw image datasets are excluded from Git repository to keep the codebase lightweight). Showing metadata and metrics only.")
            
            st.markdown(f"""
            *   **Text Caption:** "{selected_row['text']}"
            *   **Toxicity Label:** `{'Hateful (1)' if selected_row['label'] == 1 else 'Non-Hateful (0)'}`
            *   **CLIP Cosine Similarity:** `{selected_row['clip_similarity']:.4f}`
            *   **Zero-Shot Visual Classification:** `{selected_row['visual_label']}`
            """)
        else:
            st.warning("CLIP scored dataset not found. Please verify that data/cleaned/hateful_memes_clip_scored.csv exists.")
