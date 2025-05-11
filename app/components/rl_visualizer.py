# app/components/rl_visualizer.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def run_and_plot_rl(claims_path: str):
    import streamlit as st
    from models import ppo_trainer, ppo_inference, visualize_ppo_results

    # Placeholder logic
    st.info("Training PPO agent...")
    ppo_trainer.main()

    st.success("Training complete. Running inference...")
    inference_result = ppo_inference.run_inference()

    st.info("Generating plots...")
    plot_paths = visualize_ppo_results.plot_results()

    return inference_result, plot_paths


def load_ppo_results(csv_path: str) -> pd.DataFrame:
    """
    Loads PPO simulation results from CSV.

    Args:
        csv_path (str): Path to CSV file with PPO outputs.

    Returns:
        pd.DataFrame: DataFrame with PPO simulation results.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"PPO results file not found: {csv_path}")

    df = pd.read_csv(csv_path)
    return df


def plot_retention_vs_profit(df: pd.DataFrame):
    """
    Plots Retention vs Profit.

    Args:
        df (pd.DataFrame): PPO simulation results.
    """
    st.subheader("Retention vs Underwriting Profit")
    fig, ax = plt.subplots()
    ax.scatter(df["retention"], df["profit"], alpha=0.6, color="teal")
    ax.set_xlabel("Retention ($)")
    ax.set_ylabel("Underwriting Profit ($)")
    ax.grid(True)
    st.pyplot(fig)


def plot_limit_vs_profit(df: pd.DataFrame):
    """
    Plots Limit vs Profit.

    Args:
        df (pd.DataFrame): PPO simulation results.
    """
    st.subheader("Limit vs Underwriting Profit")
    fig, ax = plt.subplots()
    ax.scatter(df["limit"], df["profit"], alpha=0.6, color="purple")
    ax.set_xlabel("Limit ($)")
    ax.set_ylabel("Underwriting Profit ($)")
    ax.grid(True)
    st.pyplot(fig)


def show_ppo_metrics_summary(df: pd.DataFrame):
    """
    Displays summary statistics from PPO run.

    Args:
        df (pd.DataFrame): PPO simulation results.
    """
    st.subheader("Key PPO Metrics")
    st.metric("Best Profit", f"${df['profit'].max():,.2f}")
    st.metric("Avg Retention", f"${df['retention'].mean():,.2f}")
    st.metric("Avg Limit", f"${df['limit'].mean():,.2f}")
