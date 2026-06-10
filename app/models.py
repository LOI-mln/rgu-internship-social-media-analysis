"""
Machine Learning models and classification.
"""

import streamlit as st
from typing import Callable


@st.cache_resource(show_spinner="Pre-loading Toxicity Classifier model...")
def load_toxicity_classifier() -> Callable:
    """
    Load DistilBERT toxicity classification model.
    
    Returns:
        Text-classification pipeline
    
    Raises:
        ImportError: If torch or transformers are not available
    """
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
    
    # Detect best available device
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    
    model_name = "martin-ha/toxic-comment-model"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    
    return pipeline("text-classification", model=model, tokenizer=tokenizer, device=device)
