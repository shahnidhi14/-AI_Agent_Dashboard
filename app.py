import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="AI Pricing Optimizer", page_icon="💷", layout="centered")

st.title("💷 AI Pricing Optimizer Dashboard")
st.markdown("Compare Airbnb & Booking.com listings and get smart pricing suggestions.")

# ---- INPUT SECTION ----
with st.form("pricing_form"):
    st.subheader("📋 Enter Listing Details")

    listing_name = st.text_input("Listing Name", placeholder="e.g., Modern 4BR Home Manchester")
    location = st.text_input("Location", placeholder="e.g., Manchester M9 or Salford Quays")
    guests = st.number_input("Number of Guests", min_value=1, max_value=10, value=2)
    current_price = st.number_input("Current Price (£)", min_value=50, max_value=500, value=120)
    col1, col2 = st.columns(2)
    check_in = col1.date_input("Check-in Date", value=date(2025, 11, 1))
    check_out = col2.date_input("Check-out Date", value=date(2025, 11, 20))

    submitted = st.form_submit_button("Analyze Pricing 💡")

# ---- CALL WEBHOOK ----
if submitted:
    st.info("⏳ Analyzing pricing data... please wait 10–20 seconds.")
    payload = {
        "listing_name": listing_name,
        "location": location,
        "guests": guests,
        "check_in": check_in.strftime("%d-%m-%y"),
        "check_out": check_out.strftime("%d-%m-%y"),
        "current_price": current_price
    }

    try:
        webhook_url = "https://nidhig.app.n8n.cloud/webhook/ai-pricing"
        response = requests.post(webhook_url, json=payload)
        data = response.json()

        # ---- OUTPUT DISPLAY ----
        st.success("✅ Analysis Complete!")

        # Display pricing recommendations
        st.subheader("💡 AI Pricing Recommendation")
        st.markdown(f"**Suggested Target Price:** £{data.get('recommended_price', 'N/A')}")
        st.markdown(f"**Recommendation Summary:** {data.get('recommendation_text', 'N/A')}")

        # Display competitor summary
        if 'competitors' in data:
            st.subheader("📊 Competitor Overview")
            comp_df = pd.DataFrame(data['competitors'])
            st.dataframe(comp_df)

        # Display calendar-based visualization if available
        if 'calendar' in data:
            st.subheader("📆 Occupancy & Price Calendar")
            cal_df = pd.DataFrame(data['calendar'])
            st.dataframe(cal_df)

    except Exception as e:
        st.error(f"⚠️ Error: Could not fetch data. Details: {e}")
