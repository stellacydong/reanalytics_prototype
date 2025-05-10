# scripts/generate_synthetic_claims.py

import os
import numpy as np
import pandas as pd

# Resolve path to ../data/
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(os.path.dirname(script_dir), "data")
os.makedirs(output_dir, exist_ok=True)

# Config
n_claims = 5000
mean_claim = 1_000_000
heavy_tail = True  # Set to False for Normal distribution

# Generate claim amounts
if heavy_tail:
    # Simulate heavy-tailed distribution using Pareto
    alpha = 2.5  # lower alpha = heavier tail
    scale = mean_claim * (alpha - 1) / alpha
    claim_amounts = (np.random.pareto(alpha, n_claims) + 1) * scale
else:
    # Normally distributed claims
    claim_amounts = np.random.normal(loc=mean_claim, scale=300_000, size=n_claims)

# Clip outliers for realism
claim_amounts = np.clip(claim_amounts, 50_000, 10_000_000)

# Wrap in DataFrame
claims_df = pd.DataFrame({
    "claim_id": range(1, n_claims + 1),
    "amount": claim_amounts.round(2)
})

# Save CSV
output_file = os.path.join(output_dir, "synthetic_claims.csv")
claims_df.to_csv(output_file, index=False)

print(f"✅ Saved synthetic claims dataset: {output_file}")

