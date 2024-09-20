import streamlit as st

# Function to handle logout
def logout():
    if 'logged_in' in st.session_state:
        del st.session_state['logged_in']
    st.session_state.logged_in = False
    st.success("You have been logged out.")
    st.write("You have been successfully logged out.")
    st.write("Click [here](../Login) to log in again.")

# Check if user is logged in
if 'logged_in' in st.session_state and st.session_state.logged_in:
    st.title("Logout")
    
    if st.button("Log Out"):
        logout()
else:
    st.write("You are not logged in.")
    st.write("Please [log in](../Login) to access this page.")
