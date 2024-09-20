import streamlit as st
import pyodbc
import hashlib
import random
import string

# Function to connect to the SQL Server
def init_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-OJD0AB2\SQLEXPRESS;'
        'DATABASE=RecoMaster;'
        'Trusted_Connection=yes;'
    )
    return connection

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if email exists
def check_email_exists(email):
    conn = init_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    data = cursor.fetchone()
    conn.close()
    return data is not None

# Function to generate a random password
def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Function to update password in the database
def update_password(email, new_password):
    conn = init_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(new_password)
    cursor.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
    conn.commit()
    conn.close()

# Streamlit UI for Forgot Password
st.title("Forgot Password")

email = st.text_input("Enter your email address")

if st.button("Reset Password"):
    if email:
        if check_email_exists(email):
            # Generate a temporary password
            temp_password = generate_temp_password()
            update_password(email, temp_password)
            st.success("A new password has been generated.")
            st.write(f"New temporary password: {temp_password}")
        else:
            st.error("No account found with that email address.")
    else:
        st.error("Please enter your email address.")
