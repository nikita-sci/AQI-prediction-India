# AQI-prediction-India
Machine learning project for analysing Indian air quality data and predicting AQI.


ADDED BY ADITRI FOR MY CITY_DAY CSV WORK
# AQI Prediction for Indian Cities

Predicting the Air Quality Index (AQI) and the AQI category from daily pollutant readings, city and date features, using Indian air-quality data from 2015 to 2020.

**Author:** Aditri Srivastava

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
