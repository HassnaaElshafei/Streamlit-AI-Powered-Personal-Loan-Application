import streamlit as st
import json
import tempfile
import os
from backend_functions import extract_document_info, save_to_database, detect_document_type

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Applicant Information"

if "extracted_info" not in st.session_state:
    st.session_state.extracted_info = None

# Sidebar for navigation using session state
def sidebar():
    logo_url = "https://raw.githubusercontent.com/HassnaaElshafei/Streamlit-AI-Powered-Personal-Loan-Application/main/bank_logo.png"
    st.sidebar.image(logo_url, use_container_width=True)
    st.sidebar.title("Navigation")

    if st.sidebar.button("Applicant Information"):
        st.session_state.page = "Applicant Information"
    if st.sidebar.button("Document Upload"):
        st.session_state.page = "Document Upload"
    if st.sidebar.button("Results"):
        st.session_state.page = "Results"

# Page 1: Applicant Information
def applicant_information():
    st.markdown("<h1><u>Applicant Information</u></h1>", unsafe_allow_html=True)

    st.markdown("### Applicant Details")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col2:
        national_id = st.text_input("National ID (14-digit)")
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])

    st.markdown("### Address")
    col1, col2 = st.columns(2)
    with col1:
        street = st.text_input("Street")
        city = st.text_input("City")
    with col2:
        district = st.text_input("District")
        governorate = st.text_input("Governorate")
    country = st.text_input("Country", value="Egypt")

    st.markdown("### Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email")
        home_phone = st.text_input("Home Phone (Optional)")
    with col2:
        mobile = st.text_input("Mobile Number")

    if st.button("Submit Application"):
        st.success("Application submitted successfully!")

# Page 2: Document Upload
def document_upload():
    st.markdown("<h1><u>Document Upload</u></h1>", unsafe_allow_html=True)
    st.markdown("Please upload PDF or JPG files only.")

    documents = {
        "HR Letter": "Upload HR Letter",
        "National ID": "Upload National ID (Both Sides in One File)",
        "Utility Receipt": "Upload Utility Receipt",
        "Bank Statement": "Upload Bank Statement",
        "Employer's Salary Transfer Commitment": "Upload Salary Transfer Commitment"
    }

    for doc, label in documents.items():
        uploaded_file = st.file_uploader(label, type=["pdf", "jpg", "jpeg", "png"], key=doc)

        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            document_type = detect_document_type(tmp_file_path)
            st.write(f"Detected Document Type: {document_type}")

            try:
                if document_type in ["national_id_front", "national_id_back"]:
                    extracted_front = extract_document_info(tmp_file_path, "national_id_front")
                    extracted_back = extract_document_info(tmp_file_path, "national_id_back")

                    extracted_info_dict = {
                        "Front Side Information": json.loads(extracted_front),
                        "Back Side Information": json.loads(extracted_back)
                    }
                else:
                    extracted_info = extract_document_info(tmp_file_path, document_type)
                    extracted_info_dict = json.loads(extracted_info)

                st.session_state.extracted_info = extracted_info_dict
                save_to_database(extracted_info_dict, document_type)
                st.success(f"Information extracted and saved for {document_type.replace('_', ' ').title()}!")

            except Exception as e:
                st.error(f"Error processing {document_type.replace('_', ' ').title()}: {str(e)}")

            os.unlink(tmp_file_path)

    # Display extracted info in a collapsible popup-style box
    if st.session_state.extracted_info:
        with st.expander("🔍 Extracted Information (Click to Expand/Close)"):
            st.json(st.session_state.extracted_info)
            if st.button("❌ Close Extracted Info"):
                st.session_state.extracted_info = None

    if st.button("Process Application"):
        st.success("Documents processed successfully!")

# Page 3: Results
def results():
    st.markdown("<h1><u>Results</u></h1>", unsafe_allow_html=True)
    st.info("Please process the application to view results.")

# Main app
def main():
    sidebar()

    if st.session_state.page == "Applicant Information":
        applicant_information()
    elif st.session_state.page == "Document Upload":
        document_upload()
    elif st.session_state.page == "Results":
        results()

if __name__ == "__main__":
    main()
