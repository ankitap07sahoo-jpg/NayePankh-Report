import streamlit as st
import pandas as pd
from database.connection import get_session
from database.models import Donation
from utils.auth import require_auth
from datetime import date

require_auth()

if st.session_state['role'] != 'admin':
    st.error("You do not have permission to view this page.")
    st.stop()

st.title("Donations Ledger")

session = get_session()

# Fetch data for dataframe
donations = session.query(Donation).order_by(Donation.date.desc()).all()
if donations:
    df = pd.DataFrame([{
        'ID': d.id,
        'Donor Name': d.donor_name,
        'Amount (INR)': d.amount,
        'Date': d.date,
        'Purpose': d.purpose,
        'Payment Mode': d.payment_mode
    } for d in donations])
else:
    df = pd.DataFrame(columns=['ID', 'Donor Name', 'Amount (INR)', 'Date', 'Purpose', 'Payment Mode'])

st.subheader("Donation Records")

col_s1, col_s2 = st.columns([2, 1])
with col_s1:
    search = st.text_input("Search by Donor Name...")
with col_s2:
    purpose_filter = st.selectbox("Filter by Purpose", ["All", "General", "Education", "Health", "Events", "Other"])

# Apply filters
if search:
    df = df[df['Donor Name'].str.contains(search, case=False)]

if purpose_filter != "All":
    df = df[df['Purpose'] == purpose_filter]

# Format amount column
if not df.empty:
    st.dataframe(df.style.format({'Amount (INR)': '₹{:.2f}'}), hide_index=True, use_container_width=True)
else:
    st.dataframe(df, hide_index=True, use_container_width=True)

st.divider()
st.subheader("Record New Donation")
with st.form("add_donation_form"):
    col1, col2 = st.columns(2)
    with col1:
        donor_name = st.text_input("Donor Name")
        amount = st.number_input("Amount (INR)", min_value=1.0, step=100.0)
        donation_date = st.date_input("Date", value=date.today())
    with col2:
        purpose = st.selectbox("Purpose", ["General", "Education", "Health", "Events", "Other"])
        payment_mode = st.selectbox("Payment Mode", ["UPI", "Bank Transfer", "Cash", "Cheque"])
        
    submitted = st.form_submit_button("Record Donation")
    
    if submitted:
        if donor_name and amount > 0:
            new_d = Donation(
                donor_name=donor_name, amount=amount, date=donation_date, 
                purpose=purpose, payment_mode=payment_mode
            )
            try:
                session.add(new_d)
                session.commit()
                st.success(f"Donation from {donor_name} recorded successfully!")
                st.rerun()
            except Exception as e:
                session.rollback()
                st.error(f"Error recording donation: {str(e)}")
        else:
            st.warning("Please provide a valid Donor Name and Amount.")

session.close()
