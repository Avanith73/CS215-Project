import sys
from pathlib import Path
import pandas as pd

# Usage: python merge.py <input_dir> <output_file>
in_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "../cleaned")
out_file = Path(sys.argv[2] if len(sys.argv) > 2 else "../merged.csv")
out_file.parent.mkdir(parents=True, exist_ok=True)

SERIAL_COL = "Sr. No."

def read_csv(path):
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")

files = sorted(in_dir.glob("*.csv"))
if not files:
    sys.exit(f"No CSV files found in {in_dir}")

frames = []
for path in files:
    df = read_csv(path)
    frames.append(df)
    print(f"{path.name}: {len(df)} rows, {len(df.columns) - 1} columns")

# Columns are matched by name; any column missing from a file is filled with empty values
merged = pd.concat(frames, ignore_index=True)

# Renumber the serial column from 1 across the whole merged file
if SERIAL_COL in merged.columns:
    merged = merged.drop(columns=[SERIAL_COL])
merged.insert(0, SERIAL_COL, range(1, len(merged) + 1))

merged.to_csv(out_file, index=False)
merged.duplicated(subset=["Startup Name", "Investment Date", "Amount(in USD)"]).sum()
print(f"\nMerged {len(files)} files -> {out_file} ({len(merged)} rows)")