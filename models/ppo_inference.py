import os
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from ppo_structuring_agent import TreatyStructuringEnv

# Config
MODEL_PATH = "models/ppo_treaty_agent.zip"
CLAIMS_FILE = "data/synthetic_claims.csv"
NUM_EPISODES = 10
SAVE_DIR = "outputs/inference_results/"
os.makedirs(SAVE_DIR, exist_ok=True)

def run_inference():
    print("✅ Loaded trained PPO model")
    env = TreatyStructuringEnv(claims_file=CLAIMS_FILE)
    model = PPO.load(MODEL_PATH)

    results = []

    for episode in range(NUM_EPISODES):
        obs, _ = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _, info = env.step(action)

        results.append({
            "retention": env.retention,
            "limit": env.limit,
            "reward": reward,
            "profit": info.get("profit", None),
            "payout": info.get("payout", None)
        })

        print(f"Episode {episode+1}: Retention = ${env.retention:,.0f}, "
              f"Limit = ${env.limit:,.0f}, Reward = {reward:.2f}, "
              f"Profit = ${info.get('profit', 0):,.2f}")

    return results

def plot_results(results):
    retentions = [r["retention"] for r in results]
    profits = [r["profit"] for r in results]

    plt.figure(figsize=(8, 5))
    plt.plot(retentions, profits, marker='o')
    plt.title("Underwriting Profit vs Retention")
    plt.xlabel("Retention ($)")
    plt.ylabel("Profit ($)")
    plt.grid(True)

    plot_path = os.path.join(SAVE_DIR, "profit_vs_retention.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"📈 Plot saved to: {plot_path}")

if __name__ == "__main__":
    results = run_inference()
    plot_results(results)
