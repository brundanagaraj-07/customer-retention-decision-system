import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
from feature_engineering import preprocess_customer_data

# Page Configuration
st.set_page_config(
    page_title="RevGuard: Retention Decision System",
    page_icon="🛡️",
    layout="wide"
)

# Load Model Artifact
MODEL_PATH = 'models/churn_model.pkl'
@st.cache_resource
def load_model_artifact():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

artifact = load_model_artifact()

# App Header
st.title("🛡️ RevGuard: Customer Value & Retention Decision System")
st.markdown("### Executive Dashboard & Real-Time Churn Risk Intelligence")
st.markdown("---")

if artifact is None:
    st.error("❌ Model artifact not found! Please run `train_model.py` first.")
else:
    model = artifact['model']
    feature_cols = artifact['feature_cols']
    
    # Load and Score Data
    with st.spinner("🔄 Loading customer analytics and scoring risk tiers..."):
        df = preprocess_customer_data()
        
    if df is not None:
        X = df[feature_cols].fillna(0)
        df['churn_probability'] = model.predict_proba(X)[:, 1]
        df['predicted_churn'] = model.predict(X)
        
        # Assign Risk Tiers
        df['risk_tier'] = pd.cut(
            df['churn_probability'],
            bins=[-0.01, 0.30, 0.70, 1.00],
            labels=['Low Risk', 'Medium Risk', 'High Risk']
        )
        
        # Top-Level Metrics
        col1, col2, col3, col4 = st.columns(4)
        total_customers = len(df)
        high_risk_count = len(df[df['risk_tier'] == 'High Risk'])
        med_risk_count = len(df[df['risk_tier'] == 'Medium Risk'])
        avg_churn_prob = df['churn_probability'].mean() * 100
        
        col1.metric("Total Customers Monitored", f"{total_customers:,}")
        col2.metric("High Risk (Immediate Action)", f"{high_risk_count:,}", delta_color="inverse")
        col3.metric("Medium Risk (Monitor)", f"{med_risk_count:,}")
        col4.metric("Average Churn Probability", f"{avg_churn_prob:.1f}%")
        
        st.markdown("---")
        
        # Tabs for Navigation
        tab1, tab2 = st.tabs(["📊 Portfolio Risk Analytics", "🔍 Live Customer Simulation"])
        
        with tab1:
            st.subheader("Customer Risk Tier Distribution")
            fig = px.pie(
                df, 
                names='risk_tier', 
                title="Proportion of Customers by Churn Risk Tier",
                color='risk_tier',
                color_discrete_map={'Low Risk': '#2ecc71', 'Medium Risk': '#f1c40f', 'High Risk': '#e74c3c'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("🚨 High-Risk Customers Requiring Outreach")
            high_risk_df = df[df['risk_tier'] == 'High Risk'].sort_values(by='churn_probability', ascending=False)
            st.dataframe(high_risk_df[['customer_id', 'churn_probability', 'total_spend', 'avg_monthly_logins', 'total_support_tickets']], use_container_width=True)
            
        with tab2:
            st.subheader("Simulate Customer Churn Risk")
            st.markdown("Adjust customer metrics in the sidebar or below to calculate real-time churn probability.")
            
            col_a, col_b = st.columns(2)
            with col_a:
                sim_recency = st.slider("Recency (Days since last activity)", 0, 90, 15)
                sim_frequency = st.slider("Transaction Frequency", 1, 50, 5)
                sim_monetary = st.number_input("Monetary Value (\$)", 10.0, 5000.0, 250.0)
                sim_logins = st.slider("Avg Monthly Logins", 0.0, 30.0, 10.0)
            with col_b:
                sim_tickets = st.slider("Total Support Tickets", 0, 20, 2)
                sim_resolution = st.slider("Avg Resolution Time (Hours)", 0.0, 72.0, 12.0)
                sim_spend = st.number_input("Total Spend (\$)", 50.0, 10000.0, 500.0)
                
            if st.button("Calculate Churn Risk", type="primary"):
                sim_data = pd.DataFrame([{
                    'recency': sim_recency,
                    'frequency': sim_frequency,
                    'monetary': sim_monetary,
                    'avg_monthly_logins': sim_logins,
                    'total_support_tickets': sim_tickets,
                    'avg_resolution_time_hours': sim_resolution,
                    'total_spend': sim_spend
                }])
                
                # Align with model features
                for col in feature_cols:
                    if col not in sim_data.columns:
                        sim_data[col] = 0.0
                X_sim = sim_data[feature_cols].fillna(0)
                
                prob = float(model.predict_proba(X_sim)[:, 1][0])
                
                if prob > 0.70:
                    tier, color = "High Risk", "red"
                elif prob > 0.30:
                    tier, color = "Medium Risk", "orange"
                else:
                    tier, color = "Low Risk", "green"
                    
                st.markdown(f"### Predicted Churn Probability: `{prob * 100:.2f}%`")
                st.markdown(f"### Risk Tier: `:{color}[{tier}]`")