import joblib
import shap
import numpy as np

# Load model
model = joblib.load("Model/gradient_boosting_model_cleaned.pkl")
print("✅ Model loaded successfully.")

# Define input
input_vector = np.array([[0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 26, 3, 28]])

# Predict
prediction = model.predict(input_vector)
print("Prediction:", prediction)

# Explain with SHAP
explainer = shap.Explainer(model, input_vector)
shap_values = explainer(input_vector)

# Print SHAP values
print("SHAP values:", shap_values.values)
print("Base value:", shap_values.base_values)

# Optional: visualize
shap.plots.waterfall(shap_values[0])