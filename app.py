import streamlit as st

st.set_page_config(
    page_title="NayePankh Foundation",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to force a dark sidebar but keep inputs white
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #0e1117 !important;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebarNavItems"] a {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] button {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
            border: 1px solid #00b4d8 !important;
            font-weight: bold !important;
        }
        [data-testid="stSidebar"] button:hover {
            background-color: #0077b6 !important;
            border: 1px solid #0077b6 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Auto-seed the database if it's empty (specifically for Streamlit Cloud deployments)
from database.connection import get_session
from database.models import User
try:
    session = get_session()
    if session.query(User).count() == 0:
        import seed_data
        seed_data.seed()
    session.close()
except Exception:
    pass

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['role'] = 'viewer'

if not st.session_state['authenticated']:
    import views.login as login
    login.show()
else:
    # Navigation
    from utils.auth import logout_user
    
    dashboard_page = st.Page("views/dashboard.py", title="Dashboard", icon="📊", default=True)
    volunteers_page = st.Page("views/volunteers.py", title="Volunteers", icon="🤝")
    beneficiaries_page = st.Page("views/beneficiaries.py", title="Beneficiaries", icon="🎓")
    donations_page = st.Page("views/donations.py", title="Donations", icon="💰")
    programs_page = st.Page("views/programs.py", title="Programs", icon="📅")
    reports_page = st.Page("views/reports.py", title="Reports", icon="📄")
    
    # Hide donations from viewers if needed
    pages = [dashboard_page, volunteers_page, beneficiaries_page, programs_page, reports_page]
    
    if st.session_state['role'] == 'admin':
        pages.insert(3, donations_page)
        
    pg = st.navigation({
        "Menu": pages
    })
    
    with st.sidebar:
        st.markdown(f"**Logged in as:** {st.session_state.get('username', 'User')}")
        st.markdown(f"**Role:** {st.session_state.get('role', 'Viewer').title()}")
        if st.button("Logout"):
            logout_user()
            st.rerun()
            
    pg.run()
