import os
import json
import sqlite3
import streamlit as st
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# Configure Gemini API
api_key = st.secrets["GOOGLE_API_KEY"]  # Ensure this is set correctly in Streamlit Secrets
genai.configure(api_key=api_key)

# Function to upload files to Gemini
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini API."""
    file = genai.upload_file(path, mime_type=mime_type)
    return file

# Function to detect document type
def detect_document_type(image_path):
    """Detects the type of document in the given image."""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])

    prompt = """
    Identify the document type. Choose from:
    - national_id_front
    - national_id_back
    - hr_letter
    - utility_receipt
    """

    response = chat_session.send_message([prompt, uploaded_file])
    return response.text.strip().lower()

# Function to extract document information
def extract_document_info(image_path, document_type):
    """Calls the appropriate extraction function based on document type."""
    if document_type == "national_id_front":
        return extract_front_side(image_path)
    elif document_type == "national_id_back":
        return extract_back_side(image_path)
    elif document_type == "hr_letter":
        return extract_HR_Letter(image_path)
    elif document_type == "utility_receipt":
        return extract_Utility_Receipt(image_path)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")

# SQLite Database Setup
def create_database():
    """Creates the SQLite database if it does not exist."""
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS national_id (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Document_Type TEXT,
            Full_Name TEXT,
            Address TEXT,
            National_ID INTEGER,
            Date_of_Birth TEXT,
            Issue_Date TEXT,
            Gender TEXT,
            Expiry_Date TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hr_letter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Employee_Name T
