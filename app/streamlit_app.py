# app/streamlit_app.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.components.treaty_uploader import handle_treaty_upload
from app.components.summary_view import display_summary
from app.components.rl_visualizer import run_and_plot_rl

st.set_page_config(page_title="TreatyStructuring-GPT", layout="wide")

# Title and Hero Section
st.markdown("""
    <style>
        .title {
            font-size: 2.8em;
            font-weight: bold;
            color: #2c3e50;
        }
        .subtitle {
            font-size: 1.3em;
            color: #34495e;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">📑 TreatyStructuring-GPT</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Co-Pilot for Reinsurance Structuring — LLM + RL + RAG</p>', unsafe_allow_html=True)

# Treaty File Upload
st.markdown("---")
st.header("📤 Upload Treaty File")

uploaded_file = st.file_uploader("Upload treaty", type=["txt"])
if uploaded_file:
    filepath = handle_treaty_upload(uploaded_file)
    st.success(f"Uploaded treaty to: `{filepath}`")

    # LLM Summary
    st.markdown("---")
    st.header("🧠 Treaty Summary (LLM-RAG)")
    summary = display_summary(filepath)
    st.info(summary)

    # PPO Optimization
    st.markdown("---")
    st.header("📊 PPO Optimization Result (RL Agent)")
    claims_file = st.file_uploader("Upload claims data", type=["csv"])
    if claims_file:
        run_and_plot_rl(claims_file)


else:
    st.warning("Please upload a treaty file to get started.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Reinsurance Analytics")

