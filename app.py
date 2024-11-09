# app.py

import streamlit as st
from auth import login, logout, get_token, get_user_info, is_authenticated
import urllib.parse

st.set_page_config(page_title="Cryptalyzer", page_icon="💰")

if not is_authenticated():
    params = st.get_query_params()
    if 'code' in params:
        code = params['code'][0]
        # Retrieve token
        token = get_token(code)
        # Retrieve user info
        user_info = get_user_info(token)
        # Save user info in session
        st.session_state['user'] = user_info
        # Clear query params
        st.set_query_params()
        st.experimental_rerun()
    else:
        login()
else:
    user = st.session_state['user']
    st.sidebar.write(f"Welcome, {user['name']}!")
    if st.sidebar.button("Logout"):
        logout()

    # Your main application code here
    st.title("Cryptalyzer Dashboard")
    # ... rest of your app
