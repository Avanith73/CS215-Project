import pandas as pd
from pathlib import Path

file = Path("Datasets/cleaned_by_year/Startup_Funding_Cleaned_2018.csv")

df = pd.read_csv(file)

# Renumber serial numbers from 1
df["Sr. No."] = range(1, len(df) + 1)

# Save back to the same file
df.to_csv(file, index=False)

print(f"Done! Updated {len(df)} serial numbers.")