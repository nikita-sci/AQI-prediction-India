# AQI Prediction for India

Exploratory analysis and prediction of Air Quality Index (AQI) across Indian cities.
Course project for **IDC409 – Data Science**, IISER.

> **Status:** EDA on the 2023–2025 dataset is complete. Feature engineering and modelling are in progress.

---

## Project goal

1. Understand how AQI varies across **cities, states, months, seasons and festivals** (Diwali).
2. Check whether past AQI is a strong enough signal to support **next-day AQI prediction**.
3. Build a classifier for the **AQI category** (`Good` to `Severe`) and report per-class metrics, since the rare classes matter most.

---

## Datasets

| Dataset | Period | What it contains | Used for |
|---|---|---|---|
| 2023–2025 AQI file (`aqi_2023_2025_clean.csv`) | Jan 2023 – Apr 2025 | Daily AQI, category, dominant pollutant, number of monitoring stations, city and state (~291 cities, ~32 states) | Geography, seasonality, category balance, classification |

**Limitation:** the 2023–2025 file has no pollutant concentrations, only which pollutant was dominant. It therefore supports **classification of `AQI_Bucket`**, not pollutant regression.

Raw files are not committed. Put the source CSVs in `data/Raw/` and the output of the cleaning notebook in `data/Cleaned/`.

---

## Repository structure

```
AQI-prediction-India/
├── data/
│   ├── Raw/                  # original downloads (not tracked)
│   └── Cleaned/              # cleaned CSVs used by the notebooks
├── notebooks/
│   ├── 01_clean_2023_25.ipynb
│   ├── 02_eda_2023_25.ipynb 
│   └── ...                   
├── reports/
│   ├── figures/2023_25/      # saved plots (PNG)
│   └── results/2023_25/      # CSV tables behind each plot
├── requirements.txt
└── README.md
```

Every plot saved to `reports/figures/2023_25/` has a matching table in `reports/results/2023_25/` with the same name (for example `2023_25_city_month_heatmap.png` and `2023_25_city_month_heatmap.csv`).

---

## EDA notebook: `02_eda_2023_25.ipynb`

| Section | Contents |
|---|---|
| **A. Data quality** | Missing values, duplicate (City, Date) rows, AQI range check, days per city, AQI vs category consistency |
| **B. Geography** | City-wise and state-wise average AQI |
| **C. Time patterns** | National and city trends, monthly boxplot, city × month heatmap, weekday boxplot, fair Jan–Apr year comparison, Diwali window |
| **D. Categories and pollutants** | AQI category balance, Very Poor/Severe by state and month, dominant pollutant overall and by month, monitoring stations vs AQI |
| **E. Time-series diagnostics** | Delhi vs Chandigarh vs Mumbai comparison, autocorrelation of AQI |
| **F. Summary** | Auto-generated key numbers and written findings |

### Features created during EDA

| Feature | Definition |
|---|---|
| `season` | Winter (Dec–Feb), Summer (Mar–May), Monsoon (Jun–Sep), Post-Monsoon (Oct–Nov) |
| `weekday` | Day name from the date |
| `is_winter` | 1 for Nov–Feb, else 0 (November is included because post-Diwali and stubble-burning pollution is already high in North India) |

---

## Key findings

*Fill in from the "Key numbers" cell at the end of the notebook.*

- **Most polluted city / state:** ...
- **Cleanest city:** ...
- **Worst and best months:** ... (winter months are worst, monsoon best)
- **Days Poor or worse (AQI > 200):** ...%
- **Diwali effect:** AQI rose from ... to ... within 3 days of Diwali (2023) and ... to ... (2024)
- **Weekday effect:** ...
- **Class imbalance:** `Severe` is only ...% of the data, so accuracy alone is misleading
- **Autocorrelation:** lag-1 correlation ... and lag-7 correlation ..., supporting next-day prediction

---

## Roadmap

- [x] Data cleaning
- [x] EDA on 2023–2025 data
- [x] EDA on `city_day.csv` (2015–2020)
- [ ] Feature engineering (calendar features, lag features, festival flag)
- [ ] Classification of `AQI_Bucket` with per-class precision, recall and F1
- [ ] Next-day AQI prediction
- [ ] Final report
