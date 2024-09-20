import streamlit as st
import pyodbc
import hashlib

# Function to connect to the SQL Server
def init_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-OJD0AB2\SQLEXPRESS;'
        'DATABASE=RecoMaster;'
        'Trusted_Connection=yes;'
    )
    return connection

# Function to create the table if it doesn't exist
def create_table():
    conn = init_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if a user already exists
def user_exists(username):
    conn = init_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = cursor.fetchone()
    conn.close()
    return data is not None

# Function to add a new user
def add_user(username, email, password):
    conn = init_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute('''
        INSERT INTO users (username, email, password) 
        VALUES (?, ?, ?)
    ''', (username, email, hashed_password))
    conn.commit()
    conn.close()

# Create the table if not exists
create_table()

# Streamlit UI for Sign Up
st.title("Sign Up")

username = st.text_input("Enter your username")
email = st.text_input("Enter your email")
password = st.text_input("Enter your password", type="password")

if st.button("Sign Up"):
    if username and email and password:
        if not user_exists(username):
            add_user(username, email, password)
            st.success("Sign up successful! You can now log in.")
        else:
            st.error("Username already exists.")
    else:
        st.error("Please fill in all fields.")

# Link to the login page
st.write("Already have an account? [Log In here](../Login)")

# import streamlit as st
# import pyodbc
# import hashlib
# import streamlit_authenticator as stauth
# from oauthlib.oauth2 import WebApplicationClient
# import requests

# # Google OAuth configuration
# GOOGLE_CLIENT_ID = '427732006510-vcrt4pqlaasur7o15ec4uufdopamg3r5.apps.googleusercontent.com'
# GOOGLE_CLIENT_SECRET = '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'
# GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# # Function to connect to the SQL Server
# def init_db_connection():
#     connection = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         'SERVER=DESKTOP-OJD0AB2\SQLEXPRESS;'
#         'DATABASE=RecoMaster;'
#         'Trusted_Connection=yes;'
#     )
#     return connection

# # Function to create the table if it doesn't exist
# def create_table():
#     conn = init_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
#         CREATE TABLE users (
#             id INT IDENTITY(1,1) PRIMARY KEY,
#             username VARCHAR(255) NOT NULL,
#             email VARCHAR(255) NOT NULL,
#             password VARCHAR(255) NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # Function to hash passwords
# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

# # Function to check if a user already exists
# def user_exists(username):
#     conn = init_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
#     data = cursor.fetchone()
#     conn.close()
#     return data is not None

# # Function to add a new user
# def add_user(username, email, password):
#     conn = init_db_connection()
#     cursor = conn.cursor()
#     hashed_password = hash_password(password)
#     cursor.execute('''
#         INSERT INTO users (username, email, password) 
#         VALUES (?, ?, ?)
#     ''', (username, email, hashed_password))
#     conn.commit()
#     conn.close()

# # Create the table if not exists
# create_table()

# # Streamlit UI for Sign Up
# st.title("Sign Up")

# username = st.text_input("Enter your username")
# email = st.text_input("Enter your email")
# password = st.text_input("Enter your password", type="password")

# if st.button("Sign Up"):
#     if username and email and password:
#         if not user_exists(username):
#             add_user(username, email, password)
#             st.success("Sign up successful! You can now log in.")
#         else:
#             st.error("Username already exists.")
#     else:
#         st.error("Please fill in all fields.")

# # Google login
# client = WebApplicationClient(GOOGLE_CLIENT_ID)

# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()

# if st.button("Sign Up with Google"):
#     # Get provider configuration
#     google_provider_cfg = get_google_provider_cfg()
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
#     # Create the authorization URL
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri="http://localhost:8501",
#         scope=["openid", "email", "profile"],
#     )
    
#     # Redirect to Google OAuth login page
#     st.write(f'<a href="{request_uri}">Sign In with Google</a>', unsafe_allow_html=True)

# # Link to the login page
# st.write("Already have an account? [Log In here](../Login)")

