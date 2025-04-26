# models/ppo_reserving_agent.py

import numpy as np

class PPOReserveAgent:
    """
    A simple PPO-like agent to optimize reserve predictions based on incurred losses.
    """

    def __init__(self, gamma=0.99, epsilon=0.2, lr=0.001):
        """
        Initialize the PPO Reserve Agent.

        Parameters:
        - gamma (float): Discount factor (not heavily used in static claim setting).
        - epsilon (float): Clipping range for policy updates (PPO idea).
        - lr (float): Learning rate for adjusting policy weight.
        """
        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.policy_weight = np.random.uniform(0.5, 1.5)  # start randomly

    def predict_reserve(self, incurred_loss):
        """
        Predict reserve for a given incurred loss.
        """
        return self.policy_weight * incurred_loss

    def update_policy(self, incurred_losses, targets):
        """
        Update the policy weight using a simple PPO-like gradient step.

        Parameters:
        - incurred_losses (np.array): Array of incurred losses.
        - targets (np.array): Array of 'true' or ideal reserve targets.
        """
        preds = np.array([self.predict_reserve(x) for x in incurred_losses])
        advantages = targets - preds  # Simple advantage estimation

        # Basic policy gradient update
        gradient = np.mean(advantages * incurred_losses)
        self.policy_weight += self.lr * gradient

        # PPO-style clipping
        self.policy_weight = np.clip(self.policy_weight, 0.5, 2.0)

    def evaluate_mse(self, incurred_losses, targets):
        """
        Evaluate the mean squared error between predictions and targets.
        """
        preds = np.array([self.predict_reserve(x) for x in incurred_losses])
        return np.mean((preds - targets) ** 2)

