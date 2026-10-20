import sys
from pathlib import Path
import pandas as pd

folder = Path(sys.argv[1] if len(sys.argv) > 1 else "../raw")

for path in sorted(folder.glob("*.csv")):   # use rglob("*.csv") to include subfolders
    try:
        cols = pd.read_csv(path, nrows=0).columns.tolist()
    except UnicodeDecodeError:
        cols = pd.read_csv(path, nrows=0, encoding="latin-1").columns.tolist()

    print(f"\n{path.name} ({len(cols)} columns)")
    for c in cols:
        print(f"  - {c!r}")