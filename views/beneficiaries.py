import streamlit as st
import pandas as pd
from database.connection import get_session
from database.models import Beneficiary
from utils.auth import require_auth

require_auth()

st.title("Beneficiaries Management")

session = get_session()

# Fetch data for dataframe
beneficiaries = session.query(Beneficiary).all()
if beneficiaries:
    df = pd.DataFrame([{
        'ID': b.id,
        'Name': b.name,
        'Age': b.age,
        'Gender': b.gender,
        'Education Level': b.education_level,
        'Location': b.location,
        'Status': b.status
    } for b in beneficiaries])
else:
    df = pd.DataFrame(columns=['ID', 'Name', 'Age', 'Gender', 'Education Level', 'Location', 'Status'])

st.subheader("Beneficiary Directory")

col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    search = st.text_input("Search by Name or Location...")
with col_s2:
    status_filter = st.selectbox("Filter by Status", ["All", "Active", "Completed", "Dropout"])

# Apply filters
if search:
    df = df[df['Name'].str.contains(search, case=False) | df['Location'].astype(str).str.contains(search, case=False)]

if status_filter != "All":
    df = df[df['Status'].str.lower() == status_filter.lower()]

st.dataframe(df, hide_index=True, use_container_width=True)

if st.session_state['role'] == 'admin':
    st.divider()
    st.subheader("Add New Beneficiary")
    with st.form("add_beneficiary_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=1, max_value=100, step=1)
            education_level = st.text_input("Education Level")
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            location = st.text_input("Location")
            status = st.selectbox("Status", ["active", "completed", "dropout"])
            
        submitted = st.form_submit_button("Add Beneficiary")
        
        if submitted:
            if name:
                new_b = Beneficiary(
                    name=name, age=age, gender=gender, 
                    education_level=education_level, location=location, status=status
                )
                try:
                    session.add(new_b)
                    session.commit()
                    st.success(f"Beneficiary {name} added successfully!")
                    st.rerun()
                except Exception as e:
                    session.rollback()
                    st.error(f"Error adding beneficiary: {str(e)}")
            else:
                st.warning("Name is required.")

session.close()
