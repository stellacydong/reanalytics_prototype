# models/visualize_ppo_results.py

import os
import pandas as pd
import matplotlib.pyplot as plt

# === Load PPO simulation results ===
csv_path = "data/ppo_simulation.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"{csv_path} not found. Please run ppo_inference.py first.")

df = pd.read_csv(csv_path)

# === Create output directory ===
os.makedirs("outputs", exist_ok=True)

# === Plot Retention ===
plt.figure(figsize=(8, 4))
plt.plot(df["Step"], df["Retention"], color="navy", linewidth=2)
plt.title("Retention Over Time")
plt.xlabel("Step")
plt.ylabel("Retention ($)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/retention_over_time.png")
print("📊 Saved: outputs/retention_over_time.png")

# === Plot Limit ===
plt.figure(figsize=(8, 4))
plt.plot(df["Step"], df["Limit"], color="green", linewidth=2)
plt.title("Limit Over Time")
plt.xlabel("Step")
plt.ylabel("Limit ($)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/limit_over_time.png")
print("📊 Saved: outputs/limit_over_time.png")

# === Plot Reward ===
plt.figure(figsize=(8, 4))
plt.plot(df["Step"], df["Reward"], color="orange", linewidth=2)
plt.title("Reward Over Time")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/reward_over_time.png")
print("📊 Saved: outputs/reward_over_time.png")

