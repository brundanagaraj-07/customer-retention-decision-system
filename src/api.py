from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

# Initialize FastAPI app
app = FastAPI(
    title="RevGuard API",
    description="Customer Value & Retention Decision System Inference API",
    version="1.0.0"
)

# Load trained model artifact on startup
MODEL_PATH = 'models/churn_model.pkl'
if os.path.exists(MODEL_PATH):
    artifact = joblib.load(MODEL_PATH)
    model = artifact['model']
    feature_cols = artifact['feature_cols']
else:
    model = None
    feature_cols = []

# Define input schema for single-customer inference requests
class CustomerFeatureInput(BaseModel):
    recency: float = 0.0
    frequency: float = 0.0
    monetary: float = 0.0
    avg_monthly_logins: float = 0.0
    total_support_tickets: float = 0.0
    avg_resolution_time_hours: float = 0.0
    total_spend: float = 0.0

@app.get("/")
def health_check():
    """Health check endpoint to verify API status."""
    return {
        "status": "online",
        "system": "RevGuard Customer Value & Retention Decision System",
        "model_loaded": model is not None
    }

@app.post("/predict-churn")
def predict_customer_churn(data: CustomerFeatureInput):
    """
    Accepts customer behavioral and transactional metrics,
    runs inference using the trained churn model, and returns risk tiers.
    """
    if model is None:
        raise HTTPException(
            status_code=500, 
            detail="Model artifact not found. Please run `train_model.py` first."
        )
    
    try:
        # Convert incoming JSON payload to a DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # Ensure all feature columns expected by the model exist
        for col in feature_cols:
            if col not in input_df.columns:
                input_df[col] = 0.0
                
        X = input_df[feature_cols].fillna(0)
        
        # Predict probability and class
        churn_prob = float(model.predict_proba(X)[:, 1][0])
        predicted_class = int(model.predict(X)[0])
        
        # Assign Risk Tier
        if churn_prob > 0.70:
            risk_tier = "High Risk"
        elif churn_prob > 0.30:
            risk_tier = "Medium Risk"
        else:
            risk_tier = "Low Risk"
            
        return {
            "churn_probability": round(churn_prob, 4),
            "predicted_churn": predicted_class,
            "risk_tier": risk_tier,
            "recommendation": "Immediate retention outreach required" if risk_tier == "High Risk" else "Standard engagement monitor"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Inference error: {str(e)}")