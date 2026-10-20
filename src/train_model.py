import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import os
from feature_engineering import preprocess_customer_data

def train_churn_model():
    """
    Trains a machine learning classifier to predict customer churn 
    using engineered features from MySQL views.
    """
    print("🚀 Starting Phase 3: Machine Learning Model Training...")
    
    # 1. Load engineered dataset
    df = preprocess_customer_data()
    if df is None:
        print("❌ Error: Could not load processed data.")
        return
        
    # Define target column
    target_col = 'is_churned'
    if target_col not in df.columns:
        print(f"❌ Error: Target column '{target_col}' not found in dataset. Available columns: {df.columns.tolist()}")
        return
        
    # Exclude non-feature columns (IDs, dates, or target)
    exclude_cols = [target_col, 'customer_id', 'signup_date', 'last_activity_date']
    feature_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]
    
    X = df[feature_cols].fillna(0)
    y = df[target_col]
    
    print(f"📊 Features selected for training ({len(feature_cols)}): {feature_cols}")
    print(f"📈 Target churn distribution:\n{y.value_counts(normalize=True)}")
    
    # 2. Train-test split (stratified to preserve class balance)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. Train Classifier (Random Forest with balanced weights for churn prediction)
    print("🤖 Training Random Forest Churn Prediction Model...")
    model = RandomForestClassifier(
        n_estimators=150, 
        max_depth=10, 
        random_state=42, 
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    
    # 4. Evaluate Model Performance
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print("\n--- Model Evaluation Report ---")
    print(f"🎯 ROC-AUC Score: {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # 5. Save Model and Feature Metadata
    os.makedirs('models', exist_ok=True)
    model_path = 'models/churn_model.pkl'
    
    artifact = {
        'model': model,
        'feature_cols': feature_cols
    }
    joblib.dump(artifact, model_path)
    print(f"Trained model artifact successfully saved to '{model_path}'!")
    
    return model

if __name__ == "__main__":
    train_churn_model()