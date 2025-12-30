#import
import pandas as pd
### Calculate Key Metrics
def compute_metrics (df):
    return {
        "avg_pm25": df["pm25"].mean(),
        "avg_pm10": df["pm10"].mean(),
        "avg_no2": df["no2"].mean(),
        "avg_so2": df["so2"].mean(),
        "max_city": df.loc[df["pm25"].idxmax(), "city"],
        "max_pm25": df.loc[df["pm25"].idxmax(), "pm25"]    }