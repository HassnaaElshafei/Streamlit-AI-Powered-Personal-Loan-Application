import streamlit as st
import json
import tempfile
import os
from backend_functions import extract_document_info, save_to_database, detect_document_type

# Sidebar for navigation
def sidebar():
    logo_url = "https://raw.githubusercontent.com/HassnaaElshafei/Streamlit-AI-Powered-Personal-Loan-Application/main/bank_logo.png"
    st.sidebar.image(logo_url, use_container_width=True)
    st.sidebar.title("Navigation")

    applicant_btn = st.sidebar.button("Applicant Information")
    document_btn = st.sidebar.button("Document Upload")
    results_btn = st.sidebar.button("Results")

    if applicant_btn:
        return "Applicant Information"
    elif document_btn:
        return "Document Upload"
    elif results_btn:
        return "Results"
    return "Applicant Information"

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

    if "extracted_info" not in st.session_state:
        st.session_state.extracted_info = None

    documents = {
        "HR Letter": "Upload HR Letter",
        "National ID": "Upload National ID (Both Sides in One File)",
        "Utility Receipt": "Upload Utility Receipt"
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
                if document_type == "national_id_front" or document_type == "national_id_back":
                    extracted_front = extract_document_info(tmp_file_path, "national_id_front")
                    extracted_back = extract_document_info(tmp_file_path, "national_id_back")

                    extracted_info_front = json.loads(extracted_front)
                    extracted_info_back = json.loads(extracted_back)

                    extracted_info_dict = {
                        "Front Side Information": extracted_info_front,
                        "Back Side Information": extracted_info_back
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

    if st.session_state.extracted_info:
        with st.expander("🔍 Extracted Information (Click to Expand/Close)"):
            st.json(st.session_state.extracted_info)
            if st.button("❌ Close Extracted Info"):
                st.session_state.extracted_info = None

# Page 3: Results
def results():
    st.markdown("<h1><u>Results</u></h1>", unsafe_allow_html=True)
    st.info("Please process the application to view results.")

def main():
    page = sidebar()

    if page == "Applicant Information":
        applicant_information()
    elif page == "Document Upload":
        document_upload()
    elif page == "Results":
        results()

if __name__ == "__main__":
    main()
