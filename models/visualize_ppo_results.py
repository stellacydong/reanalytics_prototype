import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_training_curve(log_path):
    """
    Load Stable-Baselines3 PPO training logs and generate a reward curve.

    Args:
        log_path (str): Path to monitor.csv file

    Returns:
        matplotlib.figure.Figure: A plot of episode rewards over time
    """
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Log file not found at: {log_path}")

    # Load CSV log
    df = pd.read_csv(log_path, skiprows=1)  # Skip first header line (SB3-specific format)

    if "r" not in df.columns or "l" not in df.columns:
        raise ValueError("Expected columns 'r' (reward) and 'l' (episode length) not found.")

    # Plot episode rewards
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["r"].rolling(window=10).mean(), label="Smoothed Reward", color="blue")
    ax.set_title("PPO Training Reward Curve")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    return fig
