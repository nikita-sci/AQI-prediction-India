# Pollutant-Based AQI Estimation Using Random Forest Regression

## Project Overview
This branch focuses on developing a machine learning model to estimate the Air Quality Index (AQI) using daily air-quality data from Indian cities. The model uses pollutant measurements, city information, and date-related features to estimate AQI.

The project uses a Random Forest Regression algorithm implemented in Python with Scikit-learn.

## Dataset
The model uses the `city_day.csv` dataset, which contains daily air-quality measurements for multiple Indian cities.

**Data period:** 2015–2020  
**Target variable:** AQI

### Input Features
The model uses available measurements of the following air pollutants:

- PM2.5
- PM10
- NO
- NO₂
- NOx
- NH₃
- CO
- SO₂
- O₃
- Benzene
- Toluene
- Xylene

The model also uses:
- City
- Month
- Day of the week

Only pollutant columns available in the dataset are used.

## Methodology

1. **Data preprocessing:** Converted dates into the appropriate format, removed rows with missing dates or AQI values, removed duplicate city-date records, and filtered the data to the 2015–2020 period.
2. **Feature engineering:** Extracted month and day-of-week information from the date.
3. **Train-test split:** Used data from 2015–2019 for training and data from 2020 for testing.
4. **Missing-value handling:** Used median imputation for numerical features and most-frequent-value imputation for the city feature.
5. **Categorical encoding:** Applied one-hot encoding to the city feature.
6. **Model training:** Trained a Random Forest Regressor with 100 trees.
7. **Evaluation:** Compared predicted AQI values with actual values using MAE, RMSE, and R².

## Model Performance

The model achieved the following results on the 2020 test data:

| Evaluation Metric | Value |
|---|---:|
| Mean Absolute Error (MAE) | 16.11 |
| Root Mean Squared Error (RMSE) | 26.70 |
| R² Score | 0.898 |

These results indicate that the model captures much of the variation in AQI. However, the error analysis shows that predictions can be less accurate for some extreme AQI observations.

## Visualizations and Error Analysis

The notebook includes:
- A comparison of actual and predicted AQI values.
- Feature importance analysis to examine which input features contribute most to the model's predictions.
- An analysis of observations with the largest prediction errors.

The error analysis highlights the need to examine extreme AQI values carefully.

## Important Limitation

This model estimates AQI using pollutant measurements available for a given observation. It is **not a future AQI forecasting model**, because it does not predict future pollutant concentrations.

A separate forecasting approach would be needed to predict AQI in advance.

## Tools and Libraries

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Google Colab
- Git and GitHub

## Notebook

The main notebook for this branch is:

`notebooks/model_a_pollutant_rf.ipynb`

It contains the data preprocessing, feature engineering, model training, evaluation, visualizations, and error analysis.

## Future Improvements

- Evaluate model performance separately for different cities.
- Investigate prediction errors for extreme AQI values.
- Compare Random Forest with other regression algorithms.
- Explore a separate time-series forecasting model for future AQI prediction.
