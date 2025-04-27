# app/components/treaty_uploader.py

import os
import streamlit as st

def upload_treaties(upload_folder="data/treaties"):
    """
    Streamlit component to upload single or multiple treaty files.
    Saves uploaded files into a specified folder.

    Args:
        upload_folder (str): Path to the folder where treaties will be saved.

    Returns:
        list: List of saved file paths
    """
    st.sidebar.header("Upload Treaty Files")

    # Allow multiple file uploads
    uploaded_files = st.sidebar.file_uploader(
        "Upload one or more Treaty Documents (PDF or TXT):",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    # Create directory if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)

    saved_files = []

    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(upload_folder, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            saved_files.append(file_path)
        st.sidebar.success(f"✅ {len(saved_files)} file(s) successfully uploaded!")

    return saved_files
