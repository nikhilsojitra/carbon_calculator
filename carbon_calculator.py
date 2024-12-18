import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class Carbon_calculator:
    def __init__(self,cname,ebill,gbill,fbill,waste,recycle,purpose,liters):
        self.cname = cname
        self.ebill = ebill
        self.gbill = gbill
        self.fbill = fbill
        self.waste = waste
        self.recycle = recycle
        self.purpose = purpose
        self.liters = liters
        self.sum1 = (ebill * 12 * 0.0005) + (gbill * 12 * 0.0053) + (fbill * 12 * 2.32)
        self.sum2 = waste * 12 * (0.57 - (recycle / 100))
        if liters != 0:
            self.sum3 = purpose * (1 / liters) * 2.31
        else:
            self.sum3 = 0
            st.write("Note: Enter liters greater than 0.")
        data = {
                    "Category": ["Energy Usage", "Waste", "Business Travel"],
                    "kgCO2": [self.sum1, self.sum2, self.sum3]
                }
        self.df = pd.DataFrame(data)

     # Generate Result
    def generate_result(self):
        if st.button("Generate Result"):
            # Display Company name
            st.subheader("Company Name")
            st.write(cname)

            # Display Table
            st.subheader("Results")
            st.table(self.df)

            # Generate Bar Graph
            st.subheader("Bar Graph")
            plt.figure(figsize=(8, 5))
            plt.bar(self.df["Category"], self.df["kgCO2"], color=['blue', 'green', 'orange'])
            plt.xlabel("Category")
            plt.ylabel("kgCO2")
            plt.title("Carbon Emission")
            st.pyplot(plt)


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

cc = Carbon_calculator(cname,ebill,gbill,fbill,waste,recycle,purpose,liters)
cc.generate_result()