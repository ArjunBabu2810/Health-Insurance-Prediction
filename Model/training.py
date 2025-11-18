import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import shap

import joblib
import os

# Load data
df = pd.read_csv("cleaned_premiums.csv")

X = df.drop('Annual_Premium_Amount', axis=1)
y = df['Annual_Premium_Amount']

# Identify categorical and numerical features
categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
numerical_features = X.select_dtypes(include=np.number).columns.tolist()

# Preprocessor: one-hot encode categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

# Transform features
X_processed = preprocessor.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Train model
model = GradientBoostingRegressor()
model.fit(X_train, y_train)
explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)
shap.plots.waterfall(shap_values[0])

# Save clean artifacts
os.makedirs("Model", exist_ok=True)
joblib.dump(model, "Model/gradient_boosting_model_cleaned.pkl")
joblib.dump(preprocessor, "Model/preprocessor_cleaned.joblib")
joblib.dump(categorical_features + numerical_features, "Model/training_columns_cleaned.joblib")
joblib.dump(explainer, "Model/shap_explainer.joblib")

print("✅ Model and preprocessor saved cleanly.")