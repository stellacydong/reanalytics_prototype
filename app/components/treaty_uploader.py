import os
import streamlit as st

def handle_treaty_upload(uploaded_file, upload_dir="data/treaty_samples/"):
    """
    Save uploaded treaty file and return the path.
    """
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Uploaded: {uploaded_file.name}")
    return file_path
