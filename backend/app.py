from flask import Flask, request, jsonify
import psycopg2
from google.cloud import storage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Cloud SQL Configuration
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT', '5432')

# GCS Configuration
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# PostgreSQL Connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

# API to submit data to the Cloud SQL database
@app.route('/submitdata', methods=['POST'])
def submit_data():
    data = request.json.get('value')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data_table (value) VALUES (%s)", (data,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Data inserted successfully"})

# API to fetch data from the Cloud SQL database
@app.route('/fetchdata', methods=['GET'])
def fetch_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM data_table")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

# API to upload a file to Google Cloud Storage
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Google Cloud Storage (GCS) upload
        storage_client = storage.Client.from_service_account_json(GCS_CREDENTIALS)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        
        return jsonify({"message": "File uploaded successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

