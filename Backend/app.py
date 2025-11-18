from flask import Flask, request, jsonify, abort
from model_utils import load_model_and_features, predict_premium
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for the Streamlit frontend to communicate with the Flask API
CORS(app) 

# Load model and feature list when the application starts
# This is a critical step for a production model
load_model_and_features()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives raw feature data, preprocesses it, and returns a premium prediction.
    
    Expected JSON payload structure:
    {
        "age": 35,
        "gender": "Male",
        "region": "Northwest",
        "marital_status": "Married",
        "number_of_dependants": 1,
        "smoking_status": "Non-Smoker",
        "employment_status": "Salaried",
        "income_lakhs": 15.0,
        "insurance_plan": "Silver",
        "raw_bmi_value": 25.0,
        "diabetes_value": 95.0,
        "systolic_pressure_value": 120,
        "diastolic_pressure_value": 80,
        "thyroid_status": "No",
        "heart_disease_status": "No"
    }
    """
    if not request.json:
        # Bad request if no JSON is provided
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
        
        # Return the result as a JSON object
        return jsonify({
            'predicted_premium': round(float(prediction), 2)
        })

    except Exception as e:
        # Log the error and return a 500 status
        print(f"An error occurred during prediction: {e}")
        return jsonify({'error': 'Prediction failed due to internal server error.'}), 500

@app.route('/', methods=['GET'])
def home():
    """Simple route to confirm the API is running."""
    return "Insurance Prediction API is Running!"

if __name__ == '__main__':
    # Running on port 5000 by default. 
    # Use 0.0.0.0 for external accessibility (important for deployment/testing with Streamlit)
    app.run(host='0.0.0.0', port=5000, debug=True)
