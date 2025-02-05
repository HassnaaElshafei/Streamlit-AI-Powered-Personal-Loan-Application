import os
import json
import sqlite3
import streamlit as st
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# Configure Gemini API
api_key = st.secrets["GOOGLE_API_KEY"]  # Ensure this is set in Streamlit Secrets
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

# Function to ensure database and tables exist
def create_database():
    """Creates the SQLite database and tables if they do not exist."""
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()

    # Ensure all required tables exist
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
            Employee_Name TEXT,
            Employer_Name TEXT,
            Hire_Date TEXT,
            Job_Title TEXT,
            Letter_Date TEXT,
            Monthly_Gross_Salary INTEGER,
            National_ID INTEGER,
            Currency TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utility_receipt (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Amount_Billed INTEGER,
            Bill_Issue_Date TEXT,
            Customer_Name TEXT,
            Service_Provider TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Ensure the database is created at app startup
create_database()

# Function to save extracted data
def save_to_database(extracted_info, document_type):
    """Saves extracted document information into the SQLite database."""
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()

    table_mapping = {
        "national_id_front": "national_id",
        "national_id_back": "national_id",
        "hr_letter": "hr_letter",
        "utility_receipt": "utility_receipt"
    }

    if document_type in table_mapping:
        table = table_mapping[document_type]

        columns = ', '.join(extracted_info.keys())
        placeholders = ', '.join(['?'] * len(extracted_info))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor.execute(sql, tuple(extracted_info.values()))
        conn.commit()

    conn.close()

# Functions to extract information from specific documents
def extract_front_side(image_path):
    """Extracts information from the front side of the National ID."""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])

    response = chat_session.send_message([
        "Extract full name, address, national ID, and date of birth from this National ID front side.",
        uploaded_file
    ])

    return response.text

def extract_back_side(image_path):
    """Extracts information from the back side of the National ID."""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])

    response = chat_session.send_message([
        "Extract issue date, gender, and expiry date from this National ID back side.",
        uploaded_file
    ])

    return response.text

def extract_HR_Letter(image_path):
    """Extracts information from the HR Letter."""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])

    response = chat_session.send_message([
        "Extract employee name, employer name, hire date, job title, letter date, salary, and national ID from this HR Letter.",
        uploaded_file
    ])

    return response.text

def extract_Utility_Receipt(image_path):
    """Extracts information from the Utility Receipt."""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])

    response = chat_session.send_message([
        "Extract amount billed, bill issue date, customer name, and service provider from this Utility Receipt.",
        uploaded_file
    ])

    return response.text
