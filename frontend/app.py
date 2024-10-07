import streamlit as st
import requests

# Backend URL to communicate with the backend
BACKEND_URL = "http://backend-service:5000"
  # Use backend container URL # Current:
#BACKEND_URL = "http://backend-container:5000"


# Streamlit application layout
st.set_page_config(page_title="App Dashboard", layout="centered")

# Title of the application
st.title("App Dashboard")

# Section to submit data
st.header("Submit Data to Cloud SQL")
input_value = st.text_input("Enter a value to store in the database:")
if st.button("Submit"):
    response = requests.post(f"{BACKEND_URL}/submitdata", json={"value": input_value})
    if response.status_code == 200:
        st.success("Data submitted successfully!")
    else:
        st.error("Failed to submit data!")

# Section to fetch data from Cloud SQL
st.header("Fetch Data from Cloud SQL")
if st.button("Fetch Data"):
    response = requests.get(f"{BACKEND_URL}/fetchdata")
    if response.status_code == 200:
        data = response.json()
        st.write("Fetched Data:", data)
    else:
        st.error("Failed to fetch data!")

# Section to upload files to GCS
st.header("Upload File to Google Cloud Storage")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if st.button("Upload"):
        # Read file content and pass file name
        files = {
            'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
        }
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
        if response.status_code == 200:  # Correct syntax
            st.success("File uploaded successfully!")
        else:
            st.error("Failed to upload file!")

