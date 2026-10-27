# AQI Prediction — Date Feature Engineering and EDA (2022–2025)

## Overview
This branch focuses on the cleaned 2022–2025 Air Quality Index (AQI) dataset as part of the AQI Prediction project. The aim is to prepare the dataset for exploratory data analysis (EDA) and investigate temporal patterns and variations in air quality.

## Objectives
- Perform date feature engineering on the cleaned AQI dataset.
- Analyze AQI trends across years, months, seasons, weekdays, and cities.
- Visualize AQI distributions and air quality category frequencies.
- Identify missing data and retain genuine high-AQI observations during EDA.
- Prepare analysis outputs for integration with the historical dataset maintained by another team member.

## Dataset
The dataset contains air quality observations from 2022–2025.

Relevant columns include:
- `date`: Date of observation.
- `state`: State associated with the observation.
- `area`: City or area where air quality was recorded.
- `aqi_value`: Recorded AQI value.
- `air_quality_status`: Air quality category.
- `prominent_pollutants`: Text describing the prominent pollutants.
- `number_of_monitoring_stations`: Number of monitoring stations, where available.

The dataset is maintained separately from the historical dataset to allow independent analysis before integration.

## Work Completed

### 1. Dataset Preparation
- Worked with the cleaned 2022–2025 AQI dataset.
- Identified the relevant columns for temporal and city-wise analysis.
- Reviewed the dataset's structure and identified limitations affecting further analysis.

### 2. Date Feature Engineering
The following features have been identified for temporal analysis:
- `Year`: Year of observation.
- `Month`: Month of observation.
- `Weekday`: Day of the week.
- `Is_Weekend`: Indicates whether an observation falls on a weekend.
- `Season`: Season associated with the observation date.

These features will support comparisons of AQI patterns over time.

### 3. Exploratory Data Analysis (EDA)
The planned EDA includes:
- AQI distribution analysis.
- Yearly and monthly AQI trends.
- Seasonal variations in AQI.
- Weekday versus weekend comparisons.
- City-wise AQI comparisons.
- Air quality category distributions.
- Examination of unusually high AQI observations.

## Tools and Libraries
- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Dataset Limitations
- The dataset contains a `prominent_pollutants` text column rather than separate numerical concentration columns for individual pollutants.
- Pollutant concentration correlation heatmaps cannot be generated from this dataset alone.
- Missing values should be handled according to the requirements of each analysis rather than filled unnecessarily.
- Unusually high AQI values should be retained during EDA unless a data-quality issue is verified.
- If 2025 observations cover only part of the year, yearly comparisons must account for this incomplete coverage.

## Next Steps
- Implement date feature engineering.
- Generate and interpret EDA visualizations.
- Save the feature-enhanced dataset, plots, and summary statistics.
- Compare the recent dataset with the historical dataset and identify compatible columns.
- Support combined analysis and subsequent AQI prediction modelling.

## Project Context
This work contributes to the group project on Air Quality Index prediction by focusing on temporal analysis of recent air quality data. The resulting features and EDA findings will support dataset integration, interpretation of air quality patterns, and later modelling.

