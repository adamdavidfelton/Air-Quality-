#import
import matplotlib.pyplot as plt
### Generate a Chart
def generate_chart(df, latest_date):
    plt.figure(figsize = (10,10))
    df.groupby("city")["pm25"].mean().sort_values().plot(kind="bar")
    plt.title (f"Average PM2.5 by City on {latest_date}")
    plt.ylabel("PM2.5")
    plt.xlabel("City")
    plt.tight_layout()
    plt.savefig(f"charts/aqichart_{latest_date}.png")
    plt.close()