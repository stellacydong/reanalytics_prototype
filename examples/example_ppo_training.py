
# examples/example_ppo_training.py

import numpy as np
from app.models.ppo_reserving_agent import PPOReserveAgent

def main():
    # Create a PPO agent
    agent = PPOReserveAgent()

    # Synthetic claims data
    incurred_losses = np.random.randint(500_000, 5_000_000, size=100)
    true_reserves = incurred_losses * np.random.uniform(0.8, 1.2, size=100)  # simulate 'true' needs

    # Initial performance
    initial_preds = np.array([agent.predict_reserve(x) for x in incurred_losses])
    initial_mse = np.mean((initial_preds - true_reserves)**2)
    print(f"Initial MSE: {initial_mse:.2f}")

    # Train for a few epochs
    for epoch in range(20):
        agent.update_policy(incurred_losses, true_reserves)

    # Final performance
    final_preds = np.array([agent.predict_reserve(x) for x in incurred_losses])
    final_mse = np.mean((final_preds - true_reserves)**2)
    print(f"Final MSE after training: {final_mse:.2f}")

if __name__ == "__main__":
    main()
