import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

os.makedirs("data/raw", exist_ok=True)

print("Generating synthetic relational dataset...")

NUM_CUSTOMERS = 2000
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 10, 1)

# 1. Customers Table
customer_ids = [f"CUST_{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)]
signup_dates = [
    start_date + timedelta(days=random.randint(0, 300)) 
    for _ in range(NUM_CUSTOMERS)
]

tiers = ['Standard', 'Pro', 'Enterprise']
tier_weights = [0.60, 0.30, 0.10]
channels = ['Organic', 'Paid Search', 'Referral', 'Social Media']
channel_weights = [0.40, 0.30, 0.20, 0.10]

customers_data = []
for cid, s_date in zip(customer_ids, signup_dates):
    tier = random.choices(tiers, weights=tier_weights)[0]
    channel = random.choices(channels, weights=channel_weights)[0]
    
    base_churn_prob = 0.25 if tier == 'Standard' else (0.15 if tier == 'Pro' else 0.08)
    is_churned = random.random() < base_churn_prob
    
    churn_date = None
    if is_churned:
        max_possible_churn = (end_date - s_date).days
        if max_possible_churn > 30:
            churn_days = random.randint(30, min(max_possible_churn, 300))
            churn_date = s_date + timedelta(days=churn_days)
            
    customers_data.append({
        'customer_id': cid,
        'signup_date': s_date.strftime('%Y-%m-%d'),
        'subscription_tier': tier,
        'acquisition_channel': channel,
        'is_churned': int(is_churned),
        'churn_date': churn_date.strftime('%Y-%m-%d') if churn_date else None
    })

df_customers = pd.DataFrame(customers_data)
df_customers.to_csv("data/raw/customers.csv", index=False)

# 2. Transactions Table
transactions_data = []
tx_id_counter = 1

for _, row in df_customers.iterrows():
    cid = row['customer_id']
    s_date = datetime.strptime(str(row['signup_date']), '%Y-%m-%d')
    c_date = datetime.strptime(str(row['churn_date']), '%Y-%m-%d') if pd.notna(row['churn_date']) else end_date
    
    tier_pricing = {'Standard': 29.99, 'Pro': 79.99, 'Enterprise': 249.99}
    base_amount = tier_pricing[row['subscription_tier']]
    
    curr_date = s_date.replace(day=1)
    while curr_date <= c_date and curr_date <= end_date:
        if curr_date >= s_date:
            discount = random.choice([0.0, 0.0, 0.0, 0.15, 0.20]) if row['subscription_tier'] != 'Standard' else 0.0
            amount = round(base_amount * (1 - discount), 2)
            payment_failed = random.random() < 0.05
            
            transactions_data.append({
                'transaction_id': f"TXN_{tx_id_counter:07d}",
                'customer_id': cid,
                'transaction_date': curr_date.strftime('%Y-%m-%d'),
                'amount': amount,
                'discount_applied': discount,
                'payment_status': 'Failed' if payment_failed else 'Success'
            })
            tx_id_counter += 1
            
        if curr_date.month == 12:
            curr_date = curr_date.replace(year=curr_date.year + 1, month=1)
        else:
            curr_date = curr_date.replace(month=curr_date.month + 1)

df_transactions = pd.DataFrame(transactions_data)
df_transactions.to_csv("data/raw/transactions.csv", index=False)

# 3. Usage Activity Table
usage_data = []
for _, row in df_customers.iterrows():
    cid = row['customer_id']
    s_date = datetime.strptime(str(row['signup_date']), '%Y-%m-%d')
    c_date = datetime.strptime(str(row['churn_date']), '%Y-%m-%d') if pd.notna(row['churn_date']) else end_date
    
    curr_date = s_date.replace(day=1)
    while curr_date <= c_date and curr_date <= end_date:
        is_near_churn = row['is_churned'] and (c_date - curr_date).days < 60
        base_logins = 25 if row['subscription_tier'] == 'Enterprise' else (15 if row['subscription_tier'] == 'Pro' else 8)
        
        login_count = max(1, int(np.random.normal(base_logins, 3) * (0.3 if is_near_churn else 1.0)))
        feature_breadth = random.randint(1, 10)
        
        usage_data.append({
            'customer_id': cid,
            'usage_month': curr_date.strftime('%Y-%m-01'),
            'login_count': login_count,
            'feature_breadth_score': feature_breadth
        })
        
        if curr_date.month == 12:
            curr_date = curr_date.replace(year=curr_date.year + 1, month=1)
        else:
            curr_date = curr_date.replace(month=curr_date.month + 1)

df_usage = pd.DataFrame(usage_data)
df_usage.to_csv("data/raw/usage.csv", index=False)

# 4. Support Tickets Table
tickets_data = []
ticket_id_counter = 1
issue_types = ['Billing', 'Technical Bug', 'Feature Request', 'Account Access', 'Performance']

for _, row in df_customers.iterrows():
    cid = row['customer_id']
    num_tickets = random.randint(2, 5) if row['is_churned'] else random.randint(0, 2)
    s_date = datetime.strptime(str(row['signup_date']), '%Y-%m-%d')
    c_date = datetime.strptime(str(row['churn_date']), '%Y-%m-%d') if pd.notna(row['churn_date']) else end_date
    
    for _ in range(num_tickets):
        t_date = s_date + timedelta(days=random.randint(5, max(6, (c_date - s_date).days)))
        if t_date > end_date:
            continue
            
        # Fixed to use numpy random exponential instead of random.exponential
        resolution_time_hours = np.random.exponential(scale=24)
        if row['is_churned']:
            resolution_time_hours *= 1.8
            
        status = random.choices(['Resolved', 'Unresolved'], weights=[0.8, 0.2])[0]
        sat_score = random.randint(1, 3) if status == 'Unresolved' else random.randint(3, 5)

        tickets_data.append({
            'ticket_id': f"TKT_{ticket_id_counter:07d}",
            'customer_id': cid,
            'ticket_date': t_date.strftime('%Y-%m-%d'),
            'issue_type': random.choice(issue_types),
            'resolution_status': status,
            'resolution_time_hours': round(resolution_time_hours, 1),
            'satisfaction_score': sat_score
        })
        ticket_id_counter += 1

df_tickets = pd.DataFrame(tickets_data)
df_tickets.to_csv("data/raw/support_tickets.csv", index=False)

print("Successfully generated all raw relational files in data/raw/!")