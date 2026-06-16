import streamlit as st
import pandas as pd
from database.connection import get_session
from database.models import Volunteer
from utils.auth import require_auth
from datetime import date

require_auth()

st.title("Volunteers Management")

session = get_session()

# Fetch data for dataframe
volunteers = session.query(Volunteer).all()
if volunteers:
    df = pd.DataFrame([{
        'ID': v.id,
        'Name': v.name,
        'Email': v.email,
        'Phone': v.phone,
        'City': v.city,
        'Skills': v.skills,
        'Active': v.is_active,
        'Join Date': v.join_date
    } for v in volunteers])
else:
    df = pd.DataFrame(columns=['ID', 'Name', 'Email', 'Phone', 'City', 'Skills', 'Active', 'Join Date'])

st.subheader("Volunteer Directory")

search = st.text_input("Search by Name or City...")
if search:
    df = df[df['Name'].str.contains(search, case=False) | df['City'].str.contains(search, case=False)]

st.dataframe(df, hide_index=True, use_container_width=True)

if st.session_state['role'] == 'admin':
    st.divider()
    st.subheader("Add New Volunteer")
    with st.form("add_volunteer_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            phone = st.text_input("Phone")
            skills = st.text_input("Skills (comma separated)")
        with col2:
            email = st.text_input("Email")
            city = st.text_input("City")
            is_active = st.checkbox("Is Active", value=True)
            
        submitted = st.form_submit_button("Add Volunteer")
        
        if submitted:
            if name and email and phone and city:
                new_v = Volunteer(
                    name=name, email=email, phone=phone, city=city, 
                    skills=skills, is_active=is_active, join_date=date.today()
                )
                try:
                    session.add(new_v)
                    session.commit()
                    st.success(f"Volunteer {name} added successfully!")
                    st.rerun()
                except Exception as e:
                    session.rollback()
                    st.error(f"Error adding volunteer: {str(e)}")
            else:
                st.warning("Please fill all required fields.")

session.close()
