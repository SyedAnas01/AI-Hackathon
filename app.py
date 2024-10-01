# app.py
import os
import requests
import streamlit as st
from streamlit_ace import st_ace  # Make sure this is installed

# Set the directory for saving submissions
SUBMISSIONS_DIR = "submissions"

# Create the submissions directory if it doesn't exist
if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)

# Title of the app
st.title("AI Hackathon Challenge with Duo Authentication")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ("Participant", "Judge"))

# Participant Page
if page == "Participant":
    st.header("Participant Page")
    
    # User ID input for verification
    user_id = st.text_input("Enter your user ID (email):")
    
    if st.button("Verify"):
        # Send request to backend for Duo verification
        response = requests.post('http://localhost:5000/verify', json={'user_id': user_id})
        if response.status_code == 200:
            sig_request = response.json().get("sig_request")
            # Display the Duo verification URL (simulated here)
            st.write("Please complete the Duo verification using the link below:")
            st.markdown(f"[Duo Verification]({sig_request})")  # Simulated verification link
        else:
            st.error("Verification failed. Please try again.")

    # Code editor for submissions
    st.subheader("Code Editor")
    code = st_ace(
        placeholder="Write your code here...",
        language="python",  # Change language as needed
        theme="monokai",
        height=300
    )

    # File uploader for submissions
    if st.button("Submit Code"):
        if code:
            # Save the submitted code to the submissions directory
            file_name = f"submission_{user_id}.py"  # Modify as needed
            file_path = os.path.join(SUBMISSIONS_DIR, file_name)
            with open(file_path, "w") as f:
                f.write(code)
            st.success(f"Submission received! Code saved as {file_name}.")
        else:
            st.error("Please enter your code before submitting.")
# Judge Page
else:
    st.header("Judge Page")
    
    # Authentication section for judges
    judge_password = st.text_input("Enter judge password to view submissions:", type="password")

    # Define your judge password (you can change this)
    VALID_JUDGE_PASSWORD = "your_secure_password"  # Replace with your own password

    if judge_password == VALID_JUDGE_PASSWORD:
        # List the files in the submissions directory
        st.subheader("Previous Submissions")
        if os.path.exists(SUBMISSIONS_DIR):
            submissions = os.listdir(SUBMISSIONS_DIR)
            if submissions:
                for file in submissions:
                    st.write(file)
                    # Displaying the content of each submission
                    with open(os.path.join(SUBMISSIONS_DIR, file), "r") as f:
                        st.code(f.read(), language='python')  # Adjust language based on file type
            else:
                st.write("No submissions yet.")
    else:
        if judge_password:
            st.error("Incorrect password. Please try again.")
