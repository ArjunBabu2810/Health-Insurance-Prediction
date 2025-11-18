import streamlit as st
import pandas as pd
import requests 
import json # Used for formatting the JSON payload display

# --- Configuration ---
# NOTE: Ensure your Flask API is running on http://localhost:5000/
FLASK_API_URL = "http://localhost:5000/predict" 

# --- Frontend Helper Functions (Used for Review Display Only) ---

def get_bmi_category(bmi):
    """Categorizes the BMI value (Used for local review display only)."""
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25.0:
        return 'Normal'
    elif 25.0 <= bmi < 30.0:
        return 'Overweight'
    else:
        return 'Obesity'

def get_medical_history_category(diabetes_value, systolic_pressure_value, diastolic_pressure_value, thyroid_status, heart_disease_status):
    """Categorizes raw health inputs into a combined 'Medical History' string (Used for local review display only)."""
    DIABETES_THRESHOLD = 126.0
    SBP_THRESHOLD = 140
    DBP_THRESHOLD = 90
    
    diseases = []
    
    if diabetes_value >= DIABETES_THRESHOLD:
        diseases.append('Diabetes')
    
    if (systolic_pressure_value >= SBP_THRESHOLD) or (diastolic_pressure_value >= DBP_THRESHOLD):
        diseases.append('High blood pressure')
    
    if thyroid_status == 'Yes':
        diseases.append('Thyroid')
        
    if heart_disease_status == 'Yes':
        diseases.append('Heart disease')
    
    if not diseases:
        return 'No Disease'

    return ' & '.join(sorted(diseases))


def main():
    """
    Main function to create the Streamlit frontend page for detailed insurance data entry 
    and make an API call to the Flask backend for prediction.
    """
    st.set_page_config(page_title="Insurance Premium Predictor", layout="wide")
    st.title("Insurance Premium Prediction Data Entry 📝")
    st.markdown("Enter the client details and click 'Submit' to get the predicted annual premium.")

    # Dictionary to store all collected raw data
    data = {}

    col1, col2, col3 = st.columns([1, 1, 1])

    # --- INPUT COLLECTION ---
    with col1:
        st.header("👤 Personal Details")
        # KEY CHANGE 1: 'age' matches 'Age'
        data['age'] = st.number_input("Age (Years)", min_value=18, max_value=100, value=35, step=1)
        # KEY CHANGE 2: 'gender' matches 'Gender'
        data['gender'] = st.radio("Gender", options=["Male", "Female"], index=0, horizontal=True)
        # KEY CHANGE 3: 'marital_status' matches 'Marital_status'
        data['marital_status'] = st.selectbox("Marital Status", options=["Married", "Unmarried"], index=0)
        # KEY CHANGE 4: 'number_of_dependants' matches 'Number Of Dependants'
        data['number_of_dependants'] = st.select_slider("Number of Dependants", options=list(range(0, 6)), value=1)
        
    with col2:
        st.header("🩺 Health & Lifestyle")
        # This key remains 'raw_bmi_value' as it is a raw input calculated client-side/used for helpers
        data['raw_bmi_value'] = st.number_input("BMI Value ($kg/m^2$)", min_value=10.0, max_value=60.0, value=25.0, step=0.1, format="%.1f")
        # KEY CHANGE 5: 'smoking_status' matches 'Smoking_Status'
        data['smoking_status'] = st.radio("Smoking Status", options=["Non-Smoker", "Regular", "Occasional"], index=0, horizontal=False)
        
        st.subheader("Specific Disease Parameters")
        # These raw keys remain as the backend uses them to calculate the 'Medical History' string
        data['diabetes_value'] = st.number_input("Diabetes/Sugar Value (Fasting Glucose mg/dL)", min_value=0.0, max_value=500.0, value=95.0, step=1.0)
        
        bp_col1, bp_col2 = st.columns(2)
        with bp_col1:
            data['systolic_pressure_value'] = st.number_input("Systolic BP (Top Number)", min_value=50, max_value=250, value=120, step=1)
        with bp_col2:
            data['diastolic_pressure_value'] = st.number_input("Diastolic BP (Bottom Number)", min_value=30, max_value=150, value=80, step=1)
        
        data['thyroid_status'] = st.radio("Thyroid Disease Detected?", options=["No", "Yes"], index=0, horizontal=True)
        data['heart_disease_status'] = st.radio("Heart Disease Detected?", options=["No", "Yes"], index=0, horizontal=True)

    with col3:
        st.header("💵 Financial & Plan")
        # KEY CHANGE 6: 'region' matches 'Region'
        data['region'] = st.selectbox("Region of Residence", options=["Northwest", "Southeast", "Northeast", "Southwest"], index=0)
        # KEY CHANGE 7: 'employment_status' matches 'Employment_Status'
        data['employment_status'] = st.selectbox("Employment Status", options=["Salaried", "Self-Employed", "Freelancer"], index=0)
        # KEY CHANGE 8: 'income_lakhs' matches 'Income_Lakhs'
        data['income_lakhs'] = st.number_input("Annual Income ($$Lakhs$$)", min_value=0.0, max_value=200.0, value=15.0, step=0.5, format="%.2f")
        
        st.subheader("Plan Details")
        # KEY CHANGE 9: 'insurance_plan' matches 'Insurance_Plan'
        data['insurance_plan'] = st.selectbox("Insurance Plan Type", options=["Bronze", "Silver", "Gold"], index=1)
        
    st.markdown("---")

    # --- Submission and API Call ---
    
    if st.button("Submit All Data for Analysis", type="primary"):
        st.session_state['show_result'] = False
        st.session_state['error_message'] = None
        
        with st.spinner('Sending data to API and calculating premium...'):
            try:
                # Send the raw collected data dictionary to the Flask API
                response = requests.post(FLASK_API_URL, json=data)
                response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
                
                prediction_result = response.json()
                predicted_premium = prediction_result.get('predicted_premium')
        
                if predicted_premium is not None:
                    st.session_state['predicted_premium'] = predicted_premium
                    st.session_state['show_result'] = True
                    # Store processed features for review display
                    st.session_state['processed_data'] = {
                        # The processed data here uses simplified keys for frontend readability
                        'age': data['age'],
                        'gender': data['gender'],
                        'region': data['region'],
                        'marital_status': data['marital_status'],
                        'number_of_dependants': data['number_of_dependants'],
                        'bmi_category': get_bmi_category(data['raw_bmi_value']),
                        'smoking_status': data['smoking_status'],
                        'employment_status': data['employment_status'],
                        'income_lakhs': data['income_lakhs'],
                        'medical_history': get_medical_history_category(
                            data['diabetes_value'], 
                            data['systolic_pressure_value'], 
                            data['diastolic_pressure_value'], 
                            data['thyroid_status'], 
                            data['heart_disease_status']
                        ),
                        'insurance_plan': data['insurance_plan'],
                    }
                else:
                    st.session_state['error_message'] = "API call succeeded, but the 'predicted_premium' key was missing from the response."
            
            except requests.exceptions.ConnectionError:
                st.session_state['error_message'] = f"Connection Error: Could not connect to the Flask API at {FLASK_API_URL}. Please ensure the backend server is running."
            except requests.exceptions.RequestException as e:
                # If the API returns a 400 (Bad Request) or 500 (Internal Server Error)
                try:
                    error_details = response.json().get('error', str(e))
                except (json.JSONDecodeError, UnboundLocalError):
                    error_details = str(e)
                st.session_state['error_message'] = f"API Request Failed: {response.status_code} - {error_details}"
            
        st.rerun() # Rerun to display results outside the spinner block

    # --- Result Display Area (Renders on rerun after submission) ---
    if 'show_result' in st.session_state and st.session_state['show_result']:
        st.success("Data Submitted! See the Predicted Annual Premium below. ✅")
        st.markdown("---")
        
        st.header("🎯 Predicted Annual Premium")
        st.metric(
            label="Estimated Annual Premium (₹)", 
            value=f"₹{st.session_state['predicted_premium']:,.2f}",
            help="This prediction was calculated by the Flask backend API."
        )
        
        # st.subheader("Review Processed Categorical Data")
        # st.json(st.session_state['processed_data'])

    elif 'error_message' in st.session_state and st.session_state['error_message']:
        st.error(st.session_state['error_message'])

if __name__ == "__main__":
    main()