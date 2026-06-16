import streamlit as st
from utils.auth import login_user

def show():
    st.markdown("<h1 style='text-align: center; color: #4361ee;'>NayePankh Foundation</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Admin Dashboard Login</h4>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if login_user(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
                    
        st.info("Default Credentials: admin / nayepankh@2024")
