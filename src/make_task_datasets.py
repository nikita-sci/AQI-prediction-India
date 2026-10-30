"""We now take the cleaned data sets and use thatto divide it into 3 separate datasets for 3 different workings: i.e Regression, classification and Time series forecasting."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CLEAN_DIR = ROOT / "data" / "Cleaned"
BASE_CSV = CLEAN_DIR / "city_day_clean.csv"
DB_FILE = CLEAN_DIR / "aqi.db"

POLLUTANTS = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene"]
DATE_FEATURES = ["Year", "Month", "Weekday", "Is_Weekend", "Season", "Is_Winter", "Is_Diwali_Period"]
SPLIT_DATE = pd.Timestamp("2019-01-01")  # before = Train, on/after = Test
BUCKET_ORDER = {"Good": 0, "Satisfactory": 1, "Moderate": 2, "Poor": 3, "Very Poor": 4, "Severe": 5}


def add_split(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Split"] = (df["Date"] >= SPLIT_DATE).map({False: "Train", True: "Test"})
    return df


def impute_from_train(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Fill missing values: city+month median -> city median -> overall median.
    All medians come from TRAIN rows only, so nothing leaks from the test set."""
    df = df.copy()
    train = df[df["Split"] == "Train"]
    city_month = train.groupby(["City", "Month"])[cols].median()
    city = train.groupby("City")[cols].median()
    overall = train[cols].median()
    keys = pd.MultiIndex.from_frame(df[["City", "Month"]])
    for col in cols:
        by_city_month = pd.Series(city_month[col].reindex(keys).values, index=df.index)
        df[col] = df[col].fillna(by_city_month)
        df[col] = df[col].fillna(df["City"].map(city[col]))
        df[col] = df[col].fillna(overall[col])
    return df


def build_regression(base: pd.DataFrame) -> pd.DataFrame:
    df = impute_from_train(add_split(base), POLLUTANTS)
    cols = ["City", "Date", "Split"] + POLLUTANTS + DATE_FEATURES + ["AQI"]
    return df[cols]


def build_classification(base: pd.DataFrame) -> pd.DataFrame:
    df = impute_from_train(add_split(base), POLLUTANTS)
    df["AQI_Bucket"] = df["AQI_Bucket"].str.strip()
    df["AQI_Bucket_Code"] = df["AQI_Bucket"].map(BUCKET_ORDER)
    df = df.dropna(subset=["AQI_Bucket_Code"])
    df["AQI_Bucket_Code"] = df["AQI_Bucket_Code"].astype(int)
    # AQI number is deliberately left out: the category is calculated from it
    cols = ["City", "Date", "Split"] + POLLUTANTS + DATE_FEATURES + ["AQI_Bucket", "AQI_Bucket_Code"]
    return df[cols]


def build_timeseries(base: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for city, g in base.groupby("City"):
        g = g.set_index("Date").sort_index()
        # Insert a row for every calendar day so missing days become visible gaps
        g = g.reindex(pd.date_range(g.index.min(), g.index.max(), freq="D"))
        g["City"] = city
        g["AQI_Lag1"] = g["AQI"].shift(1)
        g["AQI_Lag2"] = g["AQI"].shift(2)
        g["AQI_Lag3"] = g["AQI"].shift(3)
        g["AQI_Last7_Mean"] = g["AQI"].rolling(7, min_periods=4).mean()
        g["AQI_Next_Day"] = g["AQI"].shift(-1)
        frames.append(g.rename_axis("Date").reset_index())
    ts = pd.concat(frames, ignore_index=True)

    # Keep only real days that have a full history and a known next day
    needed = ["AQI", "AQI_Lag1", "AQI_Lag2", "AQI_Lag3", "AQI_Last7_Mean", "AQI_Next_Day"]
    ts = ts.dropna(subset=needed)
    for col in ["Year", "Month", "Weekday", "Is_Weekend", "Is_Winter", "Is_Diwali_Period"]:
        ts[col] = ts[col].astype(int)

    ts = impute_from_train(add_split(ts), POLLUTANTS)
    lag_cols = ["AQI", "AQI_Lag1", "AQI_Lag2", "AQI_Lag3", "AQI_Last7_Mean"]
    cols = ["City", "Date", "Split"] + POLLUTANTS + DATE_FEATURES + lag_cols + ["AQI_Next_Day"]
    return ts[cols].sort_values(["City", "Date"]).reset_index(drop=True)


def save(df: pd.DataFrame, name: str, conn: sqlite3.Connection) -> None:
    df.to_csv(CLEAN_DIR / f"{name}.csv", index=False)
    df_db = df.copy()
    df_db["Date"] = df_db["Date"].dt.strftime("%Y-%m-%d")
    df_db.to_sql(name, conn, if_exists="replace", index=False)
    split = df["Split"].value_counts().to_dict()
    left = int(df.drop(columns=["Date"]).isna().sum().sum())
    print(f"{name}: shape={df.shape}, split={split}, missing cells={left}")


def main() -> None:
    base = pd.read_csv(BASE_CSV, parse_dates=["Date"])
    print(f"Loaded base table: {base.shape}\n")
    with sqlite3.connect(DB_FILE) as conn:
        save(build_regression(base), "city_day_regression", conn)
        save(build_classification(base), "city_day_classification", conn)
        save(build_timeseries(base), "city_day_timeseries", conn)
    print("\nDone. Files saved in data/Cleaned/ and tables added to aqi.db")


if __name__ == "__main__":
    main()
