from modules.load import load_data
from modules.filter import get_latest_day
from modules.metrics import compute_metrics
from modules.charting import generate_chart
from modules.reporting import write_report

def main():
    df = load_data()
    df_latest, latest_date = get_latest_day(df)

    metrics = compute_metrics(df_latest)
    generate_chart(df_latest, latest_date)
    write_report(metrics, latest_date)

    print(f"Daily AQI report generated for {latest_date}.")

if __name__ == "__main__":
    main()