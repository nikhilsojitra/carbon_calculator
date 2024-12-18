import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
from fpdf import FPDF

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
        self.total = self.sum1 + self.sum2 + self.sum3     
        data = {
                    "Category": ["Energy Usage", "Waste", "Business Travel", "Total KgCO2"],
                    "kgCO2": [self.sum1, self.sum2, self.sum3, self.total]
                }
        self.df = pd.DataFrame(data)

    #Generate PDF
    def generate_pdf(self):
        st.subheader("Download Results as PDF")

            # Temporary file for the graph image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            plt.savefig(temp_file.name, format="png")
            temp_file_path = temp_file.name

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=24)
        pdf.cell(200, 10, txt="Carbon Emissions", ln=True, align='C')

        pdf.ln(10)

        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt=f"Company Name: {cname}", ln=True, align='L')
        pdf.ln(2)

        # Table Header in pdf
        pdf.set_font("Arial", size=14, style="B")
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(95, 10, "Category", border=1, align='C', fill=True)
        pdf.cell(95, 10, "kgCO2", border=1, align='C', fill=True)
        pdf.ln()

        # Table Rows in pdf
        pdf.set_font("Arial", size=12)
        for index, row in self.df.iterrows():
            pdf.cell(95, 10, row['Category'], border=1, align='C')
            pdf.cell(95, 10, f"{row['kgCO2']:.2f}", border=1, align='C')
            pdf.ln()

        pdf.ln(10)

        # Pie Graph Image to PDF
        pdf.image(temp_file_path, x=10, y=pdf.get_y(), w=190)

        # Save PDF
        pdf_output = "./carbon_emission_report.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download PDF",   
                data=file,
                file_name="carbon_emission_report.pdf",
                mime="application/pdf"
            )


     # Generate Result
    def generate_result(self):
        if st.button("Generate Result"):
            # Display Company name
            st.subheader("Company Name")
            st.write(cname)

            # Display Table
            st.subheader("Results")
            st.table(self.df)

            # Generate Pie Graph
            st.subheader("Pie Chart")
            plt.figure(figsize=(8, 8))
            colors = ['#4CAF50', '#2196F3', '#FFC107']
            explode = [0.1 if i == self.df["kgCO2"][:-1].idxmax() else 0 for i in range(len(self.df) -1)]
            plt.pie(
            self.df["kgCO2"][:-1],
            labels=self.df["Category"][:-1],
            autopct="%1.1f%%",
            startangle=140,
            explode=explode,
            colors=colors,
            shadow=True,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.2},
            textprops={'fontsize': 12, 'color': 'black'}
            )
            plt.title("Carbon Emission Distribution", fontsize=16, fontweight='bold', color='darkblue')
            st.pyplot(plt)

            # Generate PDF
            self.generate_pdf()



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