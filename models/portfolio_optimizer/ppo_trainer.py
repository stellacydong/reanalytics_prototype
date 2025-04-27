# models/portfolio_optimizer/ppo_trainer.py

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from models.portfolio_optimizer.optimizer_env import PortfolioOptimizerEnv
import os
import json

class PPOTrainer:
    """
    Class to handle PPO agent training and suggesting optimized portfolios.
    """

    def __init__(self, portfolio_path="data/portfolios/original_portfolio.json", model_save_path="models/ppo_agent"):
        self.portfolio_path = portfolio_path
        self.model_save_path = model_save_path

        # Load portfolio
        with open(self.portfolio_path, "r") as f:
            self.portfolio_data = json.load(f)

        # Create environment
        self.env = make_vec_env(lambda: PortfolioOptimizerEnv(self.portfolio_data), n_envs=1)

        # Create PPO model
        self.model = PPO("MlpPolicy", self.env, verbose=1)

        # Create save path
        os.makedirs(self.model_save_path, exist_ok=True)

    def train(self, timesteps=10000):
        """
        Train PPO agent.
        """
        self.model.learn(total_timesteps=timesteps)
        self.model.save(os.path.join(self.model_save_path, "ppo_portfolio_optimizer"))

    def optimize_portfolio(self):
        """
        Use trained PPO agent to suggest optimized actions.

        Returns:
        - list of optimized portfolio treaties.
        """
        env = PortfolioOptimizerEnv(self.portfolio_data)
        obs, _ = env.reset()
        action, _ = self.model.predict(obs, deterministic=True)
        env.step(action)

        optimized_portfolio = env.current_portfolio
        return optimized_portfolio

# Example usage
if __name__ == "__main__":
    trainer = PPOTrainer()
    trainer.train(timesteps=5000)
    optimized_portfolio = trainer.optimize_portfolio()

    # Save optimized portfolio
    os.makedirs("data/portfolios", exist_ok=True)
    with open("data/portfolios/optimized_portfolio.json", "w") as f:
        json.dump(optimized_portfolio, f, indent=4)

    print("Optimized Portfolio Saved!")
