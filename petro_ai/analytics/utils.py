# analytics/utils.py
import pandas as pd
import numpy as np
from prophet import Prophet

# -------------------------------
# Predictive Maintenance (Demo)
# -------------------------------
def run_predictive_maintenance_demo(df):
    """
    Predictive maintenance demo: generates synthetic failure probabilities
    df: pandas DataFrame with numeric columns
    """
    df_result = df.copy()
    # Generate random probability between 0 and 1 for each row
    df_result['PredictedFailureProbability'] = np.round(np.random.rand(len(df)), 2)
    return df_result.to_html(classes="table table-striped table-sm")


# -------------------------------
# Production Forecasting (Prophet)
# -------------------------------
def run_forecast_prophet(df, date_col):
    """
    Forecast production (or any numeric columns) using Prophet
    df: pandas DataFrame
    date_col: name of the date column
    """
    forecast_tables = []
    
    # Loop through numeric columns except date
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    for col in numeric_cols:
        # Prepare DataFrame for Prophet
        df_prophet = df[[date_col, col]].rename(columns={date_col: "ds", col: "y"})
        
        # Create Prophet model
        m = Prophet(daily_seasonality=True)
        m.fit(df_prophet)
        
        # Forecast next 10 days
        future = m.make_future_dataframe(periods=10)
        forecast = m.predict(future)
        
        # Keep only date and forecasted value
        forecast_table = forecast[['ds', 'yhat']].rename(columns={'ds': 'Date', 'yhat': f'Forecast_{col}'})
        forecast_tables.append(forecast_table)
    
    # Merge all forecasts into one table
    result_df = pd.concat(forecast_tables, axis=1)
    # Remove duplicate date columns
    result_df = result_df.loc[:, ~result_df.columns.duplicated()]
    
    # Convert to HTML for rendering
    return result_df.to_html(classes="table table-striped table-sm")
