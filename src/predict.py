import pandas as pd
import numpy as np
import joblib
import os
from feature_engineering import preprocess_customer_data

def generate_churn_predictions():
    """
    Loads the trained churn model, generates risk probabilities for active customers,
    and assigns actionable risk tiers for retention decision-making.
    """
    print("🔍 Starting Phase 4: Inference & Retention Decision Scoring...")
    
    # 1. Check if trained model artifact exists
    model_path = 'models/churn_model.pkl'
    if not os.path.exists(model_path):
        print(f"❌ Error: Model artifact not found at '{model_path}'. Please run `train_model.py` first.")
        return None
        
    # Load model and feature metadata
    artifact = joblib.load(model_path)
    model = artifact['model']
    feature_cols = artifact['feature_cols']
    
    # 2. Load latest processed customer data via feature engineering pipeline
    df = preprocess_customer_data()
    if df is None:
        print("❌ Error: Could not load customer data for prediction.")
        return None
        
    # Align features with training columns
    X = df[feature_cols].fillna(0)
    
    # 3. Generate churn probabilities and predictions
    print("⚙️ Calculating churn risk probabilities...")
    churn_probabilities = model.predict_proba(X)[:, 1]
    churn_predictions = model.predict(X)
    
    # 4. Compile results dataframe
    results_df = df[['customer_id']].copy() if 'customer_id' in df.columns else pd.DataFrame()
    results_df['churn_probability'] = churn_probabilities
    results_df['predicted_churn'] = churn_predictions
    
    # 5. Assign Actionable Risk Tiers for Retention
    results_df['risk_tier'] = pd.cut(
        results_df['churn_probability'],
        bins=[-0.01, 0.30, 0.70, 1.00],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )
    
    print(f"✅ Successfully scored {len(results_df)} customers!")
    return results_df.sort_values(by='churn_probability', ascending=False)

if __name__ == "__main__":
    scored_customers = generate_churn_predictions()
    if scored_customers is not None:
        print("\n--- Top High-Risk Customers for Retention Intervention ---")
        print(scored_customers.head(10))
        
        # Summary distribution of risk tiers
        print("\n--- Risk Tier Distribution ---")
        print(scored_customers['risk_tier'].value_counts())