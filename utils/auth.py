import streamlit as st
import bcrypt
from database.connection import get_session
from database.models import User

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_user(username, password):
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    
    if user and check_password(password, user.password_hash):
        st.session_state['authenticated'] = True
        st.session_state['username'] = user.username
        st.session_state['role'] = user.role
        return True
    return False

def logout_user():
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.session_state['role'] = None
    
def require_auth():
    if not st.session_state.get('authenticated', False):
        st.warning("Please log in to access this page.")
        st.stop()
