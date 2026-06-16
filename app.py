import streamlit as st

st.set_page_config(
    page_title="NayePankh Foundation",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['role'] = 'viewer'

if not st.session_state['authenticated']:
    import views.login as login
    # login.show() is called inside views.login
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
