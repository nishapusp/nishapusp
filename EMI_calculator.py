import streamlit as st

# Function to calculate EMI
def calculate_emi(principal, annual_rate, tenure_years):
    monthly_rate = annual_rate / (12 * 100)  # Convert annual rate to monthly and in decimal
    tenure_months = tenure_years * 12
    if monthly_rate == 0:  # Prevent division by zero in edge cases
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    return emi

# Function to determine ROI based on loan type, credit score, and category
def determine_roi(loan_type, credit_score, customer_category):
    # Adjusted ROI data to ensure rates for females are equal to or less than males
    roi_data = {
        "Home Loan": {
            "Salaried": {
                "Male": {800: 8.35, 750: 8.50, 700: 9.15, 650: 9.45, 600: 10.25},
                "Female": {800: 8.30, 750: 8.45, 700: 9.10, 650: 9.40, 600: 10.20}
            },
            "Non-Salaried": {
                "Male": {800: 8.35, 750: 8.50, 700: 9.25, 650: 9.50, 600: 10.75},
                "Female": {800: 8.30, 750: 8.45, 700: 9.20, 650: 9.45, 600: 10.70}
            },
        },
        "Vehicle Loan": {
            "Salaried": {
                "Male": {800: 8.80, 750: 9.00, 700: 9.45, 650: 10.25, 600: 10.70},
                "Female": {800: 8.75, 750: 8.95, 700: 9.40, 650: 10.20, 600: 10.65}
            },
            "Non-Salaried": {
                "Male": {800: 8.85, 750: 9.05, 700: 9.50, 650: 10.30, 600: 10.75},
                "Female": {800: 8.80, 750: 9.00, 700: 9.45, 650: 10.25, 600: 10.70}
            },
        }
    }

    # Get the applicable ROI or return a default value if not found
    return roi_data.get(loan_type, {}).get(customer_category["type"], {}).get(customer_category["gender"], {}).get(credit_score, 9.25)

# Streamlit UI
st.title("EMI and ROI Calculator")

# User inputs
loan_type = st.selectbox("Select Loan Type", ["Home Loan", "Vehicle Loan"])
loan_amount = st.number_input("Loan Amount", min_value=1000, step=1000)
tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, max_value=30, step=1)
credit_score = st.number_input("Credit Score", min_value=300, max_value=900, step=50)
customer_type = st.selectbox("Customer Category", ["Salaried", "Non-Salaried"])
gender = st.selectbox("Gender", ["Male", "Female"])

# Combine category information
customer_category = {"type": customer_type, "gender": gender}

# Calculate ROI and EMI
roi = determine_roi(loan_type, credit_score, customer_category)
emi = calculate_emi(loan_amount, roi, tenure_years)

# Debugging: Display intermediate values
st.write(f"Debug Info: Principal={loan_amount}, Rate={roi}, Tenure={tenure_years}")

# Display results
st.write(f"**Applicable ROI:** {roi:.2f}%")
st.write(f"**EMI:** ₹{emi:.2f}")
