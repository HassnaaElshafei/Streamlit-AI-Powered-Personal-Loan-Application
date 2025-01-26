import streamlit as st

# Sidebar with logo and navigation in boxes
def sidebar():
    logo_url = "https://raw.githubusercontent.com/HassnaaElshafei/Streamlit-AI-Powered-Personal-Loan-Application/main/bank_logo.png"
    st.sidebar.image(logo_url, use_container_width=True)
    st.sidebar.title("Navigation")
    
    # Create boxes for navigation
    applicant_btn = st.sidebar.button("Applicant Information")
    document_btn = st.sidebar.button("Document Upload")
    results_btn = st.sidebar.button("Results")
    
    # Return the selected page
    if applicant_btn:
        return "Applicant Information"
    elif document_btn:
        return "Document Upload"
    elif results_btn:
        return "Results"
    else:
        return "Applicant Information"  # Default page

# Page 1: Applicant Information
def applicant_information():
    st.markdown("<h1 style='text-align: left; font-size: 32px;'><u>Applicant Information</u></h1>", unsafe_allow_html=True)
    
    # Applicant Details Section
    st.markdown("### Applicant Details")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col2:
        national_id = st.text_input("National ID (14-digit)")
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])

    # Address Section
    st.markdown("### Address")
    col1, col2 = st.columns(2)
    with col1:
        street = st.text_input("Street")
        city = st.text_input("City")
    with col2:
        district = st.text_input("District")
        governorate = st.text_input("Governorate")
    country = st.text_input("Country", value="Egypt")

    # Contact Information Section
    st.markdown("### Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email")
        home_phone = st.text_input("Home Phone Number (Optional)")
    with col2:
        mobile = st.text_input("Mobile Number")

    # Employment & Financial Information Section
    st.markdown("### Employment & Financial Information")
    col1, col2 = st.columns(2)
    with col1:
        education = st.text_input("Education")
        occupation = st.text_input("Occupation")
        employer_name = st.text_input("Employer Name")
    with col2:
        monthly_income = st.number_input("Monthly Income", min_value=0)
        other_income = st.number_input("Other Income (Optional)", min_value=0)

    # Loan Details Section
    st.markdown("### Loan Details")
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input("Loan Amount", min_value=0)
        loan_term = st.number_input("Loan Term (Months)", min_value=1)
    with col2:
        loan_purpose = st.text_input("Loan Purpose")
        payment_method = st.selectbox("Payment Method", ["Bank Transfer", "Cash", "Check"])

    if st.button("Submit Application"):
        st.success("Application submitted successfully!")

# Page 2: Document Upload
def document_upload():
    st.markdown("<h1 style='text-align: left; font-size: 32px;'><u>Document Upload</u></h1>", unsafe_allow_html=True)
    st.markdown("Please upload PDF or JPG files only.")
    
    documents = {
        "HR Letter": "Upload HR Letter",
        "National ID": "Upload National ID",
        "Utility Receipt": "Upload Utility Receipt",
        "Bank Statement": "Upload Bank Statement",
        "Employer's Salary Transfer Commitment": "Upload Salary Transfer Commitment",
        "Employer's End-of-Service Benefit Commitment": "Upload End-of-Service Commitment"
    }
    for doc, label in documents.items():
        st.file_uploader(label, type=["pdf", "jpg", "jpeg", "png"])

    if st.button("Process Application"):
        st.success("Documents processed successfully!")

# Page 3: Results
def results():
    st.markdown("<h1 style='text-align: left; font-size: 32px;'><u>Results</u></h1>", unsafe_allow_html=True)
    st.info("Please process the application to view results.")

# Main app
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
