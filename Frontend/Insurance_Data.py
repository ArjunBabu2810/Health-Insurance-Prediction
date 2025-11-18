# import streamlit as st
# import pandas as pd

# def get_bmi_category(bmi):
#     """
#     Categorizes the BMI value into one of the standard categories.
#     Matches the required unique values: 'Underweight', 'Normal', 'Overweight', 'Obesity'.
#     """
#     if bmi < 18.5:
#         return 'Underweight'
#     elif 18.5 <= bmi < 25.0:
#         # Note: The user provided 'Normal' (25)
#         return 'Normal'
#     elif 25.0 <= bmi < 30.0:
#         # Note: The user provided 'Overweight' (30) and 'Obesity'
#         return 'Overweight'
#     else:
#         return 'Obesity'

# def get_medical_history_category(diabetes_value, systolic_pressure_value, diastolic_pressure_value, thyroid_status, heart_disease_status):
#     """
#     Categorizes the raw numerical inputs and binary statuses into the required 
#     single 'Medical History' categorical string (e.g., 'Diabetes & Thyroid').
    
#     NOTE: Thresholds are simplified for this example application.
#     """
#     # Simplified thresholds for categorization:
#     DIABETES_THRESHOLD = 126.0  # Assumes Fasting Plasma Glucose (FPG) >= 126 mg/dL for 'Diabetes'
#     SBP_THRESHOLD = 140         # Systolic BP >= 140 mmHg
#     DBP_THRESHOLD = 90          # Diastolic BP >= 90 mmHg
    
#     # 1. Determine which diseases are present based on input/thresholds
#     diseases = []
    
#     if diabetes_value >= DIABETES_THRESHOLD:
#         diseases.append('Diabetes')
    
#     # Check for High Blood Pressure based on EITHER Systolic OR Diastolic thresholds
#     if (systolic_pressure_value >= SBP_THRESHOLD) or (diastolic_pressure_value >= DBP_THRESHOLD):
#         diseases.append('High blood pressure')
    
#     if thyroid_status == 'Yes':
#         diseases.append('Thyroid')
        
#     if heart_disease_status == 'Yes':
#         diseases.append('Heart disease')
    
#     # 2. Combine and format the output
#     if not diseases:
#         return 'No Disease'

#     # Sort the diseases list alphabetically for consistent output string, 
#     # then join with ' & '. This flexible combination matches the user's example 
#     # (e.g., 'Thyroid & Heart disease').
#     return ' & '.join(sorted(diseases))


# def main():
#     """
#     Main function to create the Streamlit frontend page for detailed insurance data entry.
#     """
#     st.set_page_config(page_title="Insurance Data Input", layout="wide")
#     st.title("Comprehensive Insurance Data Collector 📋")
#     st.markdown("Please enter the details for the policy holder below.")

#     # Dictionary to store all collected data
#     data = {}

#     # Use columns and containers for a cleaner, organized layout
#     col1, col2, col3 = st.columns([1, 1, 1])

#     # --- Column 1: Personal & Demographics ---
#     with col1:
#         st.header("👤 Personal Details")
        
#         # 1. age (Changed to manual number input as requested)
#         data['age'] = st.number_input(
#             "Age (Years)",
#             min_value=18,
#             max_value=100,
#             value=35,
#             step=1,
#             help="The primary beneficiary's age. Must be between 18 and 100."
#         )

#         # 2. gender (Updated options: 'Male', 'Female')
#         data['gender'] = st.radio(
#             "Gender",
#             options=["Male", "Female"],
#             index=0,
#             horizontal=True
#         )

#         # 4. marital_status (Updated options: 'Married', 'Unmarried')
#         data['marital_status'] = st.selectbox(
#             "Marital Status",
#             options=["Married", "Unmarried"],
#             index=0
#         )

#         # 5. number_of_dependants (Using a slider to cover the range 0-5)
#         data['number_of_dependants'] = st.select_slider(
#             "Number of Dependants",
#             options=list(range(0, 6)), # Covering the max value of 5
#             value=1
#         )
        
#     # --- Column 2: Health & Lifestyle ---
#     with col2:
#         st.header("🩺 Health & Lifestyle")

#         # RAW BMI Input (Inputted value to be converted to category on submission)
#         # 6. bmi_value 
#         bmi_value = st.number_input(
#             "BMI Value (Body Mass Index - $kg/m^2$)",
#             min_value=10.0,
#             max_value=60.0,
#             value=25.0,
#             step=0.1,
#             format="%.1f",
#             help="Enter the raw BMI value. This will be automatically categorized upon submission."
#         )

#         # 7. smoking_status (Updated options)
#         data['smoking_status'] = st.radio(
#             "Smoking Status",
#             options=["Non-Smoker", "Regular", "Occasional"],
#             index=0,
#             horizontal=False
#         )
        
#         # 10. Medical History (Redesigned for specific value inputs)
#         st.subheader("Specific Disease Parameters")

#         # Value input for Sugar/Diabetes
#         data['diabetes_value'] = st.number_input(
#             "Diabetes/Sugar Value (Fasting Glucose in mg/dL)",
#             min_value=0.0,
#             max_value=500.0,
#             value=95.0,
#             step=1.0,
#             help="Value >= 126 is categorized as 'Diabetes'."
#         )

#         # Blood Pressure Inputs (Split into two columns as requested)
#         bp_col1, bp_col2 = st.columns(2)
#         with bp_col1:
#             systolic_pressure_value = st.number_input(
#                 "Systolic BP (Top Number)",
#                 min_value=50,
#                 max_value=250,
#                 value=120,
#                 step=1,
#                 help="If >= 140, is a factor in High blood pressure categorization."
#             )
#         with bp_col2:
#             diastolic_pressure_value = st.number_input(
#                 "Diastolic BP (Bottom Number)",
#                 min_value=30,
#                 max_value=150,
#                 value=80,
#                 step=1,
#                 help="If >= 90, is a factor in High blood pressure categorization."
#             )
#         # Store raw BP values in data dictionary
#         data['systolic_pressure_value'] = systolic_pressure_value
#         data['diastolic_pressure_value'] = diastolic_pressure_value

#         # Yes/No for Thyroid
#         data['thyroid_status'] = st.radio(
#             "Thyroid Disease Detected?",
#             options=["No", "Yes"],
#             index=0,
#             horizontal=True
#         )
#         # Yes/No for Heart Disease
#         data['heart_disease_status'] = st.radio(
#             "Heart Disease Detected?",
#             options=["No", "Yes"],
#             index=0,
#             horizontal=True
#         )

#     # --- Column 3: Location, Financials, & Plan ---
#     with col3:
#         st.header("💵 Financial & Location")
        
#         # 3. region (Updated options order)
#         data['region'] = st.selectbox(
#             "Region of Residence",
#             options=["Northwest", "Southeast", "Northeast", "Southwest"],
#             index=0
#         )

#         # 8. employment_status (Updated options)
#         data['employment_status'] = st.selectbox(
#             "Employment Status",
#             options=["Salaried", "Self-Employed", "Freelancer"],
#             index=0
#         )
        
#         # REINSTATED: Income (Lakhs)
#         data['income_lakhs'] = st.number_input(
#             "Annual Income ($$Lakhs$$)",
#             min_value=0.0,
#             max_value=200.0,
#             value=15.0,
#             step=0.5,
#             format="%.2f",
#             help="Annual household income in lakhs (e.g., 15.00 for ₹15,00,000)."
#         )

#         st.subheader("Plan Details")

#         # 11. insurance_plan (Updated options)
#         data['insurance_plan'] = st.selectbox(
#             "Insurance Plan Type",
#             options=["Bronze", "Silver", "Gold"],
#             index=1
#         )
        
#         # NOTE: Annual Premium Amount (The prediction target) is now excluded from inputs.

#     st.markdown("---")

#     # --- Submission and Review ---
    
#     if st.button("Submit All Data for Analysis", type="primary"):
        
#         # --- Processing Step 1: Categorize BMI ---
#         bmi_category = get_bmi_category(bmi_value)
#         data['raw_bmi_value'] = bmi_value
#         data['bmi_category'] = bmi_category
        
#         # --- Processing Step 2: Categorize Medical History ---
#         medical_history = get_medical_history_category(
#             data['diabetes_value'], 
#             data['systolic_pressure_value'], 
#             data['diastolic_pressure_value'], 
#             data['thyroid_status'], 
#             data['heart_disease_status']
#         )
#         data['medical_history'] = medical_history # New derived column

#         # ----------------------------------------------------
#         # NEW: 3. Simulate Prediction and Display Result
#         # ----------------------------------------------------
        
#         # Dummy Prediction Logic (Replace with actual model prediction function in a real app)
#         base_premium = 15000 
#         age_factor = data['age'] * 150
#         bmi_factor = data['raw_bmi_value'] * 200
        
#         # Example factor based on smoking status (Smokers pay more)
#         smoking_multiplier = 1.0
#         if data['smoking_status'] == 'Regular':
#              smoking_multiplier = 2.5
#         elif data['smoking_status'] == 'Occasional':
#              smoking_multiplier = 1.5

#         # Example factor based on medical history count
#         medical_count = len(data['medical_history'].split(' & ')) if data['medical_history'] != 'No Disease' else 0
#         medical_factor = medical_count * 5000
        
#         # Simple Additive/Multiplicative Model
#         predicted_premium_base = base_premium + age_factor + bmi_factor + medical_factor
#         predicted_premium = int(predicted_premium_base * smoking_multiplier)
        
#         # ----------------------------------------------------
#         # DISPLAY RESULT
#         # ----------------------------------------------------
#         st.success("Data Submitted! See the Predicted Annual Premium below. 👇")
#         st.markdown("---")
#         st.header("🎯 Predicted Annual Premium")
#         st.metric(
#             label="Estimated Annual Premium (₹)", 
#             value=f"₹{predicted_premium:,}",
#             help="This is a simulated prediction result based on the entered data. In a real application, a machine learning model would calculate this value."
#         )
#         st.markdown("---")

        
#         # ----------------------------------------------------
#         # REVIEW DATA (FOR MODEL INPUT)
#         # ----------------------------------------------------
#         st.subheader("Review Collected Data (JSON Format)")
        
#         # Final JSON payload containing only the features needed for the model
#         final_data_json = {
#             'age': data['age'],
#             'gender': data['gender'],
#             'region': data['region'],
#             'marital_status': data['marital_status'],
#             'number_of_dependants': data['number_of_dependants'],
#             'bmi_category': data['bmi_category'], 
#             'smoking_status': data['smoking_status'],
#             'employment_status': data['employment_status'],
#             'income_lakhs': data['income_lakhs'],
#             'medical_history': data['medical_history'], 
#             'insurance_plan': data['insurance_plan'],
#             # The predicted value would typically be returned by an API call using this JSON payload
#         }
        
#         st.json(final_data_json)
        
#         st.subheader("Data Table Preview (All Inputs)")
        
#         # Using a list of tuples to define the order and labels for the review table
#         review_data = [
#             ("Age (Years)", data['age']),
#             ("Gender", data['gender']),
#             ("Marital Status", data['marital_status']),
#             ("Dependants", data['number_of_dependants']),
#             ("Region", data['region']),
#             ("Employment Status", data['employment_status']),
#             ("Income (Lakhs)", data['income_lakhs']),
#             ("Smoking Status", data['smoking_status']),
            
#             # Health Inputs (Raw and Categorized)
#             ("Raw BMI Value", data['raw_bmi_value']),
#             ("Derived BMI Category", data['bmi_category']), 
#             ("Derived Medical History", data['medical_history']),
#             ("Raw Sugar/Diabetes Value (mg/dL)", data['diabetes_value']),
#             ("Raw Systolic BP (mmHg)", data['systolic_pressure_value']),
#             ("Raw Diastolic BP (mmHg)", data['diastolic_pressure_value']),
#             ("Raw Thyroid Status", data['thyroid_status']),
#             ("Raw Heart Disease Status", data['heart_disease_status']),
            
#             ("Insurance Plan", data['insurance_plan']),
#         ]

#         df_review = pd.DataFrame(review_data, columns=["Feature", "Value"])
#         st.dataframe(df_review, use_container_width=True, hide_index=True)


# if __name__ == "__main__":
#     main()
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
        data['age'] = st.number_input("Age (Years)", min_value=18, max_value=100, value=35, step=1)
        data['gender'] = st.radio("Gender", options=["Male", "Female"], index=0, horizontal=True)
        data['marital_status'] = st.selectbox("Marital Status", options=["Married", "Unmarried"], index=0)
        data['number_of_dependants'] = st.select_slider("Number of Dependants", options=list(range(0, 6)), value=1)
        
    with col2:
        st.header("🩺 Health & Lifestyle")
        # Raw BMI value is sent directly to the backend for categorization
        data['raw_bmi_value'] = st.number_input("BMI Value ($kg/m^2$)", min_value=10.0, max_value=60.0, value=25.0, step=0.1, format="%.1f")
        data['smoking_status'] = st.radio("Smoking Status", options=["Non-Smoker", "Regular", "Occasional"], index=0, horizontal=False)
        st.subheader("Specific Disease Parameters")
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
        data['region'] = st.selectbox("Region of Residence", options=["Northwest", "Southeast", "Northeast", "Southwest"], index=0)
        data['employment_status'] = st.selectbox("Employment Status", options=["Salaried", "Self-Employed", "Freelancer"], index=0)
        data['income_lakhs'] = st.number_input("Annual Income ($$Lakhs$$)", min_value=0.0, max_value=200.0, value=15.0, step=0.5, format="%.2f")
        st.subheader("Plan Details")
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
                st.session_state['error_message'] = f"Error during API request: {e}. Check the Flask server logs for details."
            
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
        # st.markdown("---")
        
        st.subheader("Review Processed Categorical Data")
        st.json(st.session_state['processed_data'])

    elif 'error_message' in st.session_state and st.session_state['error_message']:
        st.error(st.session_state['error_message'])

if __name__ == "__main__":
    main()
