import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/ppo_simulation.csv")

plt.plot(df["retention"], label="Retention")
plt.plot(df["limit"], label="Limit")
plt.xlabel("Step")
plt.ylabel("Amount ($)")
plt.title("PPO Optimized Treaty Terms")
plt.legend()
plt.grid(True)
plt.show()

