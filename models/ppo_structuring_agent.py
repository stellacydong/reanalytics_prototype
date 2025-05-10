# models/ppo_structuring_agent.py
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import pandas as pd

class TreatyStructuringEnv(gym.Env):
    """
    A custom environment to simulate treaty structuring decisions in reinsurance.
    The agent adjusts retention and limit levels to maximize expected profit.
    """

    def __init__(self, claims_df: pd.DataFrame, premium: float = 10_000_000):
        super(TreatyStructuringEnv, self).__init__()

        self.claims_df = claims_df
        self.premium = premium
        self.current_step = 0
        self.n_steps = 10

        # Action space: [delta_retention, delta_limit] — normalized [-1, 1]
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        # Observation space: [retention, limit, step, loss_ratio_stats...]
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(4,), dtype=np.float32)

        self.reset()

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.retention = 1_000_000
        self.limit = 5_000_000
        self.stats = self.claims_df["amount"].describe()
        return self._get_obs(), {}

    def _get_obs(self):
        return np.array([
            self.retention / 10_000_000,
            self.limit / 10_000_000,
            self.current_step / self.n_steps,
            self.stats['mean'] / 10_000_000
        ], dtype=np.float32)

    def step(self, action):
        # Update retention and limit
        self.retention += float(action[0]) * 0.1e6
        self.limit += float(action[1]) * 0.1e6

        self.retention = max(100_000, min(self.retention, 10_000_000))
        self.limit = max(self.retention + 100_000, min(self.limit, 20_000_000))

        # Apply to claims
        covered_losses = self.claims_df["amount"].clip(lower=self.retention, upper=self.retention + self.limit)
        payout = covered_losses - self.retention
        payout = payout.clip(lower=0)
        total_payout = payout.sum()

        # Reward = premium - losses paid (simplified)
        reward = self.premium - total_payout

        self.current_step += 1
        done = self.current_step >= self.n_steps
        info = {}

        return self._get_obs(), reward, done, False, info
