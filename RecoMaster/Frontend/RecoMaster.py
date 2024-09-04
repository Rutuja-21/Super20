import streamlit as st

# Set up the page configuration
st.set_page_config(
    page_title="RecoMaster",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Background image */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1627770246352-35d53657538f?q=80&w=1527&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-position: center;
        background-size: cover;
        height: 100vh; /* Ensure full viewport height */
        overflow: hidden; /* Hide scrollbar */
    }

    /* Header styling */
    .header {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        text-align: center;
        margin-bottom: 20px;
    }

    .header h1 {
        color: #FFD700;
        font-size: 4em;
        margin: 0;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
    }

    .header h2 {
        color: #FFFAFA;
        font-size: 1.5em;
        margin: 10px 0 0;
        font-family: 'Arial', sans-serif;
    }

    /* Centered button styling */
    .signup-btn-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: calc(32vh - 100px);
    }

    .signup-btn {
        background-color: #FF6347;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 1.4em;
        display: inline-block;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }

    .signup-btn:hover {
        background-color: #FF4500;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content
st.markdown(
    '<div class="header">'
    '<h1>RecoMaster</h1>'
    '<h2>Your Ultimate Food Guide</h2>'
    '</div>',
    unsafe_allow_html=True
)

st.sidebar.success("Select a recommendation app.")

url="http://localhost:8501/Signup"

# Signup button centered in the viewport
st.markdown(
    '<div class="signup-btn-container">'
    f'<a href="{url}" class="signup-btn">Join Us Now</a>'
    '</div>',
    unsafe_allow_html=True
)
