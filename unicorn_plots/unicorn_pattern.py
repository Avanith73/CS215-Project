import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
df = pd.read_csv("Datasets/unicorn.csv")
df_financials = df.dropna(subset=["valuation_cr", "annual_revenue_cr"])
df_financials = df_financials[df_financials["annual_revenue_cr"] > 0]

plt.figure(figsize=(11, 7))

sns.scatterplot(
    data=df_financials,
    x="annual_revenue_cr",
    y="valuation_cr",
    hue="primary_sector",  
    alpha=0.8,
    s=120,
    edgecolor="black",
    palette="tab20",
)

plt.xscale("log")
plt.yscale("log")
plt.axhline(
    y=8400,
    color="crimson",
    linestyle="--",
    linewidth=2,
    label="True Unicorn Threshold (~₹8,400 Cr / $1B)",
)

plt.title(
    "The Unicorn Formula: Valuation vs. Annual Revenue (Log Scale)",
    fontsize=14,
    pad=15,
    fontweight="bold",
)
plt.xlabel("Annual Revenue (in Crores - Log Scale)", fontsize=12)
plt.ylabel("Valuation (in Crores - Log Scale)", fontsize=12)
plt.grid(True, which="both", linestyle=":", alpha=0.5)
plt.legend(
    title="Primary Sector",
    fontsize=9,
    title_fontsize=10,
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
)

plt.tight_layout()
plt.show()
