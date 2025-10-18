import streamlit as st
import requests

st.title("✈️ Flight Booking Simulator")

backend_url = "http://127.0.0.1:8000/api/flights/"

if st.button("Show All Flights"):
    res = requests.get(backend_url)
    if res.status_code == 200:
        flights = res.json()
        for f in flights:
            st.write(f"{f['airline']} — {f['origin']} → {f['destination']} | ₹{f['base_fare']}")
    else:
        st.error("Failed to fetch flights.")
