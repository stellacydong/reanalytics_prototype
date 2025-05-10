import os
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from ppo_structuring_agent import TreatyStructuringEnv

def train_ppo_agent():
    # Load synthetic claims
    claims_path = os.path.join("data", "synthetic_claims.csv")
    if not os.path.exists(claims_path):
        raise FileNotFoundError(f"Claims file not found: {claims_path}")

    claims_df = pd.read_csv(claims_path)

    # Initialize environment
    env = TreatyStructuringEnv(claims_df=claims_df, premium=10_000_000)
    check_env(env, warn=True)

    # Wrap for training
    env = Monitor(env)
    env = DummyVecEnv([lambda: env])

    # Train PPO agent
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=20_000)

    # Ensure models directory exists
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "ppo_treaty_agent.zip")
    model.save(model_path)

    print(f"✅ PPO model trained and saved to: {model_path}")

if __name__ == "__main__":
    train_ppo_agent()
