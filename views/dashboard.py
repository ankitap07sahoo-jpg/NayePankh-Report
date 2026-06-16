import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy.sql import func
from database.connection import get_session
from database.models import Volunteer, Beneficiary, Donation, Program
from utils.auth import require_auth

require_auth()

st.title("Dashboard Overview")

session = get_session()

# Metrics
total_volunteers = session.query(Volunteer).filter_by(is_active=True).count()
total_beneficiaries = session.query(Beneficiary).count()
total_donations = session.query(func.sum(Donation.amount)).scalar() or 0.0
active_programs = session.query(Program).filter(Program.status.in_(['upcoming', 'ongoing'])).count()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Volunteers", total_volunteers)
col2.metric("Beneficiaries", total_beneficiaries)
col3.metric("Total Donations", f"₹{total_donations:,.2f}")
col4.metric("Active Programs", active_programs)

st.divider()

# Charts
st.subheader("Analytics")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("**Donations by Purpose**")
    donations_data = session.query(Donation.purpose, func.sum(Donation.amount).label('total')).group_by(Donation.purpose).all()
    if donations_data:
        df_donations = pd.DataFrame(donations_data, columns=['Purpose', 'Amount'])
        df_donations['Purpose'] = df_donations['Purpose'].fillna('General')
        # Custom dark pink and dark green theme for the pie chart
        fig = px.pie(df_donations, values='Amount', names='Purpose', hole=0.4, color_discrete_sequence=["#d81159", "#2d6a4f", "#ff477e", "#40916c"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No donation data available.")

with col_chart2:
    st.markdown("**Programs by Status**")
    programs_data = session.query(Program.status, func.count(Program.id).label('count')).group_by(Program.status).all()
    if programs_data:
        df_programs = pd.DataFrame(programs_data, columns=['Status', 'Count'])
        # Custom dark blue theme for the bar chart
        fig2 = px.bar(df_programs, x='Status', y='Count', color='Status', color_discrete_sequence=["#1d3557", "#457b9d", "#03045e"])
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No program data available.")

session.close()
