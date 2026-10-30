
# AQI prediction in India: Different cities across the country
Predicting the Air Quality Index (AQI) and the AQI category from daily pollutant readings, city and date features, using Indian air-quality data from 2015 to 2020.
PARTS: 
CITY DAYS: 2015-20 by Aditri Srivastava
CITY HOURS: 2015-20 by Parul
CITY DAYS: 2023-25 by Nikita

## Project goals

- **Regression:** predict the numeric AQI value.
- **Classification:** predict the AQI category (Good, Satisfactory, Moderate, Poor, Very Poor, Severe).
- **EDA:** study city-wise AQI, pollutant correlations, and monthly, seasonal and yearly trends.

## Data

- Source: [Air Quality Data in India (2015-2020)](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india) on Kaggle, file `city_day.csv`.
- 29,531 daily records for 26 cities, from 2015-01-01 to 2020-07-01.
- The raw data is **not stored in this repository** (it is git-ignored). Download `city_day.csv` and place it in `data/raw/`.
- The [2023-2025 Kaggle dataset](https://www.kaggle.com/datasets/saikiranudayana/india-air-quality-index-aqi-dataset-20232025) contains only AQI values and the dominant pollutant, with no individual pollutant readings. It cannot be merged with the 2015-2020 data for pollutant-based models, so it is not used in the core project.

## Project structure

```
AQI-prediction-India/
├── data/
│   ├── raw/          # city_day.csv goes here (git-ignored)
│   └── Cleaned/      # cleaned CSVs and aqi.db (SQLite)
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_regression.ipynb
│   └── 03_classification.ipynb
├── src/
│   ├── inspect_data.py        # first look at the raw data
│   ├── clean_data.py          # base cleaning + date features
│   └── make_task_datasets.py  # regression / classification / time-series files
├── outputs/          # saved plots and results tables
├── requirements.txt
└── README.md
```

## How to run (Windows PowerShell)

```powershell
git clone git@github.com:nikita-sci/AQI-prediction-India.git
cd AQI-prediction-India
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# put city_day.csv in data\raw\ first
python src\clean_data.py
python src\make_task_datasets.py
```

Then open the notebooks in `notebooks/` (select the `.venv` kernel) and run them in order: `01_eda`, `02_regression`, `03_classification`.

Developed with Python 3.14. Packages: pandas, numpy, matplotlib, seaborn, scikit-learn, ipykernel.

## Data pipeline

1. **Base cleaning** (`clean_data.py`):
   - parse dates with an explicit format and strip city names
   - remove duplicate city-day rows (none were found)
   - drop `Xylene` (about 61% missing)
   - drop rows with no pollutant readings (1,424 rows)
   - drop rows with no AQI (3,306 rows), since the target must never be filled in
   - result: 24,801 rows, 26 cities

   Missing pollutant values and outliers are deliberately kept in this base table, so the EDA shows the real data.
2. **Date features:** year, month, weekday, weekend flag, season (Winter Dec-Feb, Summer Mar-May, Monsoon Jun-Sep, Post-monsoon Oct-Nov), winter flag, and a Diwali flag (+/- 3 days around Diwali of each year).
3. **Task-specific files** (`make_task_datasets.py`):
   - `city_day_regression.csv`: missing pollutants filled with the city+month median.
   - `city_day_classification.csv`: same filling, with the AQI number removed (the category is calculated from it) and the category encoded 0-5.
   - `city_day_timeseries.csv`: lag and rolling-average features for next-day prediction (prepared for the extension).
4. **Storage:** every table is saved both as CSV and as a table in the SQLite database `data/Cleaned/aqi.db`.

**Train/test split:** by date. Rows before 2019-01-01 are training data (13,326 rows) and rows from 2019 onwards are test data (11,475 rows). All fill-in medians are computed from training rows only, so no test information leaks into training.

## Exploratory data analysis

`notebooks/01_eda.ipynb` covers:

- missing pollutant data per city
- AQI distribution and number of days per category
- average AQI by city
- pollutant correlation heatmap
- monthly, seasonal and yearly AQI trends
- Delhi vs Chandigarh vs Mumbai over time
- weekday and Diwali effects
- monthly AQI boxplot and PM2.5 vs AQI scatter plot

All plots are saved in `outputs/`.

## Models

**Features:** 11 pollutants (PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene), month, weekday, weekend flag, winter flag, Diwali flag, and one-hot encoded season and city. `Year` is excluded because the test years are not seen in training.

| Task | Baseline | ML models |
|---|---|---|
| Regression | Predict the training mean | Linear Regression, Decision Tree, Random Forest |
| Classification | Predict the most frequent class | Logistic Regression, Decision Tree, Random Forest |

## Results

### Regression (test set, 2019 onwards)

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Baseline (predict mean) | 102.2 | 130.0 | -0.169 |
| Linear Regression | 27.8 | 45.9 | 0.855 |
| Decision Tree | 23.8 | 50.5 | 0.823 |
| Random Forest | **20.0** | **41.2** | **0.883** |

### Classification (test set, 2019 onwards)

| Model | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|---|---|---|---|---|
| Baseline (most frequent) | 0.346 | 0.058 | 0.167 | 0.086 |
| Logistic Regression | 0.719 | 0.666 | 0.638 | 0.644 |
| Decision Tree | 0.732 | 0.717 | 0.666 | 0.681 |
| Random Forest | **0.769** | **0.778** | **0.671** | **0.691** |

### Random Forest classifier, per category

| Category | Precision | Recall | F1 | Test days |
|---|---|---|---|---|
| Good | 0.88 | 0.23 | 0.36 | 939 |
| Satisfactory | 0.76 | 0.87 | 0.81 | 4519 |
| Moderate | 0.79 | 0.84 | 0.81 | 3969 |
| Poor | 0.69 | 0.62 | 0.66 | 1040 |
| Very Poor | 0.74 | 0.66 | 0.69 | 625 |
| Severe | 0.81 | 0.81 | 0.81 | 383 |

The confusion matrix is saved as `outputs/12_rf_confusion_matrix.png`.

## Key findings

- Random Forest was the best model for both regression (MAE about 20 AQI points, R² 0.88) and classification (accuracy 77%, macro F1 0.69).
- PM2.5, PM10 and CO are the most important features in both tasks. Date and city features matter little once the pollutant readings are known.
- Eight pollutant features (PM2.5, CO, NO, PM10, NOx, O3, SO2, NO2) gave almost the same regression accuracy as the full feature set (R² 0.876 vs 0.883).
- Good days were the hardest to predict (recall 0.23, F1 0.36): the model is rarely wrong when it says "Good" (precision 0.88) but catches few real Good days, because only 3% of training rows were Good. Severe days were predicted well (F1 0.81). Poor and Very Poor were the next weakest categories.
- The baseline R² is negative because AQI levels in the test years (2019 onwards) are lower than in the training years.
- Good days make up 3% of training rows but 8% of test rows, so the class balance shifts over time (air quality improved in 2019-2020, including the COVID-19 lockdown period).
- AQI is calculated from pollutant readings, so high same-day scores are expected.

## Limitations

- Same-day prediction is partly circular, since AQI is derived from the pollutants.
- Some pollutants (PM10, NH3, Toluene, Benzene) have many missing values that were filled with medians.
- The data ends in July 2020, and 2020 includes the COVID-19 lockdown.
- The train/test split is by time, so the test set differs in distribution from the training set. Scores are lower than a random split would give, but they are a more realistic estimate.
- Models use default or lightly set parameters and were not tuned.

## Possible extensions

- Predict next-day AQI using lag features (`city_day_timeseries.csv` is already prepared).
- Compare Delhi, Chandigarh and Mumbai with city-specific models.
- Add XGBoost, or use the 2023-2025 dataset for recent AQI trends.



## Indian Air Quality Index (AQI): Analysis, Prediction and Cross-Period Forecasting(DATASET:2023-25)

An end-to-end data science project examining air quality across Indian cities, estimating AQI from pollutant measurements, forecasting next-day AQI and AQI categories, and testing whether models trained on older observations generalize to more recent periods.

The project combines **historical data (approximately 2015–2020)** and **recent data (through April 2025 in the held-out evaluation)**. It includes exploratory analysis, leakage-aware feature engineering, regression and classification models, city-level error analysis, and a controlled historical-versus-recent training comparison.

> **Important:** Same-day AQI estimation and next-day AQI forecasting are different prediction tasks. Their numerical scores must **not** be ranked against each other as if they came from the same test set. The fairest comparison of training periods is the matched-test experiment in Notebook 06.

## Project objectives

- Explore AQI levels, pollutant concentrations, regional differences, seasonality, and temporal patterns across Indian cities.
- Predict **same-day AQI** from pollutant measurements using historical city-day data (Model A).
- Forecast **next-day AQI** and AQI categories from recent observations and lagged features.
- Evaluate **Model B**, trained on historical AQI records and tested on newer observations, to investigate cross-period generalization.
- Compare historical- and recent-trained versions of the same algorithms using **identical features and held-out rows**.
- Assess model performance overall and for individual cities, including Delhi, Chandigarh and Mumbai where data are available.

## Experiments at a glance

| Experiment | Training / evaluation setting | Target | Main inputs | Comparison scope |
| --- | --- | --- | --- | --- |
| Model A — same-day | Historical city-day data, nominally 2015–2020 | Current-day AQI | Same-day pollutant concentrations (e.g., PM2.5, PM10, NO₂, SO₂, CO, O₃) | Models and baselines within Model A |
| Model A — next-day extension | Historical data | Next-day AQI | Historical notebook's available predictors | Within that experiment's held-out rows |
| Recent-data forecasting | Recent city-day records (project dataset covering recent years) | Next-day AQI value and category | AQI lags, rolling statistics, calendar, city and context | Models and baselines within the recent test set |
| Model B — cross-period | Train on historical data through 2020; test on recent data | Next-day AQI | Shared AQI-only history, calendar and city features | Historical vs recent training on **exactly the same recent test rows** |

## Repository workflow

The `notebooks/` folder contains two complementary analysis streams and the final integration:

| Notebook | Purpose |
| --- | --- |
| `01_eda.ipynb` | Historical-data exploratory analysis |
| `02_regression.ipynb` | Historical same-day AQI regression |
| `03_classification.ipynb` | Historical AQI category classification |
| `04_next_day.ipynb` | Historical next-day forecasting extension |
| `01_clean_2023_25.ipynb` | Clean the recent AQI dataset |
| `02_eda_2023_25.ipynb` | Recent-data EDA: geography, time patterns, AQI categories, pollutants and autocorrelation |
| `03_feature_engineering_2023_25.ipynb` | Create time-aligned lag, rolling, calendar and target features; inspect leakage |
| `04_modelling_2023_25.ipynb` | Train and evaluate recent next-day regression and classification models |
| `05_analysis_2023_25.ipynb` | Feature importance, ablation, seasonality, city/state errors and case studies |
| `06_model_b_cross_period.ipynb` | Historical training, recent held-out testing, matched recent-training comparison |
| `06b_model_b_validation.ipynb` | Temporal alignment, split/leakage, prediction-matching and metric-recalculation checks |
| `07_final_model_comparison.ipynb` | Consolidated results, figures, caveats and conclusions |

Supporting code may be found in `src/` and data-preparation scripts, depending on the checkout. The recent modelling notebook uses `src.aqi_common` for shared features and split settings.

### Key project directories

```text
.
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_regression.ipynb
│   ├── 03_classification.ipynb
│   ├── 04_next_day.ipynb
│   ├── 01_clean_2023_25.ipynb
│   ├── 02_eda_2023_25.ipynb
│   ├── 03_feature_engineering_2023_25.ipynb
│   ├── 04_modelling_2023_25.ipynb
│   ├── 05_analysis_2023_25.ipynb
│   ├── 06_model_b_cross_period.ipynb
│   ├── 06b_model_b_validation.ipynb
│   └── 07_final_model_comparison.ipynb
├── data/
│   ├── raw/                    # original datasets, if included locally
│   └── Cleaned/                # cleaned city-day data and engineered features
├── src/                        # shared Python utilities, where present
├── outputs/                    # historical experiment metrics
└── reports/
    ├── figures/
    │   ├── 2023_25/
    │   ├── model_b/
    │   └── final_comparison/
    ├── results/
    │   ├── modelb/
    │   └── final_comparison/
    ├── results_regression_2023_25.csv
    └── results_classification_2023_25.csv
```

**Path note:** Some notebooks use `data/cleaned/` and others use `data/Cleaned/`. These can behave differently on case-sensitive operating systems. Confirm actual paths and notebook input settings before running; the paths above reflect those used in the cross-period analysis.

## Data and preprocessing

The historical work uses Indian city-day records with AQI and pollutant measurements. The recent stream uses daily city-level AQI observations with available contextual and pollutant information. Both sources are normalized for dates and city labels where appropriate; their exact coverage and missingness should be checked in the cleaning and validation notebooks.

Cleaning and preparation include:

1. Parse and sort dates and standardize city names.
2. Inspect missing values, duplicates, coverage and city/day continuity.
3. Create calendar features such as month, weekday, weekend, season and winter indicators.
4. Create AQI lag and rolling features **separately for each city**.
5. Define the next-day target by shifting AQI forward by one calendar day.
6. Split data chronologically and evaluate on future, held-out observations.

In the Model B notebook, a daily calendar is explicitly reindexed so missing dates are not mistaken for consecutive days. Its rolling means use past AQI readings (`shift(1)`), while current-day AQI is available at prediction time. This prevents tomorrow's AQI from appearing in model inputs.

### AQI forecasting features

The cross-period experiment intentionally uses the same predictors for both training periods:

- AQI today; lags of 1, 2, 3 and 7 days.
- Rolling means over 3, 7 and 14 prior days, plus rolling variability and recent AQI change.
- Month, weekday, weekend, winter indicator and season.
- City identity.

Unlike the historical same-day AQI model, this controlled experiment does **not** rely on pollutant concentrations measured on the target day.

## Models and evaluation

### Regression

The project evaluates suitable baselines and machine-learning algorithms, including linear/ridge regression, decision trees, random forests and histogram-based gradient boosting, as applicable to each experiment.

Reported regression metrics:

- **MAE** — mean absolute error, in AQI units (lower is better).
- **RMSE** — root mean squared error, in AQI units (lower is better).
- **R²** — coefficient of determination (higher is generally better).

A key next-day forecasting baseline is **persistence**: tomorrow's AQI equals today's AQI. The recent-data experiment also reports a 7-day-mean baseline.

### Classification

The classification notebooks forecast or estimate AQI categories and report accuracy, macro-precision, macro-recall, macro-F1, confusion matrices and per-class analyses where available. Macro-averaged metrics help assess performance across categories that may have unequal numbers of observations. Always check the source notebook's category mapping before comparing classification results.

## Selected results

The following values are drawn from the saved consolidated output in `07_final_model_comparison.ipynb`. They are **illustrative of the reported experiments**, not interchangeable scores across datasets.

### Historical same-day AQI estimation (Model A)

| Model | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Mean-prediction baseline | 102.224 | 130.034 | -0.169 |
| Linear Regression | 27.802 | 45.866 | 0.855 |
| Decision Tree | 23.812 | 50.536 | 0.823 |
| Random Forest | **19.961** | **41.165** | **0.883** |

Because reported AQI is derived from pollutants, same-day pollutant-based estimation is a substantially different problem from forecasting AQI in advance.

### Recent-data next-day AQI forecasting

| Model | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Persistence (tomorrow = today) | 24.783 | 37.158 | 0.672 |
| Ridge Regression | 23.614 | 33.918 | 0.727 |
| Random Forest | 23.531 | 33.976 | 0.726 |
| Hist Gradient Boosting | **23.505** | **33.854** | **0.728** |
| Hist Gradient Boosting (tuned) | 23.508 | 33.858 | 0.728 |

The untuned gradient boosting model has the lowest MAE among the listed recent-data regression models, although differences between the ML models are small.

### Model B: historical vs recent training on matched test rows

**Held-out target dates:** 1 November 2024 to 30 April 2025. Historical training ends by 31 December 2020; recent training uses the pre-test portion of the newer dataset. Both cohorts use the same feature definitions and the same eligible test observations.

| Algorithm | Historical-training MAE | Recent-training MAE |
| --- | ---: | ---: |
| Ridge Regression | 23.336 | **23.090** |
| Random Forest | **23.458** | 23.532 |
| Hist Gradient Boosting | **23.210** | 23.313 |
| Persistence baseline (no fitting) | 24.270 | 24.270 |

Here **Ridge improves with recent training**, while Random Forest and Hist Gradient Boosting have slightly lower MAE with historical training. These small differences do not justify a blanket claim that one training period is universally superior. Model B's comparison is valid because the test observations and feature definitions are matched.

### Visual diagnostics

The notebooks save charts of model predictions and errors, including:

- City-wise AQI patterns, monthly distributions, annual January–April comparisons, and lag autocorrelation.
- Actual-versus-predicted AQI and selected-city forecasting time series.
- Feature permutation importance and cumulative feature-group ablation.
- Errors by month, state and city, including comparison against persistence.
- A **city-wise dumbbell chart** contrasting historical-model and persistence MAE.
- A **historical-versus-recent slope chart** for matched-test model comparisons.
- Final comparison charts and classification heatmaps.

## Reproducing the analysis

### Requirements

- Python 3.10+ recommended.
- Jupyter notebooks (VS Code with the Jupyter extension or JupyterLab).
- Python packages used in the notebooks, including `numpy`, `pandas`, `matplotlib` and `scikit-learn`. Additional plotting or file-handling packages may be needed for particular notebooks.

If the repository includes a `requirements.txt`, install its pinned dependencies. Otherwise install the core packages:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install numpy pandas matplotlib scikit-learn jupyter ipykernel
```

On macOS/Linux, activate with `source venv/bin/activate` instead.

### Execution order

1. Put the input datasets in the paths expected by the notebooks. Do not assume that large raw files are tracked in Git.
2. Run the historical notebooks `01_eda.ipynb` → `02_regression.ipynb` → `03_classification.ipynb` → `04_next_day.ipynb` (and any required historical preprocessing scripts).
3. Run `01_clean_2023_25.ipynb` → `02_eda_2023_25.ipynb` → `03_feature_engineering_2023_25.ipynb` → `04_modelling_2023_25.ipynb` → `05_analysis_2023_25.ipynb`.
4. Run `06_model_b_cross_period.ipynb`, followed by `06b_model_b_validation.ipynb`.
5. Run `07_final_model_comparison.ipynb` **last**, since it reads the CSVs produced by the earlier experiments rather than retraining the models.

Start each notebook from a **fresh kernel** and run cells in order. In particular, repeatedly executing the Model B comparison cell can append duplicate result rows to an in-memory `results` list and cause a pivot error. The notebooks generally expect to be launched from the repository root or `notebooks/`; confirm paths printed in their setup cells.

### Important output files

| File | Contents |
| --- | --- |
| `outputs/regression_results.csv` | Historical same-day regression metrics |
| `outputs/classification_results.csv` | Historical classification metrics |
| `outputs/next_day_results.csv` | Historical next-day forecasting metrics |
| `reports/results_regression_2023_25.csv` | Recent next-day regression comparison |
| `reports/results_classification_2023_25.csv` | Recent classification comparison |
| `reports/results/modelb/historical_model_results.csv` | Historical-trained Model B metrics |
| `reports/results/modelb/all_models_same_test_results.csv` | Historical and recent models on common test rows |
| `reports/results/modelb/predictions_same_test_rows.csv` | Prediction-level matched-test results |
| `reports/results/modelb/city_wise_errors.csv` | Per-city historical-model and persistence errors |
| `reports/results/modelb/model_b_validation_checks.csv` | Model B validation checklist output |
| `reports/results/final_comparison/final_regression_summary.csv` | Consolidated regression results |
| `reports/results/final_comparison/final_classification_summary.csv` | Consolidated classification results |
| `reports/results/final_comparison/source_availability.csv` | File-availability report |

## Interpretation, limitations and responsible use

- **Different tasks and samples:** Same-day AQI estimation, historical next-day forecasting and recent next-day forecasting are not directly comparable by raw MAE or R². The only directly controlled training-period comparison reported here is Model B's matched test.
- **Incomplete time coverage:** Recent-year data may end in April 2025; the EDA therefore compares **January–April across years** when making yearly comparisons.
- **Missing observations:** City/day gaps, missing pollutants and changing coverage can affect the derived features and the number of eligible test rows.
- **Distribution shift:** Pollution patterns, monitoring coverage and regional conditions can change over time; results from one period may not persist indefinitely.
- **Autocorrelation:** High lag correlation motivates AQI-history features but does not, by itself, prove predictive performance or causality.
- **Classification imbalance:** Common AQI categories may dominate accuracy; macro-F1 and per-class results are essential.
- **Uncertainty:** Small differences in test MAE should not be interpreted as significant without further robustness or uncertainty analysis.
- **Validation:** Run `06b_model_b_validation.ipynb` and inspect every check before asserting that temporal alignment, matched rows and exported metrics have been fully validated.

This project is intended for academic analysis and model evaluation, **not as an operational air-quality warning system or medical advice**.

## Collaboration

This project combines contributions to the historical Model A analyses and the recent-data, cross-period and final-comparison notebooks. Development work may occur on separate Git branches before review and merging. Preserve individual contributions and verify generated result files when integrating changes.

## Data attribution and licensing

The datasets consist of Indian air-quality observations prepared for this academic project. Consult the repository's original data source documentation for provenance, usage terms and citation details. **Do not add a license or claim unrestricted redistribution of the data without verifying the relevant terms.**

---

**Project takeaway:** The strongest claim is not that one model has the lowest number across every table, but that the project evaluates distinct AQI tasks with appropriate baselines, time-aware features, honest comparison boundaries and an explicitly matched historical-versus-recent forecasting experiment.

