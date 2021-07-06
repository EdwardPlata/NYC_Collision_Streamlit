import streamlit as st

import pandas as pd
import numpy as np

DATA_URL = (
"/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("NYC Motor Vehicle Collisions")
st.markdown("This application is a streamlit dashboard that can be used to monitor vehicle collisions in NYC")

# LEt's load our data
@st.cache(persist=True)

def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows = nrows, parse_dates = [['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=["LATITUDE","LONGITUDE"], inplace=True)
    lowercase = lambda x : str(x).lower()
    data.rename(lowercase,axis='columns', inplace= True)
    data.rename(columns ={'crash_date_crash_time':'date/time'}, inplace=True )
    return data

data = load_data(10000)

st.header("Where are the most people injured in NYC")
injured_people = st.slider("Number of persons injured in vehicles",0,19)
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))

st.header("How many collisions occur during a given time of date?")
#hour = st.sidebar.selectbox("Hour to look at",range(0,24),1)
hour= st.sidebar.slider("Hour to look at",0,23)
data = data[data['date/time'].dt.hour==hour]


if st.checkbox("Show Raw Data",False):
    st.subheader('Raw Data')
    st.write(data)
