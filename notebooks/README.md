# City Hourly Air Quality Analysis

## Overview

This project analyses hourly air quality data from Indian cities to explore pollution patterns and develop machine learning models for AQI prediction.

The main focus is to understand how air quality changes across different hours, months, and cities. The project also explores future AQI prediction and examines pollution patterns around Diwali and during the 2020 lockdown.

## Data and Temporal Resolution

This project uses **hourly air quality observations rather than daily aggregated data**. Working with hourly observations makes it possible to examine changes in pollution at different times of the day.

The hourly data is used for exploratory data analysis, feature engineering, and machine learning. Some analyses also compare pollution patterns across months, cities, and specific time periods.

## Objectives

- Explore air quality patterns across different hours, months, and cities.
- Clean and prepare the dataset for analysis.
- Perform exploratory data analysis (EDA).
- Create additional features from date and time information.
- Build regression models to predict AQI values.
- Build classification models to predict AQI categories.
- Explore future AQI prediction using hourly observations.
- Compare pollution levels around Diwali.
- Examine air quality changes during the 2020 lockdown.
- Compare model performance using Principal Component Analysis (PCA).

## Notebooks

### 1. `city_hour_analysis.ipynb`

This notebook covers the initial analysis of hourly air quality data, including:

- Data cleaning and preprocessing
- Exploratory data analysis
- Hourly and seasonal pollution patterns
- Feature engineering
- AQI regression models
- AQI category classification
- Model evaluation and conclusions

### 2. `city_hour_extension.ipynb`

This notebook extends the analysis with additional investigations, including:

- Future AQI prediction
- Comparison with a persistence baseline
- Pollution patterns around Diwali
- Air quality during the 2020 lockdown
- Principal Component Analysis (PCA)
- City-wise air quality comparisons
- Exporting processed data to an SQLite database

## Methods and Tools

The project uses Python for data analysis, visualisation, and machine learning.

The main methods include:

- Data cleaning and preprocessing
- Exploratory data analysis
- Feature engineering
- Regression and classification
- Time-based training and testing
- Model performance evaluation
- Principal Component Analysis
- SQLite database operations

## Key Focus

The main focus of this project is to study air quality using **hourly observations instead of relying on daily aggregated data**. This helps examine within-day pollution patterns and provides a basis for investigating future AQI prediction.

## Limitations

- The results depend on the quality and availability of the recorded air quality data.
- Pollution patterns may differ across cities and time periods.
- The 2020 lockdown period may not represent typical pollution conditions.
- Model performance on historical data does not guarantee similar performance on future observations.

## Conclusion

This project explores hourly air quality patterns across Indian cities and applies machine learning techniques to AQI prediction. It combines exploratory analysis with model evaluation and additional investigations into Diwali pollution patterns, lockdown-related changes, and the use of PCA.

The aim is to understand the patterns present in the data and evaluate how well different approaches can predict AQI.
