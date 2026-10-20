import pandas as pd
from data_loader import load_analytics_views

def preprocess_customer_data():
    """
    Loads analytics views, merges them, handles missing values, 
    encodes categorical variables, and prepares features for machine learning.
    """
    print("🔄 Loading data views for feature engineering...")
    dfs = load_analytics_views()
    
    if not dfs:
        print("❌ Failed to load data views.")
        return None
        
    rfm_df = dfs["rfm"]
    friction_df = dfs["value_friction"]
    
    print("🛠️ Merging RFM and Value-Friction datasets...")
    # Merge datasets on customer_id
    merged_df = pd.merge(
        rfm_df,
        friction_df[['customer_id', 'total_spend', 'total_invoices', 'avg_monthly_logins', 'total_support_tickets', 'avg_resolution_time_hours']],
        on='customer_id',
        how='inner'
    )
    
    print("🧹 Cleaning missing values and engineering features...")
    # Fill missing values for numerical friction metrics with 0
    numeric_cols = ['total_spend', 'total_invoices', 'avg_monthly_logins', 'total_support_tickets', 'avg_resolution_time_hours']
    for col in numeric_cols:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].fillna(0)
            
    # Encode categorical variables (e.g., subscription_tier) using one-hot encoding
    if 'subscription_tier' in merged_df.columns:
        merged_df = pd.get_dummies(merged_df, columns=['subscription_tier'], drop_first=True, dtype=int)
        
    print(f"✅ Feature engineering complete! Final dataset shape: {merged_df.shape}")
    return merged_df

if __name__ == "__main__":
    processed_data = preprocess_customer_data()
    if processed_data is not None:
        print("\n--- Processed Dataset Preview ---")
        print(processed_data.head(3))
        print("\nColumns available for modeling:", processed_data.columns.tolist())