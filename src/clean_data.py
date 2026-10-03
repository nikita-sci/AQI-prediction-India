"""Clean data/raw/city_day.csv and save the result as a CSV and a SQLite database."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = ROOT / "data" / "raw" / "city_day.csv"
CLEAN_DIR = ROOT / "data" / "Cleaned"
CLEAN_CSV = CLEAN_DIR / "city_day_clean.csv"
DB_FILE = CLEAN_DIR / "aqi.db"

# Diwali dates for the years in the data (flag +/- 3 days around each)
DIWALI_DATES = pd.to_datetime([
    "2015-11-11", "2016-10-30", "2017-10-19",
    "2018-11-07", "2019-10-27", "2020-11-14",
])


def get_season(month: int) -> str:
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Summer"
    if month in (6, 7, 8, 9):
        return "Monsoon"
    return "Post-monsoon"  # Oct, Nov


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load
    df = pd.read_csv(RAW_FILE)
    print(f"Loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Standardise city names and parse dates (explicit format avoids day/month swaps)
    df["City"] = df["City"].str.strip()
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
    bad_dates = df["Date"].isna().sum()
    df = df.dropna(subset=["Date"])
    print(f"Dropped {bad_dates} rows with unreadable dates")

    # 3. Remove duplicate city-day rows
    before = len(df)
    df = df.drop_duplicates(subset=["City", "Date"], keep="first")
    print(f"Dropped {before - len(df)} duplicate city-day rows")

    # 4. Drop Xylene (about 61% missing)
    df = df.drop(columns=["Xylene"])
    
    # 4b. Drop rows where every pollutant reading is blank
    pollutants = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene"]
    before = len(df)
    df = df.dropna(subset=pollutants, how="all")
    print(f"Dropped {before - len(df)} rows with no pollutant readings")

    # 5. Drop rows with no AQI (no target to learn from)
    before = len(df)
    df = df.dropna(subset=["AQI", "AQI_Bucket"])
    print(f"Dropped {before - len(df)} rows with missing AQI")

    # 6. Sort so each city's days are in order
    df = df.sort_values(["City", "Date"]).reset_index(drop=True)

    # 7. Date features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.weekday          # 0 = Monday ... 6 = Sunday
    df["Is_Weekend"] = (df["Weekday"] >= 5).astype(int)
    df["Season"] = df["Month"].apply(get_season)
    df["Is_Winter"] = (df["Season"] == "Winter").astype(int)

    df["Is_Diwali_Period"] = 0
    for diwali in DIWALI_DATES:
        near = (df["Date"] - diwali).abs() <= pd.Timedelta(days=3)
        df.loc[near, "Is_Diwali_Period"] = 1

    # 8. Save as CSV
    df.to_csv(CLEAN_CSV, index=False)
    print(f"\nSaved CSV: {CLEAN_CSV}")

    # 9. Save into SQLite (dates stored as text)
    df_db = df.copy()
    df_db["Date"] = df_db["Date"].dt.strftime("%Y-%m-%d")
    with sqlite3.connect(DB_FILE) as conn:
        df_db.to_sql("city_day_clean", conn, if_exists="replace", index=False)
        check = pd.read_sql_query(
            "SELECT City, COUNT(*) AS days, ROUND(AVG(AQI), 1) AS avg_aqi "
            "FROM city_day_clean GROUP BY City ORDER BY avg_aqi DESC LIMIT 5",
            conn,
        )
    print(f"Saved SQLite database: {DB_FILE}")
    print("\nSQL check - 5 cities with the highest average AQI:")
    print(check)

    # 10. Summary
    print("\n--- Cleaned data summary ---")
    print("Shape:", df.shape)
    print("Date range:", df["Date"].min().date(), "to", df["Date"].max().date())
    print("Cities:", df["City"].nunique())
    print("\nAQI_Bucket counts:")
    print(df["AQI_Bucket"].value_counts())
    print("\nMissing values left (filled later in the models):")
    print(df.isna().sum()[df.isna().sum() > 0])


if __name__ == "__main__":
    main()