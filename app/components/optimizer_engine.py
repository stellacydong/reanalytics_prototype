# app/components/optimizer_engine.py

import os
import json
from models.portfolio_aggregator import PortfolioAggregator
from models.portfolio_optimizer.ppo_trainer import PPOTrainer

def optimize_portfolio():
    """
    High-level function to aggregate treaties, train PPO agent, and optimize portfolio.

    Returns:
    - dict: { 'original_portfolio': [...], 'optimized_portfolio': [...] }
    """
    # Step 1: Aggregate treaties into a portfolio
    aggregator = PortfolioAggregator()
    original_portfolio = aggregator.build_portfolio()

    # Step 2: Train PPO agent
    trainer = PPOTrainer()
    trainer.train(timesteps=5000)

    # Step 3: Optimize the portfolio
    optimized_portfolio = trainer.optimize_portfolio()

    # Save optimized portfolio to JSON file
    os.makedirs("data/portfolios", exist_ok=True)
    with open("data/portfolios/optimized_portfolio.json", "w", encoding="utf-8") as f:
        json.dump(optimized_portfolio, f, indent=4)

    return {
        "original_portfolio": original_portfolio,
        "optimized_portfolio": optimized_portfolio
    }

# Example Usage
if __name__ == "__main__":
    result = optimize_portfolio()
    print("Original Portfolio:")
    print(json.dumps(result["original_portfolio"], indent=2))
    print("Optimized Portfolio:")
    print(json.dumps(result["optimized_portfolio"], indent=2))
