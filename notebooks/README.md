{
  "project_title": "City Hourly Air Quality Analysis",
  "description": "This project analyses hourly air quality data from Indian cities to explore pollution patterns and develop machine-learning models for AQI prediction.",
  "data": {
    "frequency": "Hourly",
    "data_type": "Hourly air quality observations",
    "daily_aggregated_data_used_as_primary_input": false,
    "description": "The analysis uses hourly observations rather than daily aggregated data, allowing pollution patterns to be examined at different times of the day."
  },
  "objectives": [
    "Explore air quality patterns across hours, months, and cities.",
    "Perform exploratory data analysis and feature engineering.",
    "Build regression models to predict AQI values.",
    "Build classification models to predict AQI categories.",
    "Investigate future AQI prediction using hourly observations.",
    "Examine pollution patterns around Diwali and during the 2020 lockdown."
  ],
  "methods": [
    "Data cleaning and preprocessing",
    "Exploratory data analysis",
    "Feature engineering",
    "Regression and classification",
    "Future AQI prediction",
    "Principal Component Analysis (PCA)",
    "City-wise comparison",
    "SQLite database export"
  ],
  "notebooks": [
    {
      "filename": "city_hour_analysis.ipynb",
      "description": "Exploratory data analysis, feature engineering, and AQI regression and classification."
    },
    {
      "filename": "city_hour_extension.ipynb",
      "description": "Extended analysis covering future AQI prediction, Diwali, the 2020 lockdown, PCA, and city comparisons."
    }
  ]
}
