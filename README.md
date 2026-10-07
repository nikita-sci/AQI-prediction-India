# City-Hour (hourly) analysis

Notebook: `notebooks/city_hour_analysis.ipynb` (already executed; outputs visible on GitHub).

**Place files like this in the repo:**
- `data/raw/city_hour.csv` (original file; ~65 MB, fine for GitHub's 100 MB limit, or keep it git-ignored)
- `data/processed/city_hour_clean.csv.gz` (cleaned + feature-engineered, 19 MB)
- `outputs/figures/city_hour/*.png`, `outputs/results/city_hour_*.csv`

**Pipeline:** clean (dates, duplicates, sort, drop empty rows, drop Xylene 61% missing) -> hourly EDA -> time features
(hour, rush-hour, night, weekend, season, cyclic hour) -> impute predictors with train-only city+month medians ->
train 2015-2019 / test 2020 -> Linear/Logistic baseline, Decision Tree, Random Forest.

| Task | Best model | Key result (test = 2020) |
|---|---|---|
| Regression | Random Forest | MAE 33.2, RMSE 58.8, R² 0.578 (baseline R² 0.517) |
| Classification | Random Forest | Accuracy 0.667, macro-F1 0.548 (baseline 0.643 / 0.530) |