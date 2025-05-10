# scripts/plot_claims_distribution.py

import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_distribution(input_csv="data/synthetic_claims.csv", output_file="outputs/claim_distribution.png"):
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Missing input file: {input_csv}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df = pd.read_csv(input_csv)

    plt.figure(figsize=(10, 6))
    plt.hist(df['amount'], bins=50, color='skyblue', edgecolor='black')
    plt.title("Distribution of Synthetic Claim Amounts")
    plt.xlabel("Claim Amount ($)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)

    print(f"📊 Saved distribution plot → {output_file}")

if __name__ == "__main__":
    plot_distribution()
