
from pathlib import Path
import pandas as pd

SOURCE_DIR = Path("Datasets/cleaned_by_year")
OUTPUT_FILE = Path("Datasets/merged.csv")

files = sorted(SOURCE_DIR.glob("Startup_Funding_Cleaned_*.csv"))

if not files:
    raise FileNotFoundError(f"No yearly CSV files found in {SOURCE_DIR}")

frames = []

for file in files:
    df = pd.read_csv(file, skipinitialspace=True)
    df.columns = df.columns.astype(str).str.strip()

    print(f"{file.name}: {len(df)} rows, {len(df.columns)} columns")
    frames.append(df)

# All source files must have the same column structure.
expected_columns = list(frames[0].columns)

for file, df in zip(files, frames):
    if list(df.columns) != expected_columns:
        raise ValueError(
            f"Column mismatch in {file.name}\n"
            f"Expected: {expected_columns}\n"
            f"Found: {list(df.columns)}"
        )

merged = pd.concat(frames, ignore_index=True)
merged.to_csv(OUTPUT_FILE, index=False)

print(f"\nRebuilt: {OUTPUT_FILE}")
print(f"Total rows: {len(merged)}")
print(f"Columns: {merged.columns.tolist()}")
