import streamlit as st
import pandas as pd
from database.connection import get_session
from database.models import Program, Beneficiary
from utils.auth import require_auth

require_auth()

st.title("Programs Management")

session = get_session()

# Fetch data
programs = session.query(Program).all()

st.subheader("Existing Programs")

if programs:
    for p in programs:
        with st.expander(f"{p.title} - {p.status.capitalize()}"):
            st.write(f"**Description:** {p.description}")
            col1, col2 = st.columns(2)
            col1.write(f"**Start Date:** {p.start_date}")
            col2.write(f"**End Date:** {p.end_date}")
            
            st.markdown("##### Enrolled Beneficiaries")
            if p.beneficiaries:
                b_df = pd.DataFrame([{'ID': b.id, 'Name': b.name, 'Location': b.location} for b in p.beneficiaries])
                st.dataframe(b_df, hide_index=True)
            else:
                st.write("No beneficiaries enrolled yet.")
                
            if st.session_state['role'] == 'admin':
                st.markdown("##### Manage Enrollment")
                with st.form(f"enroll_form_{p.id}"):
                    all_beneficiaries = session.query(Beneficiary).all()
                    b_options = {b.name: b for b in all_beneficiaries}
                    
                    # Currently enrolled
                    current_names = [b.name for b in p.beneficiaries]
                    
                    selected_names = st.multiselect(
                        "Select Beneficiaries", 
                        options=list(b_options.keys()),
                        default=current_names
                    )
                    
                    submitted = st.form_submit_button("Update Enrollment")
                    if submitted:
                        p.beneficiaries = [b_options[name] for name in selected_names]
                        session.commit()
                        st.success("Enrollment updated!")
                        st.rerun()
else:
    st.info("No programs created yet.")

if st.session_state['role'] == 'admin':
    st.divider()
    st.subheader("Create New Program")
    with st.form("add_program_form"):
        title = st.text_input("Program Title")
        description = st.text_area("Description")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        
        status = st.selectbox("Status", ["upcoming", "ongoing", "completed"])
            
        submitted = st.form_submit_button("Create Program")
        
        if submitted:
            if title:
                new_p = Program(
                    title=title, description=description, 
                    start_date=start_date, end_date=end_date, status=status
                )
                try:
                    session.add(new_p)
                    session.commit()
                    st.success(f"Program '{title}' created successfully!")
                    st.rerun()
                except Exception as e:
                    session.rollback()
                    st.error(f"Error creating program: {str(e)}")
            else:
                st.warning("Program Title is required.")

session.close()
