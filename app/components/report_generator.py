import os
import matplotlib.pyplot as plt

def generate_summary_plot(rewards, output_dir="app/static/img"):
    """
    Generate and save a line plot of PPO rewards over time.

    Args:
        rewards (list): A list of reward values (floats or ints).
        output_dir (str): Directory path to save the image (inside Django static).

    Returns:
        str: Full file path of the saved image.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "summary_plot.png")

    # Plotting
    plt.figure(figsize=(10, 4))
    plt.plot(rewards, marker='o', linestyle='-', color='royalblue')
    plt.title("Cumulative PPO Rewards")
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return output_path
