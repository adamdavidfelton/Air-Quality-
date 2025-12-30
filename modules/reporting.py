def write_report(metrics,latest_date):
    with open ("reports/daily_aqi_report.txt","w") as f:
        f.write(f"Daily AQI Report - {latest_date}\n")
        f.write("-------------------------------\n")
        f.write(f"Average PM2.5: {metrics['avg_pm25']:.2f}\n")
        f.write(f"Average PM10: {metrics['avg_pm10']:.2f}\n")
        f.write(f"Average NO2: {metrics['avg_no2']:.2f}\n")
        f.write(f"Average SO2: {metrics['avg_so2']:.2f}\n")
        f.write(f"Worst City (PM2.5): {metrics['max_city']} ({metrics['max_pm25']:.2f})\n")
        f.write("\nChart saved as aqichart.png\n")
        f.write("\nGenerated automatically by AQI Reporter\n")