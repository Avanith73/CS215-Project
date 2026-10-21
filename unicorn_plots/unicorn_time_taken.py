import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm
df = pd.read_csv("Datasets/unicorn.csv")
def parse_time_to_years(time_str):
    if pd.isna(time_str):
        return np.nan
    years_match = re.search(r"(\d+)\s*year", str(time_str))
    months_match = re.search(r"(\d+)\s*month", str(time_str))
    years = int(years_match.group(1)) if years_match else 0
    months = int(months_match.group(1)) if months_match else 0
    return years + (months / 12.0)

df["years_to_unicorn"] = df["time_to_unicorn"].apply(parse_time_to_years)
years_data = df["years_to_unicorn"].dropna()
mu, sigma = norm.fit(years_data)
plt.figure(figsize=(10, 6))
sns.histplot(
    years_data,
    kde=False,
    stat="density",
    color="skyblue",
    bins=10,
    edgecolor="black",
    label="Actual Data Distribution",
)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, sigma)
label_text = f"Normal Curve Fit\n($\mu$={mu:.2f} yrs, $\sigma$={sigma:.2f} yrs)"
plt.plot(x, p, "r-", linewidth=2.5, label=label_text)
plt.title(
    "Distribution of Time Taken to Reach Unicorn Status",
    fontsize=14,
    pad=15,
)
plt.xlabel("Years to Reach Unicorn Status", fontsize=12)
plt.ylabel("Probability Density", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend(fontsize=11)

plt.tight_layout()
plt.show()
