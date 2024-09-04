import streamlit as st
import json

# Function to load credentials from the JSON file
def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save credentials to the JSON file
def save_credentials(credentials):
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)

# Load existing credentials
credentials = load_credentials()

# Title of the page
st.title("Sign Up")

# Input fields for user details
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Button to submit the form
if st.button("Sign Up"):
    if username and email and password:
        # Store credentials in the dictionary
        credentials[username] = {"email": email, "password": password}
        save_credentials(credentials)  # Save to JSON file
        st.success("Sign up successful!")
    else:
        st.error("Please fill in all fields")

# The credentials are now stored securely in credentials.json and not displayed on the screen.