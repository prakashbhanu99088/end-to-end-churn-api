import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Load the trained model
model = joblib.load('model_churn.pkl')

# 2. Define the Input Format (Schema)
# This ensures the user sends the right data types
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Contract: str  # We accept string like "One year"

# 3. Create the API App
app = FastAPI(title="Customer Churn Prediction API")

# 4. Define the Prediction Endpoint
@app.post("/predict")
def predict_churn(data: CustomerData):
    # Convert incoming data to a Dictionary
    input_data = data.model_dump()
    
    # Manual Encoding for Contract (Must match train.py!)
    contract_mapping = {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
    
    # Create a DataFrame (The model expects a DataFrame)
    df = pd.DataFrame([{
        'tenure': input_data['tenure'],
        'MonthlyCharges': input_data['MonthlyCharges'],
        'TotalCharges': input_data['TotalCharges'],
        'Contract': contract_mapping.get(input_data['Contract'], 0) # Default to 0 if unknown
    }])

    # Make Prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    # Return the result as JSON
    return {
        "churn_prediction": "Yes" if prediction == 1 else "No",
        "churn_probability": round(probability, 2)
    }