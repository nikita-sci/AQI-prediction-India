AQI Prediction — 2022–2025 Dataset Preparation

Overview

This branch focuses on the cleaned air quality dataset covering 2022–2025 as part of the AQI Prediction project. The work is intended to support date-feature engineering and exploratory data analysis (EDA) to identify temporal patterns and variations in air quality.

Work Completed

1. Dataset Preparation

Worked with the cleaned 2022–2025 AQI dataset.

Identified the relevant fields for further analysis, including date, location, AQI value, air quality status, prominent pollutants, and monitoring-station information.

Kept the recent dataset separate from the historical dataset used by another team member.

2. EDA Preparation

Identified the date-derived features needed to study temporal variations in AQI, including year, month, weekday, weekend status, and season.

Identified the key visualizations required for understanding AQI distributions, temporal trends, and city-wise differences.

Established data-quality considerations for EDA, including missing-value checks and retaining potential pollution-related outliers.

3. Dataset Limitations Identified

The dataset contains a prominent_pollutants field but does not contain separate numerical concentration columns for individual pollutants.

Consequently, pollutant concentration correlation analysis cannot be performed using this dataset alone.
