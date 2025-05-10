# app/components/optimizer_engine.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models')))

from ppo_structuring_agent import TreatyStructuringEnv


import os
import pandas as pd
from stable_baselines3 import PPO

def run_treaty_optimizer(treaty_text):
    # Placeholder logic – replace with PPO + Mistral inference later
    suggestion = {
        "recommendation": "Increase retention to $2M for better capital efficiency.",
        "confidence": 0.85,
        "summary": "Based on historical claim volatility and treaty structure, a higher retention improves risk-adjusted return."
    }
    return suggestion


def load_claims_data(path="data/synthetic_claims.csv"):
    """
    Load claims data from CSV file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Claims file not found at {path}")
    return pd.read_csv(path)

def load_trained_model(path="models/ppo_treaty_agent.zip"):
    """
    Load a trained PPO model from file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"PPO model file not found at {path}")
    return PPO.load(path)

def run_optimizer(claims_path="data/synthetic_claims.csv", premium=10_000_000, max_steps=10):
    """
    Run the PPO agent in a simulation environment to get treaty recommendations.

    Returns:
        dict with optimized treaty parameters and performance
    """
    claims_df = load_claims_data(claims_path)
    env = TreatyStructuringEnv(claims_df=claims_df, premium=premium)
    model = load_trained_model()

    obs, _ = env.reset()
    history = []

    for _ in range(max_steps):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)
        history.append({
            "step": len(history) + 1,
            "retention": env.retention,
            "limit": env.limit,
            "reward": reward
        })
        if terminated or truncated:
            break

    final = history[-1]
    return {
        "retention": f"${final['retention']:,.0f}",
        "limit": f"${final['limit']:,.0f}",
        "cumulative_reward": round(sum([h["reward"] for h in history]), 2),
        "steps_taken": len(history)
    }
