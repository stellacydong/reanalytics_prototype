import os
import pandas as pd
import matplotlib.pyplot as plt

# Locate paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_path = os.path.join(project_root, "data", "synthetic_claims.csv")
output_dir = os.path.join(project_root, "outputs")
output_path = os.path.join(output_dir, "claim_distribution.png")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the claims data
claims_df = pd.read_csv(data_path)

# Plot histogram
plt.figure(figsize=(10, 6))
plt.hist(claims_df['amount'], bins=50, color='steelblue', edgecolor='black')
plt.title("Distribution of Synthetic Claim Amounts")
plt.xlabel("Claim Amount ($)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()

# Save the plot
plt.savefig(output_path)
print(f"✅ Histogram saved to {output_path}")

