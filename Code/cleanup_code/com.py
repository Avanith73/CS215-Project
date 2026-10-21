
import pandas as pd

INPUT_FILE = "Datasets/merged_city_cleaned.csv"
OUTPUT_FILE = "Datasets/city_values_to_review.csv"

df = pd.read_csv(INPUT_FILE, skipinitialspace=True)
df.columns = df.columns.str.strip()

if "City" not in df.columns:
    raise ValueError(f"City column not found: {df.columns.tolist()}")

cities = (
    df["City"]
    .fillna("")
    .astype(str)
    .str.strip()
    .replace("", "(blank)")
    .value_counts()
    .rename_axis("Original City")
    .reset_index(name="Count")
)

cities.to_csv(OUTPUT_FILE, index=False)

print(f"Total distinct city values: {len(cities)}")
print(f"Saved full list to: {OUTPUT_FILE}")
print(cities.to_string(index=False))
