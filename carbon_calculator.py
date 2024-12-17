import streamlit as st

# Title
st.title("Carbon Calculator")


# Input Company Name
st.subheader("Company Name")
cname = st.text_input("Company Name")


# Energy Usage
st.subheader("Energy Usage")
ebill = st.number_input("What is your average monthly electricity bill in euros?", min_value=0.0)
gbill = st.number_input("What is your average monthly natural gas bill in euros?", min_value=0.0)
fbill = st.number_input("What is your average monthly fuel bill for transportation in euros?", min_value=0.0)


# Waste
st.subheader("Waste")
waste = st.number_input("How much waste do you generate per month in kilograms?", min_value=0.0)
recycle = st.number_input("How much of that waste is recycled or composted (in percentage)?", min_value=0.0, max_value=100.0)


# Business Travel
st.subheader("Business Travel")
purpose = st.number_input("How many kilometers do your employees travel per year for business purposes?", min_value=0.0)
liters = st.number_input("What is the average fuel efficiency of the vehicles used for business travel in liters per 100 kilometers?", min_value=0.0)

