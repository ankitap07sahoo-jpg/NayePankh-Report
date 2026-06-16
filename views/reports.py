import streamlit as st
import pandas as pd
from database.connection import get_session
from database.models import Volunteer, Beneficiary, Donation, Program
from utils.auth import require_auth
from utils.pdf_generator import generate_pdf_report

require_auth()

if st.session_state['role'] != 'admin':
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("Reports & Exports")

st.markdown("Download comprehensive data and summary reports for the foundation.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("PDF Summary Report")
    st.write("Generate a formatted PDF containing high-level statistics and aggregations.")
    
    pdf_buffer = generate_pdf_report()
    
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_buffer,
        file_name="NayePankh_Summary_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

with col2:
    st.subheader("CSV Data Exports")
    st.write("Download raw database tables as CSV files for spreadsheet analysis.")
    
    session = get_session()
    
    # Volunteers CSV
    v_data = pd.read_sql_query("SELECT id, name, email, phone, city, skills, is_active, join_date FROM volunteers", session.bind)
    v_csv = v_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Volunteers CSV", data=v_csv, file_name='volunteers.csv', mime='text/csv', use_container_width=True)
    
    # Donations CSV
    d_data = pd.read_sql_query("SELECT id, donor_name, amount, date, purpose, payment_mode FROM donations", session.bind)
    d_csv = d_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Donations CSV", data=d_csv, file_name='donations.csv', mime='text/csv', use_container_width=True)
    
    # Beneficiaries CSV
    b_data = pd.read_sql_query("SELECT id, name, age, gender, education_level, location, status FROM beneficiaries", session.bind)
    b_csv = b_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Beneficiaries CSV", data=b_csv, file_name='beneficiaries.csv', mime='text/csv', use_container_width=True)
    
    session.close()
