import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces

class TreatyStructuringEnv(gym.Env):
    """
    Custom environment for optimizing reinsurance treaty structures.
    The agent sets retention and limit to maximize profit while controlling risk.
    """

    def __init__(self, claims_file="data/synthetic_claims.csv", max_retention=10_000_000, max_limit=50_000_000):
        super(TreatyStructuringEnv, self).__init__()

        # Load claims data
        self.claims_df = pd.read_csv(claims_file)
        self.claims = self.claims_df["amount"].values

        # Action space: [Retention, Limit], normalized [0, 1]
        self.action_space = spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32)

        # Observation space: static for now — mean, std of claims
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(2,), dtype=np.float32
        )

        self.max_retention = max_retention
        self.max_limit = max_limit
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.current_step = 0
        self.done = False

        # Random sample of claims for this episode
        self.sampled_claims = np.random.choice(self.claims, size=50, replace=True)

        # Simple observation: [mean, std]
        obs = np.array([
            np.mean(self.sampled_claims),
            np.std(self.sampled_claims)
        ], dtype=np.float32)

        return obs, {}

    def step(self, action):
        retention_ratio, limit_ratio = action
        self.retention = retention_ratio * self.max_retention
        self.limit = limit_ratio * self.max_limit

        if self.retention >= self.limit:
            reward = -1.0
            done = True
            return self._get_obs(), reward, done, False, {}

        payout = np.clip(self.sampled_claims - self.retention, 0, self.limit - self.retention)
        total_payout = np.sum(payout)

        base_premium_rate = 0.12
        premium = base_premium_rate * (self.limit - self.retention)

        underwriting_profit = premium - total_payout
        penalty = -0.01 * retention_ratio

        reward = underwriting_profit + penalty
        done = True

        return self._get_obs(), reward, done, False, {
            "retention": self.retention,
            "limit": self.limit,
            "profit": underwriting_profit,
            "payout": total_payout
        }


    def _get_obs(self):
        return np.array([
            np.mean(self.sampled_claims),
            np.std(self.sampled_claims)
        ], dtype=np.float32)
