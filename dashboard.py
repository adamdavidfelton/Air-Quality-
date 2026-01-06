# dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
import pycountry
import plotly

# Import backend modules
from modules.load import load_data
from modules.filter import get_latest_day
from modules.metrics import compute_metrics
from modules.metrics import compute_metrics
from modules.filter import get_latest_day

# Streamlit settings
st.set_page_config(layout="wide")
pd.options.display.max_rows = 100
pd.options.display.width = 0
alt.data_transformers.disable_max_rows()


# LOAD & CLEAN DATA
air = load_data("data/airquality.csv")

def convert_country(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code

air["country"] = air["country"].apply(convert_country)
air_latest, latest_date = get_latest_day(air)
metrics = compute_metrics(air_latest)


# SIDEBAR FILTERS
st.sidebar.header("Filters")

# Country filter
country_list = sorted(air["country"].unique())
selected_country = st.sidebar.multiselect(
    "Select Country",
    country_list,
    default=country_list)

# City filter
city_list = sorted(air[air["country"].isin(selected_country)]["city"].unique())
selected_city = st.sidebar.multiselect("Select City", city_list)

# Pollutant filter
pollutants = ["pm25", "pm10", "no2", "so2", "o3", "co"]
selected_pollutant = st.sidebar.multiselect("Select Pollutant", pollutants)

if not selected_city or not selected_pollutant:
    st.warning("Please select a city and pollutant")
    st.stop()


# FILTER DATA
filt_air = air[
    (air["country"].isin(selected_country)) &
    (air["city"].isin(selected_city))]

filt_air["hour"] = filt_air["timestamp"].dt.hour


# ROLLING WINDOW SMOOTHING
window = st.sidebar.slider("Rolling Window (hours)", 1, 48, 6)

filt_air[selected_pollutant] = (
    filt_air[selected_pollutant]
    .rolling(window=window, min_periods=1)
    .mean())


# MELT FOR ALTAIR
melted = filt_air.melt(
    id_vars=["timestamp", "country", "city"],
    value_vars=selected_pollutant,
    var_name="pollutant",
    value_name="value")

melted_hour = filt_air.melt(
    id_vars=["hour", "country", "city"],
    value_vars=selected_pollutant,
    var_name="pollutant",
    value_name="value")

hourly_avg = (
    melted_hour.groupby(["city", "hour", "pollutant"], as_index=False)["value"]
    .mean())


# HEADER + TABS
st.header("Air Quality Dashboard")
# KPIS
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg PM2.5", f"{metrics['avg_pm25']:.2f}")
col2.metric("Avg PM10", f"{metrics['avg_pm10']:.2f}")
col3.metric("Avg NO2", f"{metrics['avg_no2']:.2f}")
col4.metric("Avg SO2", f"{metrics['avg_so2']:.2f}")

tab1, tab2 = st.tabs(["Pollutants over Time", "Pollution Heatmap"])

# TAB 1 — TIME SERIES
with tab1:
    st.subheader(f"{', '.join(selected_pollutant)} over Time")

    if melted.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    pollutant_chart = (
        alt.Chart(melted)
        .mark_line()
        .encode(
            x="timestamp:T",
            y=alt.Y("value:Q"),
            color="city:N",
            strokeDash="pollutant:N",
            tooltip=["timestamp", "city", "pollutant", "value"]        )
        .properties(width=300, height=300)    )

    pollutant_facet = pollutant_chart.facet(
        column="city:N",
        title="Pollutant over Time"    )

    st.altair_chart(pollutant_facet, use_container_width=True)


# TAB 2 — HEATMAP
with tab2:
    if hourly_avg.empty:
        st.warning("No data available for the selected filters.")
    else:
        base = (
            alt.Chart(hourly_avg)
            .mark_rect()
            .encode(
                x=alt.X("pollutant:N", title="Pollutant"),
                y=alt.Y("hour:O", title="Hour of Day"),
                color=alt.Color("value:Q", scale=alt.Scale(scheme="inferno")),
                tooltip=["city", "hour", "pollutant", "value"]            )
            .properties(width=300, height=300)        )

        heatmap = base.facet(
            column="city:N",
            title="Hourly Pollution Pattern by City"        )

        st.altair_chart(heatmap, use_container_width=True)

