import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv("Datasets/unicorn.csv")
df["primary_sector"] = df["primary_sector"].str.strip()

plt.figure(figsize=(12, 7))
sector_order = df["primary_sector"].value_counts().index
sns.countplot(
    data=df,
    x="primary_sector",
    order=sector_order,
    palette="Set2",
    edgecolor="black",
)

plt.title(
    "Number of Indian-Founded Unicorns by Sector",
    fontsize=14,
    pad=15,
    fontweight="bold",
)
plt.xlabel("Primary Sector", fontsize=12)
plt.ylabel("Number of Companies (Unicorn Count)", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()
