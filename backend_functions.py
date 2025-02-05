import os
import json
import sqlite3
import streamlit as st
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# Configure Gemini API
api_key = st.secrets["GOOGLE_API_KEY"]  # Replace with a secure method for production
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

# Functions to extract information from specific documents
def extract_front_side(image_path):
    """Extracts information from the front side of the National ID."""
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type=content.Type.OBJECT,
            required=["Document_Type", "Full_Name", "Address", "National_ID", "Date of Birth"],
            properties={
                "Document_Type": content.Schema(type=content.Type.STRING),
                "Full_Name": content.Schema(type=content.Type.STRING),
                "Address": content.Schema(type=content.Type.STRING),
                "National_ID": content.Schema(type=content.Type.INTEGER),
                "Date of Birth": content.Schema(type=content.Type.STRING),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(["Extract front side National ID details.", uploaded_file])

    return response.text

def extract_back_side(image_path):
    """Extracts information from the back side of the National ID."""
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type=content.Type.OBJECT,
            required=["Document_Type", "Issue_Date", "Gender", "Expiry_Date"],
            properties={
                "Document_Type": content.Schema(type=content.Type.STRING),
                "Issue_Date": content.Schema(type=content.Type.STRING),
                "Gender": content.Schema(type=content.Type.STRING),
                "Expiry_Date": content.Schema(type=content.Type.STRING),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(["Extract back side National ID details.", uploaded_file])

    return response.text

def extract_HR_Letter(image_path):
    """Extracts information from the HR Letter."""
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type=content.Type.OBJECT,
            required=["Document_Type", "Employee_Name", "Employer_Name", "Hire_Date", "Job_Title", "Letter_Date", "Monthly_Gross_Salary", "National_ID", "Currency"],
            properties={
                "Document_Type": content.Schema(type=content.Type.STRING),
                "Employee_Name": content.Schema(type=content.Type.STRING),
                "Employer_Name": content.Schema(type=content.Type.STRING),
                "Hire_Date": content.Schema(type=content.Type.STRING),
                "Job_Title": content.Schema(type=content.Type.STRING),
                "Letter_Date": content.Schema(type=content.Type.STRING),
                "Monthly_Gross_Salary": content.Schema(type=content.Type.INTEGER),
                "National_ID": content.Schema(type=content.Type.INTEGER),
                "Currency": content.Schema(type=content.Type.STRING),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(["Extract HR Letter details.", uploaded_file])

    return response.text

def extract_Utility_Receipt(image_path):
    """Extracts information from the Utility Receipt."""
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type=content.Type.OBJECT,
            required=["Amount_Billed", "Bill_Issue_Date", "Customer_Name", "Document_Type", "Service_Provider"],
            properties={
                "Amount_Billed": content.Schema(type=content.Type.INTEGER),
                "Bill_Issue_Date": content.Schema(type=content.Type.STRING),
                "Customer_Name": content.Schema(type=content.Type.STRING),
                "Document_Type": content.Schema(type=content.Type.STRING),
                "Service_Provider": content.Schema(type=content.Type.STRING),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp", generation_config=generation_config)
    uploaded_file = upload_to_gemini(image_path, mime_type="image/png")
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(["Extract Utility Receipt details.", uploaded_file])

    return response.text

def save_to_database(extracted_info, document_type):
    """Creates SQLite database and saves extracted data."""
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()

    tables = {
        "national_id_front": '''
            CREATE TABLE IF NOT EXISTS national_id_front (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Full_Name TEXT,
                Address TEXT,
                National_ID INTEGER,
                Date_of_Birth TEXT
            )
        ''',
        "hr_letter": '''
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
        '''
    }

    cursor.execute(tables[document_type])
    cursor.execute(f"INSERT INTO {document_type} VALUES ({','.join(['?']*len(extracted_info))})", tuple(extracted_info.values()))
    conn.commit()
    conn.close()
