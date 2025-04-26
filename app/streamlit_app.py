# app/streamlit_app.py

import streamlit as st
from agents.treaty_rag_agent import TreatyRAGAgent
from models.ppo_reserving_agent import PPOReserveAgent
import pandas as pd
import numpy as np

# Initialize session state if not already done
if 'treaty_agent' not in st.session_state:
    st.session_state['treaty_agent'] = None

if 'ppo_agent' not in st.session_state:
    st.session_state['ppo_agent'] = PPOReserveAgent()

if 'claims_data' not in st.session_state:
    st.session_state['claims_data'] = None

# Streamlit page configuration
st.set_page_config(page_title="ReAnalytics Co-Pilot", layout="wide")

st.title("\ud83d\ude80 ReAnalytics: Reinsurance Co-Pilot")

st.sidebar.header("Upload Files")

# Treaty Upload
uploaded_treaty = st.sidebar.file_uploader("Upload Treaty File (.txt)", type=["txt"])
if uploaded_treaty:
    with open("data/uploaded_treaty.txt", "wb") as f:
        f.write(uploaded_treaty.getbuffer())
    st.session_state['treaty_agent'] = TreatyRAGAgent()
    st.session_state['treaty_agent'].ingest_treaty("data/uploaded_treaty.txt")
    st.success("Treaty uploaded and ingested!")

# Claims Upload
uploaded_claims = st.sidebar.file_uploader("Upload Claims Data (.csv)", type=["csv"])
if uploaded_claims:
    claims_df = pd.read_csv(uploaded_claims)
    st.session_state['claims_data'] = claims_df
    st.success("Claims data uploaded!")

st.sidebar.markdown("---")

# Main App Tabs
tab1, tab2, tab3 = st.tabs(["\ud83e\uddf5 Treaty QA", "\ud83c\udfcb\ufe0f\u200d\u2640 Reserve Simulator", "\ud83d\udd22 Dashboard"])

# Tab 1: Treaty Q&A
with tab1:
    st.header("\ud83e\uddf5 Treaty Assistant")
    if st.session_state['treaty_agent'] is None:
        st.info("Please upload a treaty file to start.")
    else:
        query = st.text_input("Ask a question about the treaty:", placeholder="e.g., What is the retention amount?")
        if query:
            answer = st.session_state['treaty_agent'].ask(query)
            st.success(answer)

# Tab 2: Reserve Simulation
with tab2:
    st.header("\ud83c\udfcb\ufe0f\u200d\u2640 Reserve Optimization Simulator")
    if st.session_state['claims_data'] is None:
        st.info("Please upload claims data to simulate reserving.")
    else:
        claims_df = st.session_state['claims_data']
        st.subheader("Sample Claims Data")
        st.dataframe(claims_df.head())

        # Traditional Method
        claims_df['traditional_reserve'] = claims_df['incurred_loss'] * 1.2

        # PPO Optimized Method
        incurred_losses = claims_df['incurred_loss'].values
        ppo_agent = st.session_state['ppo_agent']
        ppo_reserves = np.array([ppo_agent.predict_reserve(x) for x in incurred_losses])
        claims_df['ppo_reserve'] = ppo_reserves

        st.subheader("Reserving Comparison")
        st.bar_chart(claims_df[['traditional_reserve', 'ppo_reserve']])

# Tab 3: Dashboard
with tab3:
    st.header("\ud83d\udd22 Risk Metrics Dashboard")
    if st.session_state['claims_data'] is None:
        st.info("Please upload claims data to view dashboard.")
    else:
        claims_df = st.session_state['claims_data']

        total_traditional = claims_df['traditional_reserve'].sum()
        total_ppo = claims_df['ppo_reserve'].sum()

        cvar_traditional = np.percentile(claims_df['traditional_reserve'], 95)
        cvar_ppo = np.percentile(claims_df['ppo_reserve'], 95)

        solvency_traditional = total_traditional / (claims_df['paid_loss'].sum() + 1e-6)
        solvency_ppo = total_ppo / (claims_df['paid_loss'].sum() + 1e-6)

        st.metric(label="Total Traditional Reserve", value=f"${total_traditional:,.0f}")
        st.metric(label="Total PPO Reserve", value=f"${total_ppo:,.0f}")
        st.metric(label="Traditional CVaR (95%)", value=f"${cvar_traditional:,.0f}")
        st.metric(label="PPO CVaR (95%)", value=f"${cvar_ppo:,.0f}")
        st.metric(label="Traditional Solvency Ratio", value=f"{solvency_traditional:.2f}")
        st.metric(label="PPO Solvency Ratio", value=f"{solvency_ppo:.2f}")

