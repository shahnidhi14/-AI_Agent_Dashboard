import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Pricing Dashboard", layout="wide")

st.title("💷 AI Pricing Dashboard")
st.write("An intelligent tool to visualize and adjust Airbnb or rental pricing dynamically.")

# Sidebar Inputs
st.sidebar.header("📊 Pricing Configuration")
base_price = st.sidebar.number_input("Base Price per Night (£)", min_value=50, max_value=500, value=120)
min_price = st.sidebar.number_input("Minimum Price (£)", min_value=50, max_value=base_price, value=90)

weekend_adj = st.sidebar.slider("Weekend Adjustment (%)", 0, 50, 20)
event_adj = st.sidebar.slider("Local Event Adjustment (%)", 0, 50, 30)
holiday_adj = st.sidebar.slider("Holiday Adjustment (%)", 0, 50, 20)

# Date Range
dates = pd.date_range("2024-11-01", "2024-11-20")
price_data = []

for date in dates:
    day_type = "Weekday"
    price = base_price

    if date.day_name() in ["Saturday", "Sunday"]:
        price += base_price * (weekend_adj / 100)
        day_type = "Weekend"
    elif date.day in [5, 12, 19]:
        price += base_price * (event_adj / 100)
        day_type = "Local Event"
    elif date.day in [8, 15]:
        price += base_price * (holiday_adj / 100)
        day_type = "Holiday"

    price = max(price, min_price)
    price_data.append([date.date(), day_type, round(price, 2)])

df = pd.DataFrame(price_data, columns=["Date", "Type", "Suggested Price (£)"])

# Color-coding visualization
st.subheader("📅 Price Calendar")
def highlight_type(row):
    color = {
        "Weekend": "background-color: #FFD580",
        "Local Event": "background-color: #FFB6C1",
        "Holiday": "background-color: #90EE90"
    }.get(row["Type"], "")
    return [color] * len(row)

st.dataframe(df.style.apply(highlight_type, axis=1), height=450)

# Summary Stats
avg_price = df["Suggested Price (£)"].mean()
max_price = df["Suggested Price (£)"].max()
min_price = df["Suggested Price (£)"].min()

st.markdown("---")
st.subheader("📈 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Average Price", f"£{avg_price:.2f}")
col2.metric("Max Price", f"£{max_price:.2f}")
col3.metric("Min Price", f"£{min_price:.2f}")
