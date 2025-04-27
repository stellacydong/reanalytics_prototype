# models/portfolio_optimizer/optimizer_env.py

import numpy as np
import gymnasium as gym
from gymnasium import spaces

class PortfolioOptimizerEnv(gym.Env):
    """
    Custom Environment for Treaty Portfolio Optimization using PPO.
    """

    def __init__(self, portfolio_data):
        super(PortfolioOptimizerEnv, self).__init__()

        self.original_portfolio = portfolio_data
        self.current_portfolio = portfolio_data.copy()
        self.num_treaties = len(portfolio_data)

        # Actions: for each treaty, 0 = do nothing, 1 = lower retention, 2 = increase limit
        self.action_space = spaces.MultiDiscrete([3] * self.num_treaties)

        # Observations: retention and limit for each treaty
        self.observation_space = spaces.Box(low=0, high=1e9, shape=(self.num_treaties * 2,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_portfolio = [t.copy() for t in self.original_portfolio]
        return self._get_obs(), {}

    def _get_obs(self):
        obs = []
        for treaty in self.current_portfolio:
            obs.append(treaty.get("retention", 0))
            obs.append(treaty.get("limit", 0))
        return np.array(obs, dtype=np.float32)

    def step(self, action):
        # Apply action to the portfolio
        for idx, act in enumerate(action):
            if act == 1:  # lower retention
                self.current_portfolio[idx]["retention"] = max(0, self.current_portfolio[idx]["retention"] * 0.9)
            elif act == 2:  # increase limit
                self.current_portfolio[idx]["limit"] = self.current_portfolio[idx]["limit"] * 1.1

        reward = self._calculate_reward()
        done = True  # One step environment for now
        return self._get_obs(), reward, done, False, {}

    def _calculate_reward(self):
        # Dummy reward: Encourage lower retention and higher limits
        capital_efficiency = 0
        for treaty in self.current_portfolio:
            retention = treaty.get("retention", 1)
            limit = treaty.get("limit", 1)
            capital_efficiency += (limit / retention)
        reward = capital_efficiency / self.num_treaties
        return reward

