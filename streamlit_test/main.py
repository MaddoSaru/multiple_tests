import streamlit as st
import pandas as pd
from utils.general_functions import csv_to_df

dataframe = csv_to_df()
dataframe["date"] = pd.to_datetime(dataframe["date"]).dt.date

btc_price_df = (
    dataframe[["date", "close"]].rename(columns={"date": "index"}).set_index("index")
)
btc_last_30_days_price_df = btc_price_df.tail(30)
btc_last_90_days_price_df = btc_price_df.tail(90)

min_date = dataframe.date.min()
max_date = dataframe.date.max()
date_format = "MMM DD, YYYY"

# Main Page
st.markdown("# BTC Stats")
st.sidebar.markdown("# Main Page")

data_container = st.container()

with data_container:
    min_price, max_price = st.columns(2)
    with min_price:
        f"BTC Min Price Since {min_date}"
        st.markdown(
            f'<h1 style="font-size:20px; color: black; background-color: #FFCCCB; text-align: center;">{btc_price_df["close"].min()}</h1>',
            unsafe_allow_html=True,
        )
    with max_price:
        f"BTC Max Price Since {min_date}"
        st.markdown(
            f'<h1 style="font-size:20px; color: black; background-color: #ADD8E6; text-align: center;">{btc_price_df["close"].max()}</h1>',
            unsafe_allow_html=True,
        )

st.markdown("")
st.markdown(
    '<h1 style="font-size: 25px;">Check the BTC Price at Any Date</h1>',
    unsafe_allow_html=True,
)

date = st.slider(
    "Select Date", min_value=min_date, max_value=max_date, format=date_format
)
st.write(
    f'<h1 style="font-size:20px;">BTC Price on {date.strftime("%A %d of %b, %Y")} is {btc_price_df.loc[btc_price_df.index == date]["close"].iloc[0]} USD</h1>',
    unsafe_allow_html=True,
)

st.markdown('<h1 style="font-size:25px;">BTC Price Chart</h1>', unsafe_allow_html=True)
st.line_chart(btc_price_df)

data_container_2 = st.container()

with data_container_2:
    chart_1, chart_2 = st.columns(2)
    with chart_1:
        "BTC Last 30 Days Price Chart"
        st.line_chart(btc_last_30_days_price_df)
    with chart_2:
        "BTC Last 90 Days Price Chart"
        st.line_chart(btc_last_90_days_price_df)
