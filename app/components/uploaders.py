# app/components/uploaders.py

import streamlit as st
import pandas as pd

def upload_treaty():
    """
    Upload a treaty file (.txt).

    Returns:
        - file_path (str) if uploaded, None otherwise
    """
    uploaded_treaty = st.sidebar.file_uploader("Upload Treaty File (.txt)", type=["txt"])
    if uploaded_treaty:
        file_path = "data/uploaded_treaty.txt"
        with open(file_path, "wb") as f:
            f.write(uploaded_treaty.getbuffer())
        st.success("Treaty uploaded successfully!")
        return file_path
    else:
        return None

def upload_claims():
    """
    Upload a claims CSV file.

    Returns:
        - claims_df (DataFrame) if uploaded, None otherwise
    """
    uploaded_claims = st.sidebar.file_uploader("Upload Claims Data (.csv)", type=["csv"])
    if uploaded_claims:
        claims_df = pd.read_csv(uploaded_claims)
        st.success("Claims data uploaded successfully!")
        return claims_df
    else:
        return None

