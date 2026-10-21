import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_csv("Datasets/unicorn.csv")
df["country"] = df["country"].str.strip()
df["location"] = df["location"].str.strip()
def clean_location(row):
    if pd.isna(row["country"]):
        return row["location"]
    if row["country"].lower() != "india":
        return "Abroad"
    return row["location"]


df["cleaned_location"] = df.apply(clean_location, axis=1)

plt.figure(figsize=(12, 7))
city_order = df["cleaned_location"].value_counts().index

sns.countplot(
    data=df,
    x="cleaned_location",
    order=city_order,
    palette="Set2",
    edgecolor="black",
)

plt.title(
    "Number of Indian-Founded Unicorns by Location Hub",
    fontsize=14,
    pad=15,
    fontweight="bold",
)
plt.xlabel("Location Hub (City / Abroad)", fontsize=12)
plt.ylabel("Number of Companies (Unicorn Count)", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()
