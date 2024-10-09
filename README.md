# Flask/Streamlit App with Google Cloud SQL and Google Cloud Storage Integration

This is a full-stack project that deploys a **Flask backend** with a **Streamlit frontend** using **Google Cloud SQL (PostgreSQL)** for the database and **Google Cloud Storage** for file uploads. It is designed to run in **Google Kubernetes Engine (GKE)**.

## Prerequisites

1. **Google Cloud Platform Account**: You need a GCP account with billing enabled.
2. **Google Cloud SDK**: Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) to interact with GCP services.
3. **Docker**: Make sure Docker is installed to build and push images.

## Steps to Set Up

### 1. Set Up Google Cloud Services

1. **Create a Google Cloud Project** if you don't already have one.
2. **Enable APIs**:
   - [Google Kubernetes Engine API](https://console.cloud.google.com/marketplace/product/google/container.googleapis.com)
   - [Cloud SQL Admin API](https://console.cloud.google.com/apis/library/sqladmin.googleapis.com)
   - [Cloud Storage API](https://console.cloud.google.com/apis/library/storage.googleapis.com)

### 2. Create a Google Cloud Service Account

1. Go to the **IAM & Admin** > **Service Accounts** in the Google Cloud Console.
2. **Create a new service account** and give it the following roles:
   - `Cloud SQL Client`
   - `Storage Admin`
3. **Create and download the JSON key** for the service account.
4. Save the JSON key file somewhere secure (but **do not upload it to GitHub**).
5. The downloaded JSON key will be used later when deploying to GKE.

### 3. Set Up Cloud SQL (PostgreSQL)

1. **Create a Cloud SQL instance** (PostgreSQL) in the Google Cloud Console.
2. **Configure the database** with the following information:
   - **Database Name**: `myappdb`
   - **User**: `myuser`
   - **Password**: `mypassword`

SQL to create Postgres database, and table which can be used to store data.

CREATE DATABASE myappdb;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE myappdb TO myuser;
CREATE TABLE data_table (
    id SERIAL PRIMARY KEY,
    value TEXT NOT NULL
);

3. **Enable public IP access** or use the **Cloud SQL Auth Proxy**.

### 4. Set Up Google Cloud Storage (GCS)

1. Create a new **GCS bucket** and note down the name of the bucket.
2. Make sure your **service account** has the appropriate permissions to upload files to this bucket.

### 5. Set Up Environment Variables

Create a `.env` file to store the configuration details for your database and GCS:

DB_HOST=<your-cloud-sql-public-ip> 
DB_NAME=myappdb DB_USER=myuser 
DB_PASSWORD=mypassword 
GCS_BUCKET_NAME=<your-gcs-bucket-name>
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json


This `.env` file is used to load environment variables into the Flask application.

### 6. Build and Push Docker Images

1. Build and tag the Docker images for both the frontend and backend:
  
   docker build -t gcr.io/<your-project-id>/backend-app:latest .
   docker build -t gcr.io/<your-project-id>/frontend-app:latest .

2. Push the images to Google Container Registry:

   docker push gcr.io/<your-project-id>/backend-app:latest
   docker push gcr.io/<your-project-id>/frontend-app:latest

Deploy to Google Kubernetes Engine (GKE)
  Create GKE clusters for the frontend and backend:
    gcloud container clusters create frontend-cluster --zone us-central1-a --machine-type e2-micro --num-nodes=1 --enable-autoscaling --min-nodes=1 --max-nodes=2
    gcloud container clusters create backend-cluster --zone us-central1-a --machine-type e2-micro --num-nodes=1 --enable-autoscaling --min-nodes=1 --max-nodes=2

   kubectl apply -f backend-deployment.yaml
   kubectl apply -f frontend-deployment.yaml

Why Use an .env File?
An .env file is used to store configuration variables in a secure and manageable way. By using an environment file, sensitive information (like database credentials and API keys) are not hardcoded into the application code, making it easier to change these configurations across different environments (e.g., local development, staging, production).

Conclusion
This project demonstrates how to:

Deploy a Flask and Streamlit app using Google Cloud SQL and Google Cloud Storage.
Containerize the app using Docker.
Deploy the app in Google Kubernetes Engine (GKE).
Integrate with Google Cloud services in a scalable, cloud-native architecture.
Feel free to clone this repo and follow the setup instructions to get this project running!

Now you can copy and paste this entire content directly into your **README.md** file without any issues! Let me know if you need more assistance.



