import sys
import re
from pathlib import Path
import pandas as pd

in_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw")
out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "data/clean")
out_dir.mkdir(parents=True, exist_ok=True)

TARGET_NAME = "Sr. No."

# Possible names for the serial-number column (compared case-insensitively)
SERIAL_NAMES = {"sno", "s.no", "s.no.", "sr no", "sr.no", "sr. no.", "sr.no.",
                "serial", "serial no", "serial number", "sl no"}

def is_serial(col):
    name = str(col).strip().lower()
    return name in SERIAL_NAMES or re.fullmatch(r"unnamed: \d+", name) is not None

def read_csv(path):
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")

for path in sorted(in_dir.glob("*.csv")):
    df = read_csv(path)

    serial_cols = [c for c in df.columns if is_serial(c)]

    if not serial_cols:
        df.insert(0, TARGET_NAME, range(1, len(df) + 1))
        action = f"added '{TARGET_NAME}'"
    else:
        # Keep the column already named Sr. No. if present, otherwise the first match
        keep = TARGET_NAME if TARGET_NAME in serial_cols else serial_cols[0]
        drop = [c for c in serial_cols if c != keep]

        df = df.drop(columns=drop)
        df[keep] = range(1, len(df) + 1)
        if keep != TARGET_NAME:
            df = df.rename(columns={keep: TARGET_NAME})

        # Make sure Sr. No. is the first column
        df = df[[TARGET_NAME] + [c for c in df.columns if c != TARGET_NAME]]

        action = f"kept '{keep}' as '{TARGET_NAME}', dropped {drop if drop else 'nothing'}"

    df.to_csv(out_dir / path.name, index=False)
    print(f"{path.name}: {action} (1 to {len(df)})")