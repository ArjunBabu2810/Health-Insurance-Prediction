import pandas as pd
import joblib
import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
# Note: OneHotEncoder is only needed if you are defining the preprocessor here, 
# but since you are loading it, these are technically unnecessary imports 
# for the *deployment* file, but they don't hurt.

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
PREPROCESSOR = None # New global variable for the ColumnTransformer/Pipeline
IS_SIMULATION = True # Flag to track if we are using the real model or simulation

def load_model_and_features():
    """
    Loads the trained model and the Scikit-learn preprocessor pipeline.
    """
    global MODEL, PREPROCESSOR, IS_SIMULATION
    
    MODEL_PATH = '../Model/gradient_boosting_model_cleaned.pkl'
    PREPROCESSOR_PATH = '../Model/preprocessor_cleaned.joblib' 
    
    # try:
        # Attempt to load the actual model and preprocessor pipeline
    MODEL = joblib.load(MODEL_PATH)
    PREPROCESSOR = joblib.load(PREPROCESSOR_PATH)
    IS_SIMULATION = False # Real model and preprocessor loaded successfully

    print(f"Model and preprocessor successfully loaded from {MODEL_PATH} and {PREPROCESSOR_PATH}.")

    # except FileNotFoundError as e:
    #     print(f"FATAL ERROR: Model or Preprocessor files not found at expected path ({e}). Falling back to simulation mode.")
    #     IS_SIMULATION = True 
    #     MODEL = True  # Placeholder for simulation mode
    #     PREPROCESSOR = True # Placeholder for simulation mode
        
    # except Exception as e:
    #     print(f"WARNING: An unexpected error occurred during model loading: {e}. Falling back to simulation mode.")
    #     IS_SIMULATION = True 
    #     MODEL = True
    #     PREPROCESSOR = True


def predict_premium(data):
    """
    Processes input data, transforms features using the Scikit-learn preprocessor, 
    and performs prediction using the loaded model.
    """
    global MODEL, PREPROCESSOR, IS_SIMULATION

    # --- Step 1: Preprocessing & Feature Engineering (Robust Input Handling) ---
    
    # 1. Handle BMI Category
    if 'raw_bmi_value' in data:
        bmi_category = get_bmi_category(data['raw_bmi_value'])
    elif 'bmi_category' in data:
        bmi_category = data['bmi_category']
    else:
        raise ValueError("Missing both 'raw_bmi_value' and 'bmi_category' in input data.")

    # 2. Handle Medical History Category
    if 'diabetes_value' in data and 'systolic_pressure_value' in data and 'diastolic_pressure_value' in data:
        medical_history = get_medical_history_category(
            data['diabetes_value'], 
            data['systolic_pressure_value'], 
            data['diastolic_pressure_value'], 
            data.get('thyroid_status', 'No'), 
            data.get('heart_disease_status', 'No')
        )
    elif 'medical_history' in data:
        medical_history = data['medical_history']
    else:
        raise ValueError("Missing necessary raw inputs or 'medical_history' in input data.")


    # Create a DataFrame containing all required features 
    # NOTE: The column names MUST match the names used in the training data 
    # (inferred from the training script to be capitalized/spaced).
    input_df = pd.DataFrame([{
        'Age': data['age'],
        'Gender': data['gender'],
        'Region': data['region'],
        'Marital_status': data['marital_status'],
        'Number Of Dependants': data['number_of_dependants'], # Note the space
        'BMI_Category': bmi_category, 
        'Smoking_Status': data['smoking_status'],
        'Employment_Status': data['employment_status'],
        'Income_Lakhs': data['income_lakhs'],
        'Medical History': medical_history, # Note the space
        'Insurance_Plan': data['insurance_plan'],
    }])
    categorical_features = input_df.select_dtypes(include=['object', 'category']).columns
    numerical_features = input_df.select_dtypes(include=np.number)

    # Create a column transformer to apply one-hot encoding to categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
        remainder='passthrough')



    final_features = PREPROCESSOR.transform(input_df)

    print(final_features)
    try:
        # Use the loaded PREPROCESSOR to transform the raw input DataFrame
        prediction = MODEL.predict(final_features)
        # This is the correct step for deployment.
        print(final_features)
    except Exception as e:
        print(f"ERROR: Preprocessor transformation failed: {e}. Falling back to simulation.")
        prediction = 25000 
    return prediction
    

# --- Flask App Definition ---

app = Flask(__name__)
CORS(app) 

# Load model and feature list when the application starts
load_model_and_features()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives raw feature data, preprocesses it using the loaded Scikit-learn
    preprocessor, and returns a premium prediction.
    """
    if not request.json:
        return jsonify({'error': 'No JSON payload provided'}), 400
    
    data = request.json
    print(data)
    
    # Input validation (basic check for required keys)
    required_keys = [
        "age", "gender", "region", "marital_status", "number_of_dependants", 
        "smoking_status", "employment_status", "income_lakhs", "insurance_plan", 
        "raw_bmi_value", "diabetes_value", "systolic_pressure_value", 
        "diastolic_pressure_value", "thyroid_status", "heart_disease_status"
    ]
    
    if not all(key in data for key in required_keys):
        return jsonify({'error': 'Missing one or more required input keys'}), 400

    try:
        # Get the prediction using the utility function
        prediction = predict_premium(data)
        print("Predicted amount : ",prediction)
        # Return the result as a JSON object
        return jsonify({
            'predicted_premium': round(float(prediction), 2)
        })

    except ValueError as ve:
        # Catch specific ValueErrors raised in predict_premium for missing data
        print(f"Input Data Error: {ve}")
        return jsonify({'error': f'Invalid input: {ve}'}), 400

    except Exception as e:
        # Log the error and return a 500 status
        print(f"An unexpected error occurred during prediction: {e}")
        return jsonify({'error': 'Prediction failed due to internal server error.'}), 500

@app.route('/', methods=['GET'])
def home():
    """Simple route to confirm the API is running."""
    return "Insurance Prediction API is Running! (Using Scikit-learn Preprocessor)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)