# auth.py

import os
import json
import urllib.parse
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8501'  # Adjust if your app runs on a different port

AUTH0_BASE_URL = f'https://{AUTH0_DOMAIN}'
AUTH0_AUTHORIZE_URL = f'{AUTH0_BASE_URL}/authorize'
AUTH0_TOKEN_URL = f'{AUTH0_BASE_URL}/oauth/token'
AUTH0_USERINFO_URL = f'{AUTH0_BASE_URL}/userinfo'
AUTH0_LOGOUT_URL = f'{AUTH0_BASE_URL}/v2/logout'

def login():
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                          scope='openid profile email',
                          redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.create_authorization_url(AUTH0_AUTHORIZE_URL)

    # Save state in session
    st.session_state['auth0_state'] = state

    # Redirect user to Auth0 for authentication
    st.write(f"Please [login here]({authorization_url})")

def logout():
    # Clear user session
    st.session_state.clear()
    # Redirect to Auth0 logout endpoint
    params = {'returnTo': REDIRECT_URI, 'client_id': CLIENT_ID}
    logout_url = f'{AUTH0_LOGOUT_URL}?{urllib.parse.urlencode(params)}'
    st.write(f"You have been logged out. Please [login again]({logout_url})")

def get_token(code):
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET,
                          redirect_uri=REDIRECT_URI)
    token = oauth.fetch_token(AUTH0_TOKEN_URL, code=code)
    return token

def get_user_info(token):
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, token=token)
    userinfo = oauth.get(AUTH0_USERINFO_URL).json()
    return userinfo

def is_authenticated():
    return 'user' in st.session_state
