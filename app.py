import streamlit as st
import pandas as pd
import altair as alt
import json
from datetime import datetime
from streamlit.web.server.websocket_headers import _get_websocket_headers

st.set_page_config(page_title="AI Pricing Dashboard", layout="wide")

st.title("💷 AI Pricing Agent Dashboard (Live Updates via n8n)")

# Load or create empty DataFrame
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Date", "Occupancy", "Recommended Price (£)"])

# Webhook listener
headers = _get_websocket_headers()
if headers and "x-streamlit-webhook" in headers:
    payload = json.loads(headers["x-streamlit-webhook"])
    new_row = pd.DataFrame([payload])
    st.session_state["data"] = pd.concat([st.session_state["data"], new_row], ignore_index=True)

# Display chart
df = st.session_state["data"]
if not df.empty:
    chart = alt.Chart(df).mark_bar().encode(
        x="Date",
        y="Recommended Price (£)",
        color=alt.condition(
            alt.datum.Occupancy > 80, alt.value("#16a34a"), alt.value("#dc2626")
        ),
        tooltip=["Date", "Recommended Price (£)", "Occupancy"]
    )
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(df)
else:
    st.info("Waiting for live data from n8n webhook...")
