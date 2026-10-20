import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

in_file = Path(sys.argv[1] if len(sys.argv) > 1 else "data/merged.csv")

AMOUNT_COL = "Amount(in USD)"

def read_csv(path):
    try:
        return pd.read_csv(path, dtype=str)
    except UnicodeDecodeError:
        return pd.read_csv(path, dtype=str, encoding="latin-1")

def clean_amount(series):
    s = series.astype("string").str.strip()
    s = s.str.replace(r"(?i)usd|[$,\s]", "", regex=True)
    nums = pd.to_numeric(s, errors="coerce")
    nums = nums.replace([np.inf, -np.inf], np.nan)
    rounded = np.floor(nums + 0.5).astype("Int64")
    return rounded.astype("string").fillna("Undisclosed")

df = read_csv(in_file)

if AMOUNT_COL not in df.columns:
    sys.exit(f"Column '{AMOUNT_COL}' not found. Columns are: {list(df.columns)}")

df[AMOUNT_COL] = clean_amount(df[AMOUNT_COL])

tmp_file = in_file.with_suffix(".tmp")
df.to_csv(tmp_file, index=False)
os.replace(tmp_file, in_file)          

n_undisclosed = (df[AMOUNT_COL] == "Undisclosed").sum()
print(f"{in_file.name}: {len(df)} rows, {n_undisclosed} undisclosed (file overwritten)")
