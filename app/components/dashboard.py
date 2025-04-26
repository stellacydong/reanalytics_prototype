# app/components/dashboard.py

import plotly.graph_objects as go
import streamlit as st
import numpy as np


def show_dashboard(claims_df):
    """
    Displays a dashboard comparing Traditional vs PPO Reserve Optimization
    including CVaR, Solvency Ratio, and total reserves.
    """
    st.header("\ud83d\udcca Reserve Optimization Dashboard")

    # Safety check
    if claims_df is None or 'traditional_reserve' not in claims_df.columns or 'ppo_reserve' not in claims_df.columns:
        st.warning("Please run a simulation first to generate reserve columns.")
        return

    # Compute Metrics
    total_traditional = claims_df['traditional_reserve'].sum()
    total_ppo = claims_df['ppo_reserve'].sum()

    cvar_traditional = np.percentile(claims_df['traditional_reserve'], 95)
    cvar_ppo = np.percentile(claims_df['ppo_reserve'], 95)

    solvency_traditional = total_traditional / (claims_df['paid_loss'].sum() + 1e-6)
    solvency_ppo = total_ppo / (claims_df['paid_loss'].sum() + 1e-6)

    # Metric Cards
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Traditional Reserve", value=f"${total_traditional:,.0f}")
        st.metric(label="Traditional CVaR (95%)", value=f"${cvar_traditional:,.0f}")
        st.metric(label="Traditional Solvency Ratio", value=f"{solvency_traditional:.2f}")
    with col2:
        st.metric(label="Total PPO Reserve", value=f"${total_ppo:,.0f}")
        st.metric(label="PPO CVaR (95%)", value=f"${cvar_ppo:,.0f}")
        st.metric(label="PPO Solvency Ratio", value=f"{solvency_ppo:.2f}")

    # Reserve Distribution Plot
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=claims_df['traditional_reserve'], name="Traditional Reserve", opacity=0.6))
    fig.add_trace(go.Histogram(x=claims_df['ppo_reserve'], name="PPO Reserve", opacity=0.6))

    fig.update_layout(
        title_text='Reserve Distributions (Traditional vs PPO)',
        xaxis_title='Reserve Amount',
        yaxis_title='Count',
        barmode='overlay',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # CVaR Comparison Plot
    fig_cvar = go.Figure(data=[
        go.Bar(name='Traditional CVaR', x=['CVaR (95%)'], y=[cvar_traditional]),
        go.Bar(name='PPO CVaR', x=['CVaR (95%)'], y=[cvar_ppo])
    ])

    fig_cvar.update_layout(
        title_text='CVaR (Tail Risk) Comparison',
        template='plotly_white',
        barmode='group'
    )

    st.plotly_chart(fig_cvar, use_container_width=True)

