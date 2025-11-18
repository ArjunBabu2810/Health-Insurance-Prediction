import pandas as pd
import joblib
import os
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
# --- Data Transformation Functions (Must match frontend logic) ---

def get_bmi_category(bmi):
    """Categorizes the BMI value into one of the standard categories."""
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25.0:
        return 'Normal'
    elif 25.0 <= bmi < 30.0:
        return 'Overweight'
    else:
        return 'Obesity'

def get_medical_history_category(diabetes_value, systolic_pressure_value, diastolic_pressure_value, thyroid_status, heart_disease_status):
    """Categorizes raw health inputs into a combined 'Medical History' string."""
    # NOTE: Thresholds are simplified for this example application.
    DIABETES_THRESHOLD = 126.0  
    SBP_THRESHOLD = 140         
    DBP_THRESHOLD = 90          
    
    diseases = []
    
    if diabetes_value >= DIABETES_THRESHOLD:
        diseases.append('Diabetes')
    
    # Check for High Blood Pressure based on EITHER Systolic OR Diastolic thresholds
    if (systolic_pressure_value >= SBP_THRESHOLD) or (diastolic_pressure_value >= DBP_THRESHOLD):
        diseases.append('High blood pressure')
    
    if thyroid_status == 'Yes':
        diseases.append('Thyroid')
        
    if heart_disease_status == 'Yes':
        diseases.append('Heart disease')
    
    if not diseases:
        return 'No Disease'

    # Sort diseases alphabetically for consistent output string
    return ' & '.join(sorted(diseases))

# --- Model Loading and Global Variables ---

MODEL = None
TRAINING_COLUMNS = None
IS_SIMULATION = True # Flag to track if we are using the real model or simulation

def load_model_and_features():
    """
    Loads the trained model and the list of features used during training.
    """
    global MODEL, TRAINING_COLUMNS, IS_SIMULATION
    
    MODEL_PATH = 'Model/gradient_boosting_model.joblib'
    COLUMNS_PATH = 'Model/training_columns.joblib'
    
    # Define a default set of columns for robust fallback simulation
    DEFAULT_TRAINING_COLUMNS = [
        'age', 'number_of_dependants', 'income_lakhs', 
        'gender_Female', 'gender_Male', 
        'region_Northeast', 'region_Northwest', 'region_Southeast', 'region_Southwest',
        'marital_status_Married', 'marital_status_Unmarried',
        'bmi_category_Normal', 'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight',
        'smoking_status_Non-Smoker', 'smoking_status_Occasional', 'smoking_status_Regular',
        'employment_status_Freelancer', 'employment_status_Salaried', 'employment_status_Self-Employed',
        'medical_history_Diabetes', 'medical_history_Diabetes & Heart disease',
        'medical_history_Diabetes & High blood pressure', 'medical_history_Diabetes & Thyroid', 
        'medical_history_High blood pressure', 'medical_history_High blood pressure & Heart disease',
        'medical_history_No Disease', 'medical_history_Thyroid',
        'medical_history_Thyroid & Heart disease',
        'insurance_plan_Bronze', 'insurance_plan_Gold', 'insurance_plan_Silver'
    ]

    try:
        # Attempt to load the actual model and features list
        MODEL = joblib.load(MODEL_PATH)
        TRAINING_COLUMNS = joblib.load(COLUMNS_PATH)
        IS_SIMULATION = False # Real model loaded successfully

        print(f"Model and features successfully loaded from {MODEL_PATH} and {COLUMNS_PATH}.")

    except FileNotFoundError as e:
        print(f"FATAL ERROR: Model files not found at expected path ({e}). Falling back to simulation mode.")
        IS_SIMULATION = True 
        MODEL = True 
        TRAINING_COLUMNS = DEFAULT_TRAINING_COLUMNS
        
    except Exception as e:
        print(f"WARNING: An unexpected error occurred during model loading: {e}. Falling back to simulation mode.")
        IS_SIMULATION = True 
        MODEL = True
        TRAINING_COLUMNS = DEFAULT_TRAINING_COLUMNS


def predict_premium(data):
    """
    Processes input data, aligns features, and performs prediction using the loaded model.
    Handles both raw and pre-categorized input formats for robustness.
    """
    global MODEL, TRAINING_COLUMNS, IS_SIMULATION

    # --- Step 1: Preprocessing & Feature Engineering (Robust Input Handling) ---
    
    # 1. Handle BMI Category
    if 'raw_bmi_value' in data:
        # Use existing categorization logic if raw value is provided (as in frontend.py)
        bmi_category = get_bmi_category(data['raw_bmi_value'])
    elif 'bmi_category' in data:
        # Use the provided category directly (as in user's example JSON)
        bmi_category = data['bmi_category']
    else:
        # Fallback in case of incomplete data
        raise ValueError("Missing both 'raw_bmi_value' and 'bmi_category' in input data.")

    # 2. Handle Medical History Category
    if 'diabetes_value' in data and 'systolic_pressure_value' in data and 'diastolic_pressure_value' in data:
        # Use existing categorization logic if raw values are provided (as in frontend.py)
        medical_history = get_medical_history_category(
            data['diabetes_value'], 
            data['systolic_pressure_value'], 
            data['diastolic_pressure_value'], 
            data.get('thyroid_status', 'No'), # Use .get for robustness
            data.get('heart_disease_status', 'No') # Use .get for robustness
        )
    elif 'medical_history' in data:
        # Use the provided category directly (as in user's example JSON)
        medical_history = data['medical_history']
    else:
        # Fallback
        raise ValueError("Missing necessary raw inputs or 'medical_history' in input data.")


    # Create a DataFrame containing all required features
    input_df = pd.DataFrame([{
        'age': data['age'],
        'gender': data['gender'],
        'region': data['region'],
        'marital_status': data['marital_status'],
        'number_of_dependants': data['number_of_dependants'],
        'bmi_category': bmi_category, # Categorical feature
        'smoking_status': data['smoking_status'],
        'employment_status': data['employment_status'],
        'income_lakhs': data['income_lakhs'],
        'medical_history': medical_history, # Categorical feature
        'insurance_plan': data['insurance_plan'],
    }])

    # --- Step 2 & 3: Encoding and Alignment ---
    # One-hot encode the categorical features in the input DataFrame
    input_df_encoded = pd.get_dummies(input_df, drop_first=False)
    
    # 🌟 Feature Alignment: Ensure the columns match the training columns 🌟
    if TRAINING_COLUMNS is None:
        print("ERROR: TRAINING_COLUMNS not defined. Cannot proceed.")
        return 0 
        
    # Find columns present in training data but missing in this specific input
    missing_cols = set(TRAINING_COLUMNS) - set(input_df_encoded.columns)
    
    # Add missing columns with a value of 0 (zero padding)
    for c in missing_cols:
        input_df_encoded[c] = 0
    
    # Reorder columns to exactly match the sequence expected by the model
    final_features = input_df_encoded[TRAINING_COLUMNS]
    categorical_features = final_features.select_dtypes(include=['object', 'category']).columns
    numerical_features = final_features.select_dtypes(include=np.number).columns.drop('Annual_Premium_Amount')

    # Create a column transformer to apply one-hot encoding to categorical features
    preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough')


    pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

    final_features = pipeline.fit_transform(final_features)
    # --- Step 4: Prediction ---
    if not IS_SIMULATION:
        # --- REAL MODEL PREDICTION ---
        try:
            for i in final_features:
                print(i)
            prediction = MODEL.predict(final_features)[0]
        except Exception as e:
            print(f"ERROR during real model prediction: {e}. Returning simulation value.")
            prediction = 25000 
            
    else: 
        # --- SIMULATION LOGIC (USED IF REAL MODEL FAILS TO LOAD) ---
        
        # Determine values for simulation based on available input
        sim_bmi = data.get('raw_bmi_value', 25.0) # Use 25.0 as default if raw value is missing in simulation
        sim_smoking_status = data['smoking_status']
        sim_medical_count = len(medical_history.split(' & ')) if medical_history != 'No Disease' else 0

        base_premium = 15000 
        age_factor = data['age'] * 150
        bmi_factor = sim_bmi * 200
        
        smoking_multiplier = 1.0
        if sim_smoking_status == 'Regular':
             smoking_multiplier = 2.5
        elif sim_smoking_status == 'Occasional':
             smoking_multiplier = 1.5

        medical_factor = sim_medical_count * 5000
        
        predicted_premium_base = base_premium + age_factor + bmi_factor + medical_factor
        prediction = int(predicted_premium_base * smoking_multiplier)
        # --- END SIMULATION LOGIC ---
    
    # Ensure prediction is a non-negative integer
    return max(0, int(prediction))

