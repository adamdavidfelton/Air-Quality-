#import modules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
#terminal setup
pd.options.display.max_rows = 100
pd.options.display.width = 0
alt.data_transformers.disable_max_rows()
#read csv
air = pd.read_csv("C:/Users/adamd/Documents/airquality.csv")
#clean file
air["timestamp"] = pd.to_datetime(air["timestamp"])
#create filter lists
##country filter
country_list = sorted(air["country"].unique())
selected_country = st.sidebar.selectbox("Select Country", country_list)
##city filter
city_list = sorted(air[air["country"] == selected_country]["city"].unique())
selected_city = st.sidebar.selectbox("select City", city_list)
##pollutant filter
pollutants = ["pm25", "pm10", "no2", "so2", "o3", "co"]
selected_pollutant =st.sidebar.selectbox("Select Pollutant", pollutants)
### filtered dataset
filt_air = air[(air["country"] == selected_country) & (air["city"] == selected_city)]

#create plots/tabs
tab1, tab2 = st.tabs(["Pollutants over Time","somethingelse"])
with tab1:
    st.subheader(f"{selected_pollutant} over Time")
    pollutant_chart = (alt.Chart(filt_air).mark_line().encode(x="timestamp:T",y=alt.Y(f"{selected_pollutant}:Q"), tooltip=["timestamp", "pm25"]).properties(width="container",height=400))
    st.altair_chart(pollutant_chart, use_container_width=True)

