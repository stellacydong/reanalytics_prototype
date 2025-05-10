# models/ppo_inference.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from ppo_structuring_agent import TreatyStructuringEnv

# === Load synthetic claims ===
claims_df = pd.read_csv("data/synthetic_claims.csv")

# === Initialize environment ===
env = TreatyStructuringEnv(claims_df=claims_df, premium=10_000_000)
obs, _ = env.reset()  # Gymnasium reset returns (obs, info)

# === Load trained model ===
model_path = "models/ppo_treaty_agent.zip"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}. Did you run ppo_trainer.py first?")
model = PPO.load(model_path)
print("✅ Loaded trained PPO model")

# === Run simulation ===
retentions, limits, rewards = [], [], []

done = False
while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    done = terminated or truncated

    retentions.append(env.retention)
    limits.append(env.limit)
    rewards.append(reward)

# === Save results ===
results_df = pd.DataFrame({
    "Step": np.arange(len(rewards)),
    "Retention": retentions,
    "Limit": limits,
    "Reward": rewards
})
results_df.to_csv("data/ppo_simulation.csv", index=False)
print("✅ PPO simulation saved to data/ppo_simulation.csv")

# === Plot ===
plt.figure(figsize=(10, 4))
plt.plot(results_df["Step"], results_df["Reward"], label="Reward")
plt.xlabel("Step")
plt.ylabel("Reward")
plt.title("PPO Agent Reward Progression")
plt.grid(True)
plt.legend()
os.makedirs("outputs", exist_ok=True)
plt.savefig("outputs/ppo_reward_plot.png")
print("📈 Saved reward plot to outputs/ppo_reward_plot.png")

