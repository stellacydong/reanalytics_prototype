# scripts/generate_synthetic_claims.py

import os
import numpy as np
import pandas as pd

def generate_claims(output_file="data/synthetic_claims.csv", n_claims=5000, mean_claim=1_000_000, heavy_tail=True):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if heavy_tail:
        alpha = 2.5
        scale = mean_claim * (alpha - 1) / alpha
        claim_amounts = (np.random.pareto(alpha, n_claims) + 1) * scale
    else:
        claim_amounts = np.random.normal(loc=mean_claim, scale=300_000, size=n_claims)

    claim_amounts = np.clip(claim_amounts, 50_000, 10_000_000)

    df = pd.DataFrame({
        "claim_id": np.arange(1, n_claims + 1),
        "amount": claim_amounts.round(2)
    })

    df.to_csv(output_file, index=False)
    print(f"✅ Generated {n_claims} claims → {output_file}")

if __name__ == "__main__":
    generate_claims()
