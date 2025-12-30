#imports
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
# terminal options
pd.options.display.max_rows = 100
pd.options.display.width = 0
###Load Dataset
def load_data(path="C:/Users/adamd/Documents/airquality.csv"):
    aq = pd.read_csv(path)
    aq["timestamp"] = pd.to_datetime(aq["timestamp"])
    return aq
### Select Data
def get_latest_day(aq):
    latest_date = aq["timestamp"].dt.date.max()
    return aq[(aq["timestamp"].dt.date == latest_date)], latest_date

### Calculate Key Metrics
def compute_metrics(aq):
    return {
        "avg_pm25": aq["pm25"].mean(),
        "avg_pm10": aq["pm10"].mean(),
        "avg_no2": aq["no2"].mean(),
        "avg_so2": aq["so2"].mean(),
        "max_city": aq.loc[aq["pm25"].idxmax(), "city"],
        "max_pm25": aq.loc[aq["pm25"].idxmax(), "pm25"]    }

### Generate a Chart
def generate_chart(aq, latest_date):
    plt.figure(figsize = (10,10))
    aq.groupby("city")["pm25"].mean().sort_values().plot(kind="bar")
    plt.title (f"PM2.5 by City {latest_date}")
    plt.ylabel("PM2.5")
    plt.tight_layout()
    plt.savefig("aqichart.png")
    plt.close()

def write_report(metrics,latest_date):
    with open ("daily_aqi_report.txt","w") as f:
        f.write(f"Daily AQI Report - {latest_date}\n")
        f.write("-------------------------------\n")
        f.write(f"Average PM2.5: {metrics['avg_pm25']:.2f}\n")
        f.write(f"Average PM10: {metrics['avg_pm10']:.2f}\n")
        f.write(f"Average NO2: {metrics['avg_no2']:.2f}\n")
        f.write(f"Average SO2: {metrics['avg_so2']:.2f}\n")
        f.write(f"Worst City (PM2.5): {metrics['max_city']} ({metrics['max_pm25']:.2f})\n")
        f.write("\nChart saved as aqichart.png\n")


def main():
    df = load_data()
    df_latest, latest_date = get_latest_day(df)

    metrics = compute_metrics(df_latest)
    generate_chart(df_latest, latest_date)
    write_report(metrics, latest_date)

    print(f"Daily AQI report generated for {latest_date}.")

if __name__ == "__main__":
    main()





## Saves a Clean Report