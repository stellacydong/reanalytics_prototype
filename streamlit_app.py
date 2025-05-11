import sys
import os

# Add the 'models' directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),  'models')))


import streamlit as st
import os
import tempfile
import pandas as pd
import matplotlib.pyplot as plt

# Import your local modules
from models.mistral_model_loader import summarize_treaty  # assumes this function exists
from models.ppo_inference import run_inference

from models.visualize_ppo_results import plot_training_curve

# App title and layout
st.set_page_config(page_title="Treaty Structuring Assistant", layout="wide")
st.title("📘 Intelligent Treaty Structuring Assistant")

st.markdown("Upload treaty documents and claims data to receive optimal treaty suggestions powered by LLM + RL.")

# --- Upload Section ---
with st.sidebar:
    st.header("📂 Upload Inputs")
    
    treaty_file = st.file_uploader("Upload Treaty File (.txt)", type=["txt"])
    claims_file = st.file_uploader("Upload Claims File (.csv)", type=["csv"])

    run_button = st.button("🚀 Run Optimization")

# --- Treaty Summary ---
if treaty_file:
    treaty_text = treaty_file.read().decode("utf-8")
    st.subheader("📄 Treaty Summary")
    
    with st.spinner("Summarizing treaty..."):
        summary = summarize_treaty(treaty_text)  # must return a string
        st.success("Summary generated.")
        st.markdown(f"**LLM Summary:**\n\n{summary}")

# --- Run Optimization ---
if run_button and claims_file:
    # Save files temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_treaty:
        tmp_treaty.write(treaty_text.encode("utf-8"))
        treaty_path = tmp_treaty.name

    claims_df = pd.read_csv(claims_file)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_claims:
        claims_df.to_csv(tmp_claims.name, index=False)
        claims_path = tmp_claims.name

    st.subheader("🤖 Optimization Output")
    
    with st.spinner("Running PPO optimizer..."):
        result = run_inference(treaty_path, claims_path)
        st.success("Optimization complete.")
        
        st.markdown(f"""
        - **Optimal Retention:** ${result['retention']:,.0f}  
        - **Optimal Limit:** ${result['limit']:,.0f}  
        - **LLM Reasoning:** {result['llm_summary']}
        """)

    # --- Plot reward curve ---
    st.subheader("📈 PPO Training Rewards")
    fig = plot_training_curve(result['rewards'])  # assumes it returns a Matplotlib figure
    st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.markdown("🔬 Built with 🧠 Reinforcement Learning + LLMs | ReAnalytics 2025")
