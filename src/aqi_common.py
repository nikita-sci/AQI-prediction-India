"""Shared helpers for the 2023-25 AQI notebooks (03, 04, 05).

Keeping these in one file means the notebooks use exactly the same feature lists,
class order, split date and preprocessing, and saved models can be loaded again.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ---------------------------------------------------------------- constants
CLASS_ORDER = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']

# Rows with Date < TRAIN_END are used for training, Date >= TEST_START for testing.
# The days in between are dropped, because their next-day label falls in the test period.
TRAIN_END = '2024-10-31'
TEST_START = '2024-11-01'

FEATURE_GROUPS = {
    'today':    ['AQI', 'AQI_change1'],
    'lags':     ['AQI_lag1', 'AQI_lag2', 'AQI_lag3', 'AQI_lag7'],
    'rolling':  ['AQI_roll3', 'AQI_roll7', 'AQI_roll14', 'AQI_std7'],
    'calendar': ['month', 'weekday', 'is_weekend', 'is_winter', 'is_festival', 'season'],
    'context':  ['state', 'number_of_monitoring_stations', 'pollutant_today', 'pollutant_prev'],
    'city':     ['City'],
}
ALL_FEATURES = [c for cols in FEATURE_GROUPS.values() for c in cols]

CATEGORICAL = ['season', 'state', 'pollutant_today', 'pollutant_prev']
NUMERIC = [c for c in ALL_FEATURES if c not in CATEGORICAL + ['City']]

