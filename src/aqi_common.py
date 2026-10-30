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

# ------------------------------------------------------------- transformers
class CityStats(BaseEstimator, TransformerMixin):
    """Mean and std of today's AQI for each city, learned only from the rows it is fitted on.

    Fitting happens inside each cross-validation fold, so a city's statistics never
    include validation or test rows (no leakage). Unseen cities get the global values.
    Input: DataFrame with columns ['City', 'AQI'].
    """

    def fit(self, X, y=None):
        g = X.groupby('City')['AQI']
        self.mean_ = g.mean()
        self.std_ = g.std().fillna(0.0)
        self.global_mean_ = float(X['AQI'].mean())
        self.global_std_ = float(X['AQI'].std())
        return self

    def transform(self, X):
        m = X['City'].map(self.mean_).astype(float).fillna(self.global_mean_)
        s = X['City'].map(self.std_).astype(float).fillna(self.global_std_)
        return np.column_stack([m.to_numpy(), s.to_numpy()])

    def get_feature_names_out(self, input_features=None):
        return np.array(['city_mean_aqi', 'city_std_aqi'])


def build_preprocessor(columns, scale=False):
    """ColumnTransformer for whichever of the feature columns are in `columns`."""
    cols = list(columns)
    num = [c for c in cols if c in NUMERIC]
    cat = [c for c in cols if c in CATEGORICAL]
    parts = []
    if num:
        parts.append(('num', StandardScaler() if scale else 'passthrough', num))
    if cat:
        parts.append(('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat))
    if 'City' in cols:
        steps = [('stats', CityStats())] + ([('scale', StandardScaler())] if scale else [])
        parts.append(('city', Pipeline(steps), ['City', 'AQI']))
    return ColumnTransformer(parts, remainder='drop', sparse_threshold=0)
