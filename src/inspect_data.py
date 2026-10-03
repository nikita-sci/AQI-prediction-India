"""Looking through the raw data csv."""
from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

csv_files = sorted(RAW_DIR.glob("*.csv"))
if not csv_files:
    print(f"No CSV files found in {RAW_DIR}")

for path in csv_files:
    print("=" * 80)
    print("FILE:", path.name)
    df = pd.read_csv(path)

    print("\nShape (rows, columns):", df.shape)
    print("\nColumn names and types:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nMissing values per column:")
    print(df.isna().sum())
    print("\nDuplicate rows:", df.duplicated().sum())

    for col in df.columns:
        if col.lower() in ("city", "station", "stationid", "state"):
            print(f"\nUnique values in '{col}':", df[col].nunique())
            print(sorted(df[col].dropna().unique())[:40])

    for col in df.columns:
        if "date" in col.lower():
            dates = pd.to_datetime(df[col], errors="coerce")
            print(f"\nDate range in '{col}': {dates.min()} to {dates.max()}")

    for col in df.columns:
        if "bucket" in col.lower() or "category" in col.lower():
            print(f"\nValue counts for '{col}':")
            print(df[col].value_counts(dropna=False))