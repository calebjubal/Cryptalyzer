

import os
import urllib.parse
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv


load_dotenv()


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')  
CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8501'  


AUTH0_BASE_URL = f'https://{AUTH0_DOMAIN}'
AUTH0_AUTHORIZE_URL = f'{AUTH0_BASE_URL}/authorize'
AUTH0_TOKEN_URL = f'{AUTH0_BASE_URL}/oauth/token'
AUTH0_USERINFO_URL = f'{AUTH0_BASE_URL}/userinfo'
AUTH0_LOGOUT_URL = f'{AUTH0_BASE_URL}/v2/logout'

def login():
    """
    Initiates the login process by redirecting the user to Auth0's authorization URL.
    """
    oauth = OAuth2Session(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope='openid profile email',
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = oauth.create_authorization_url(AUTH0_AUTHORIZE_URL)

    
    st.session_state['auth0_state'] = state

    
    st.write(f"Stored state: {st.session_state['auth0_state']}")

    
    redirect_html = f'''
    <meta http-equiv="refresh" content="0; url={authorization_url}">
    '''
    st.write("Redirecting to the login page...")
    st.markdown(redirect_html, unsafe_allow_html=True)
    st.stop()

def logout():
    """
    Logs out the user by clearing the session state and redirecting to Auth0's logout URL.
    """
   
    st.session_state.clear()

    
    params = {'returnTo': REDIRECT_URI, 'client_id': CLIENT_ID}
    logout_url = f'{AUTH0_LOGOUT_URL}?{urllib.parse.urlencode(params)}'

    
    redirect_html = f'''
    <meta http-equiv="refresh" content="0; url={logout_url}">
    '''
    st.write("You have been logged out.")
    st.markdown(redirect_html, unsafe_allow_html=True)
    st.stop()

def get_token(code, state):
    """
    Exchanges the authorization code for an access token after validating the state parameter.

    Parameters:
    - code (str): The authorization code received from Auth0.
    - state (str): The state parameter received from Auth0.

    Returns:
    - dict: The access token and related information if successful.
    - None: If there is a state mismatch or token fetching fails.
    """
    
    stored_state = st.session_state.get('auth0_state')
    if state != stored_state:
        st.error("State parameter mismatch. Possible CSRF attack.")
        return None

    oauth = OAuth2Session(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI
    )
    try:
        token = oauth.fetch_token(
            AUTH0_TOKEN_URL,
            code=code,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI
        )
        return token
    except Exception as e:
        st.error(f"An error occurred while fetching the token: {e}")
        return None

def get_user_info(token):
    """
    Retrieves user information from Auth0 using the access token.

    Parameters:
    - token (dict): The access token obtained from Auth0.

    Returns:
    - dict: User information if successful.
    - None: If fetching user info fails.
    """
    oauth = OAuth2Session(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token=token
    )
    try:
        userinfo = oauth.get(AUTH0_USERINFO_URL).json()
        return userinfo
    except Exception as e:
        st.error(f"An error occurred while fetching user info: {e}")
        return None

def is_authenticated():
    """
    Checks if the user is authenticated by verifying if user information exists in session state.

    Returns:
    - bool: True if authenticated, False otherwise.
    """
    return 'user' in st.session_state and st.session_state['user'] is not None
