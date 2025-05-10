import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Config
INPUT_CSV = "data/ppo_simulation.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_metric_over_time(df, metric, ylabel, title, filename):
    plt.figure(figsize=(10, 4))
    sns.lineplot(x=range(len(df)), y=df[metric], marker="o")
    plt.title(title)
    plt.xlabel("Timestep")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path)
    print(f"✅ Saved: {path}")
    plt.close()

def main():
    try:
        df = pd.read_csv(INPUT_CSV)
        if df.empty:
            raise ValueError("CSV is empty.")

        # Drop rows with NaNs
        df = df.dropna(subset=["retention", "limit", "reward"])

        # Plot each metric
        plot_metric_over_time(df, "retention", "Retention ($)", "Retention Over Time", "retention_plot.png")
        plot_metric_over_time(df, "limit", "Limit ($)", "Limit Over Time", "limit_plot.png")
        plot_metric_over_time(df, "reward", "Reward", "Cumulative Reward Over Time", "reward_plot.png")

    except FileNotFoundError:
        print(f"❌ Error: File not found: {INPUT_CSV}")
    except ValueError as ve:
        print(f"❌ Error: {ve}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
