import streamlit as st
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to load credentials from the JSON file
def load_credentials():
    try:
        with open("credentials.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to send an email
def send_email(to_email, subject, body):
    # Email details
    from_email = "your_email@gmail.com"  # Replace with your email
    password = "xmrg tjmc ittq hlen"  # Replace with your email password

    # Setting up the MIME
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    # Adding the body to the email
    message.attach(MIMEText(body, 'plain'))

    # Sending the email using SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server
        server.starttls()
        server.login(from_email, password)
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Load existing credentials
credentials = load_credentials()

# Title of the page
st.title("Login")

# Input fields for login credentials
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Button to submit the login form
if st.button("Login"):
    if username in credentials and credentials[username]["password"] == password:
        st.success("Login successful!")
    else:
        st.error("Invalid username or password")

# Forgot Password section
# st.write("---")
# st.subheader("Forgot Password?")

# email_to_retrieve = st.text_input("Enter your email to retrieve your password")

# if st.button("Retrieve Password"):
#     found = False
#     for user, info in credentials.items():
#         if info["email"] == email_to_retrieve:
#             subject = "Your Login Credentials"
#             body = f"Your username is: {user}\nYour password is: {info['password']}"
#             if send_email(email_to_retrieve, subject, body):
#                 st.success("Credentials have been sent to your email.")
#             else:
#                 st.error("Failed to send email. Please try again later.")
#             found = True
#             break
#     if not found:
#         st.error("Email not found in the system.")