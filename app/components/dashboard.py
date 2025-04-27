# app/components/dashboard.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_dashboard(original_portfolio, optimized_portfolio):
    """
    Displays a dashboard comparing original and optimized portfolios.

    Args:
    - original_portfolio (list): List of original treaty dictionaries.
    - optimized_portfolio (list): List of optimized treaty dictionaries.
    """
    st.header("📊 Portfolio Optimization Dashboard")

    # Prepare DataFrames
    df_original = pd.DataFrame(original_portfolio)
    df_optimized = pd.DataFrame(optimized_portfolio)

    # Show basic statistics
    st.subheader("Portfolio Metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Avg Retention (Original)", f"${df_original['retention'].mean():,.0f}")
        st.metric("Avg Limit (Original)", f"${df_original['limit'].mean():,.0f}")

    with col2:
        st.metric("Avg Retention (Optimized)", f"${df_optimized['retention'].mean():,.0f}")
        st.metric("Avg Limit (Optimized)", f"${df_optimized['limit'].mean():,.0f}")

    # Plot side-by-side Retention comparison
    st.subheader("Retention per Treaty")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_original['treaty_name'],
        y=df_original['retention'],
        name='Original Retention'
    ))
    fig.add_trace(go.Bar(
        x=df_optimized['treaty_name'],
        y=df_optimized['retention'],
        name='Optimized Retention'
    ))
    fig.update_layout(barmode='group', xaxis_title='Treaty', yaxis_title='Retention ($)', height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Plot side-by-side Limit comparison
    st.subheader("Limit per Treaty")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=df_original['treaty_name'],
        y=df_original['limit'],
        name='Original Limit'
    ))
    fig2.add_trace(go.Bar(
        x=df_optimized['treaty_name'],
        y=df_optimized['limit'],
        name='Optimized Limit'
    ))
    fig2.update_layout(barmode='group', xaxis_title='Treaty', yaxis_title='Limit ($)', height=500)
    st.plotly_chart(fig2, use_container_width=True)

