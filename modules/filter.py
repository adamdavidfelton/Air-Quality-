### Select Data
def get_latest_day(df):
    latest_date = df["timestamp"].dt.date.max()
    df_latest = df[df["timestamp"].dt.date == latest_date]
    return df_latest, latest_date