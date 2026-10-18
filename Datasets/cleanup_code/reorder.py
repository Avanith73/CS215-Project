import sys
import re
from pathlib import Path
import pandas as pd

# Usage: python reshape.py <input_dir_1> [<input_dir_2> ...] <output_dir>
# Defaults are used if no arguments are given.
args = sys.argv[1:]
if len(args) >= 2:
    in_dirs = [Path(a) for a in args[:-1]]
    out_root = Path(args[-1])
else:
    in_dirs = [Path("data/clean_a"), Path("data/clean_b")]
    out_root = Path("data/final")

# The only columns kept, in this order
FINAL_ORDER = ["Sr. No.", "Investment Date", "Startup Name", "Industry",
               "City", "Amount(in USD)", "Investment Stage"]

# Old column name (lowercase, letters and digits only) -> new name.
# Any column not listed here (Founding Date, Sub-Vertical, Founders, Investors, ...) is dropped.
RENAME_MAP = {
    "srno": "Sr. No.", "sno": "Sr. No.", "serialno": "Sr. No.", "slno": "Sr. No.",

    "date": "Investment Date", "dateddmmyyyy": "Investment Date",
    "investmentdate": "Investment Date",

    "startupname": "Startup Name", "startup": "Startup Name",

    "industryvertical": "Industry", "industry": "Industry", "verticals": "Industry",

    "city": "City", "citylocation": "City",

    "amountinusd": "Amount(in USD)", "amount": "Amount(in USD)", "amountusd": "Amount(in USD)",

    "investmenttype": "Investment Stage", "investmentstage": "Investment Stage",
    "stage": "Investment Stage",
}

def normalise(col):
    return re.sub(r"[^a-z0-9]", "", str(col).lower())

def read_csv(path):
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")

for in_dir in in_dirs:
    out_dir = out_root / in_dir.name          # one output subfolder per input folder
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n=== {in_dir} -> {out_dir} ===")

    for path in sorted(in_dir.glob("*.csv")):
        df = read_csv(path)

        new_cols = {}      # new name -> original column name
        dropped = []
        for col in df.columns:
            target = RENAME_MAP.get(normalise(col))
            if target and target not in new_cols:
                new_cols[target] = col
            else:
                dropped.append(col)

        out = pd.DataFrame(index=df.index)
        missing = []
        for name in FINAL_ORDER:
            if name in new_cols:
                out[name] = df[new_cols[name]]
            else:
                out[name] = pd.NA
                missing.append(name)

        out.to_csv(out_dir / path.name, index=False)

        print(f"{path.name}: {len(out)} rows")
        print(f"   dropped: {dropped}")
        if missing:
            print(f"   not found (left empty): {missing}")