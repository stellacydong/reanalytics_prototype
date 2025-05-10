import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import os
from pathlib import Path
import gymnasium as gym
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_checker import check_env

from models.ppo_structuring_agent import TreatyStructuringEnv

# === Config ===
BASE_DIR = Path(__file__).resolve().parent.parent
CLAIMS_FILE = BASE_DIR / "data" / "synthetic_claims.csv"
MODEL_PATH = BASE_DIR / "models" / "ppo_treaty_agent.zip"
LOG_DIR = BASE_DIR / "outputs" / "training_logs"
TOTAL_TIMESTEPS = 100_000
SEED = 42


def make_env() -> gym.Env:
    """Create a new instance of the TreatyStructuringEnv."""
    return TreatyStructuringEnv(claims_file=str(CLAIMS_FILE))


def main() -> None:
    """Train and evaluate a PPO agent on the treaty structuring environment."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize environment
    env = make_env()
    check_env(env, warn=True)

    print("🚀 Starting PPO training...")
    model = PPO(
        policy="MlpPolicy",
        env=env,
        seed=SEED,
        verbose=1,
        tensorboard_log=str(LOG_DIR),
        n_steps=2048,
        batch_size=64,
        learning_rate=3e-4,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01
    )

    # Optional evaluation callback
    eval_env = make_env()
    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=str(LOG_DIR),
        log_path=str(LOG_DIR),
        eval_freq=5000,
        deterministic=True,
        render=False
    )

    # Train model
    model.learn(total_timesteps=TOTAL_TIMESTEPS, callback=eval_callback)

    # Save model
    model.save(str(MODEL_PATH))
    print(f"✅ Trained PPO model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
