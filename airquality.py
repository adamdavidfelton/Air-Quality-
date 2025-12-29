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
#streamlit settings
st.set_page_config(layout="wide")
#clean file
air["timestamp"] = pd.to_datetime(air["timestamp"])
def convert_country(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return code
air["country"] = air["country"].apply(convert_country)

#create filter lists
##country filter
country_list = sorted(air["country"].unique())
selected_country = st.sidebar.multiselect("Select Country", country_list, default=country_list)
##city filter
city_list = sorted(air[air["country"].isin(selected_country)]["city"].unique())
selected_city = st.sidebar.multiselect("Select City", city_list)
##pollutant filter
pollutants = ["pm25", "pm10", "no2", "so2", "o3", "co"]
selected_pollutant =st.sidebar.multiselect("Select Pollutant", ["pm25", "pm10", "no2", "so2", "o3", "co"])
if not selected_city or not selected_pollutant:
    st.warning("Please select a city and pollutant")
    st.stop()
### filtered dataset
filt_air = air[(air["country"].isin(selected_country)) & (air["city"].isin(selected_city))]
filt_air["hour"] = filt_air["timestamp"].dt.hour
#smooth columns
window = st.sidebar.slider("Rolling Window (hours)", 1, 48, 6)
filt_air[selected_pollutant] = filt_air[selected_pollutant].rolling(window=window, min_periods=1).mean()
if window:
    filt_air[selected_pollutant] = (filt_air[selected_pollutant].rolling(window=6, min_periods=1).mean())

#melted
melted = filt_air.melt(id_vars=["timestamp", "country", "city"], value_vars=selected_pollutant,
                       var_name="pollutant", value_name="value")
melted_hour = filt_air.melt(id_vars=["hour", "country", "city"], value_vars=selected_pollutant,var_name="pollutant",value_name="value")
hourly_avg = melted_hour.groupby(["city","hour","pollutant"], as_index=False)["value"].mean()


#create plots/tabs
st.header("Air Quality")
tab1, tab2 = st.tabs(["Pollutants over Time","Pollution Heatmap"])
with tab1:
    #create base chart
    st.subheader(f"{', '.join(selected_pollutant)} over Time")
    pollutant_chart = (alt.Chart(melted)
                       .mark_line()
                       .encode(x="timestamp:T",y=alt.Y("value:Q"),color="city:N", strokeDash="pollutant:N", tooltip=["timestamp", "city", "pollutant","value"])
                       .properties(width=300,height=300, title="Pollutant over Time"))
   #facet by city
    pollutant_facet = pollutant_chart.facet(column="city:N",title="Pollutant over Time")
    if melted.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    st.altair_chart(pollutant_facet, width="stretch")
with tab2:
    # Create base heatmap
    base = (alt.Chart(hourly_avg)
        .mark_rect()
        .encode(x=alt.X("pollutant:N", title="Pollutant"),y=alt.Y("hour:O", title="Hour of Day"),color=alt.Color("value:Q", scale=alt.Scale(scheme="inferno")),tooltip=["city", "hour", "pollutant", "value"])
        .properties(width=300, height=300))

    # Facet by city
    heatmap = base.facet(column="city:N",title="Hourly Pollution Pattern by City")

    # Display safely
    if hourly_avg.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.altair_chart(heatmap, width="stretch")