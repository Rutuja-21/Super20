# import streamlit as st
# import pyodbc
# import hashlib

# # Function to connect to the SQL Server
# def init_db_connection():
#     connection = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         'SERVER=DESKTOP-OJD0AB2\SQLEXPRESS;'  
#         'DATABASE=RecoMaster;'
#         'Trusted_Connection=yes;'
#     )
#     return connection

# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Function to validate user login
# def login_user(username, password):
#     conn = init_db_connection()
#     cursor = conn.cursor()
#     hashed_password = hash_password(password)
#     cursor.execute('''
#         SELECT * FROM users WHERE username = ? AND password = ?
#     ''', (username, hashed_password))
#     data = cursor.fetchone()
#     conn.close()
#     return data is not None

# # Streamlit UI for Log In
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False

# if not st.session_state.logged_in:
#     st.title("Log In")

#     username = st.text_input("Enter your username")
#     password = st.text_input("Enter your password", type="password")

#     if st.button("Log In"):
#         if username and password:
#             if login_user(username, password):
#                 st.session_state.logged_in = True
#                 st.success(f"Welcome, {username}!")
#                 # Use a form or another mechanism to reload or redirect
#                 # st.experimental_rerun() 
#             else:
#                 st.error("Invalid username or password.")
#         else:
#             st.error("Please fill in all fields.")

#     # Link to the sign-up page
#     st.write("Don't have an account? [Sign Up here](../Signup)")

# else:
#     st.write("You are already logged in!")
#     st.write("You can now access the Meal Recommendation page")
    
import streamlit as st
import pyodbc
import hashlib
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests

# Function to connect to the SQL Server
def init_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-OJD0AB2\\SQLEXPRESS;'  
        'DATABASE=RecoMaster;'
        'Trusted_Connection=yes;'
    )
    return connection

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate user login
def login_user(username, password):
    conn = init_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, hashed_password))
    data = cursor.fetchone()
    conn.close()
    return data is not None

# Setup Google OAuth 2.0
GOOGLE_CLIENT_ID = "427732006510-vcrt4pqlaasur7o15ec4uufdopamg3r5.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501/Meal_Recommendation"  # This should match the URI you set in the Google Developer Console

def google_login():
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://accounts.google.com/o/oauth2/token",
            }
        },
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
    )

    flow.redirect_uri = REDIRECT_URI

    authorization_url, state = flow.authorization_url(prompt='consent')
    st.write(f"Please log in using [this link]({authorization_url})")

    query_params = st.query_params
    auth_response = query_params.get("code")

    if auth_response:
        # Exchange authorization code for access token
        flow.fetch_token(authorization_response=f"{REDIRECT_URI}?code={auth_response}")
        credentials = flow.credentials

        # Retrieve user info
        request = google.auth.transport.requests.Request()
        id_info = id_token.verify_oauth2_token(credentials.id_token, request, GOOGLE_CLIENT_ID)

        st.session_state.logged_in = True
        st.session_state.username = id_info.get("email")
        st.success(f"Welcome, {st.session_state.username}!")

# Streamlit UI for Log In
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Log In")

    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")

    if st.button("Log In"):
        if username and password:
            if login_user(username, password):
                st.session_state.logged_in = True
                st.success(f"Welcome, {username}!")
                # Use a form or another mechanism to reload or redirect
                # st.experimental_rerun() 
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please fill in all fields.")

    # Link to the sign-up page
    st.write("Don't have an account? [Sign Up here](../Signup)")

    # Google Sign-In
    st.write("Or log in with Google:")
    google_login()

else:
    st.write("You are already logged in!")
    st.write("You can now access the Meal Recommendation page")
