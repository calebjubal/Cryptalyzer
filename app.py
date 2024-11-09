

import streamlit as st
from auth import login, logout, get_token, get_user_info, is_authenticated


st.set_page_config(page_title="Cryptalyzer", page_icon="💰")


if 'user' not in st.session_state:
    st.session_state['user'] = None


if not is_authenticated():
    params = st.query_params
    if 'code' in params and 'state' in params:
        code = params['code']
        state = params['state']

    
        if isinstance(code, list):
            code = code[0]
        if isinstance(state, list):
            state = state[0]

     
        stored_state = st.session_state.get('auth0_state')

    
        st.write(f"Received state: {state}")
        st.write(f"Stored state: {stored_state}")

   
        if state != stored_state:
            st.error("State parameter mismatch. Possible CSRF attack.")
        else:
        
            token = get_token(code, state)
            if token:
               
                user_info = get_user_info(token)
                if user_info:
                    
                    st.session_state['user'] = user_info

                   
                    st.experimental_set_query_params()

          
                    st.experimental_rerun()
                else:
                    st.error("Failed to retrieve user information.")
            else:
                st.error("Authentication failed due to state mismatch.")
    else:

        login()
else:

    user = st.session_state['user']
    st.sidebar.write(f"Welcome, {user.get('name', 'User')}!")
    if st.sidebar.button("Logout"):
        logout()

    st.title("Cryptalyzer Dashboard")
    st.write("🔍 Analyze cryptocurrency sentiment data here!")

