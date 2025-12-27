#import modules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import pycountry
#terminal setup
pd.options.display.max_rows = 100
pd.options.display.width = 0
alt.data_transformers.disable_max_rows()
#read csv
air = pd.read_csv("C:/Users/adamd/Documents/airquality.csv")
#clean file
air["timestamp"] = pd.to_datetime(air["timestamp"])
def convert_country(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code
air["country"] = air["country"].apply(convert_country)
#streamlit settings
st.set_page_config(layout="wide")
apply_rolling = st.sidebar.checkbox("Apply Rolling Average (6‑hour)")
#create filter lists
##country filter
country_list = sorted(air["country"].unique())
selected_country = st.sidebar.multiselect("Select Country", sorted(air["country"].unique()))
##city filter
city_list = sorted(air[air["country"].isin(selected_country)]["city"].unique())
selected_city = st.sidebar.multiselect("Select City", city_list)
##pollutant filter
pollutants = ["pm25", "pm10", "no2", "so2", "o3", "co"]
selected_pollutant =st.sidebar.multiselect("Select Pollutant", ["pm25", "pm10", "no2", "so2", "o3", "co"])
if not selected_city or not selected_pollutant:
    st.warning("Please select a city or pollutant")
    st.stop()
### filtered dataset
filt_air = air[(air["country"].isin(selected_country)) & (air["city"].isin(selected_city))]
#smooth columns
if apply_rolling:
    filt_air[selected_pollutant] = (filt_air[selected_pollutant].rolling(window=6, min_periods=1).mean())


#melted
melted = filt_air.melt(id_vars=["timestamp", "country", "city"], value_vars=selected_pollutant,
                       var_name="pollutant", value_name="value")
#create plots/tabs
tab1, tab2 = st.tabs(["Pollutants over Time","somethingelse"])
with tab1:
    st.subheader(f"{'.'.join(selected_pollutant)} over Time")
    pollutant_chart = (alt.Chart(melted).mark_line().encode(x="timestamp:T",y=alt.Y("value:Q"),color="city:N", strokeDash="pollutant:N",
                            tooltip=["timestamp", "city", "pollutant","value"]).properties(width="container",height=700, title="Pollutant over Time"))
    st.altair_chart(pollutant_chart, use_container_width=True)


