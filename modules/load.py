#import
import pandas as pd

def load_data(path="data/airquality.csv"):
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df