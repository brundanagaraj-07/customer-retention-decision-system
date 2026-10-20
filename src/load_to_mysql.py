import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

def load_data():
    try:
        # Connect to your local MySQL server (Update password if needed)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Nagaraj@1211'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 1. Create Database and Tables automatically
            print("Setting up database and tables...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS revguard_db;")
            cursor.execute("USE revguard_db;")
            
            # Drop and create tables to ensure clean state
            cursor.execute("DROP TABLE IF EXISTS fact_support_tickets;")
            cursor.execute("DROP TABLE IF EXISTS fact_usage_monthly;")
            cursor.execute("DROP TABLE IF EXISTS fact_transactions;")
            cursor.execute("DROP TABLE IF EXISTS dim_customers;")

            cursor.execute("""
                CREATE TABLE dim_customers (
                    customer_id VARCHAR(20) PRIMARY KEY,
                    signup_date DATE NOT NULL,
                    subscription_tier VARCHAR(20) NOT NULL,
                    acquisition_channel VARCHAR(30) NOT NULL,
                    is_churned TINYINT NOT NULL,
                    churn_date DATE DEFAULT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE fact_transactions (
                    transaction_id VARCHAR(20) PRIMARY KEY,
                    customer_id VARCHAR(20) NOT NULL,
                    transaction_date DATE NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    discount_applied DECIMAL(4, 2) NOT NULL,
                    payment_status VARCHAR(20) NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
                );
            """)

            cursor.execute("""
                CREATE TABLE fact_usage_monthly (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id VARCHAR(20) NOT NULL,
                    usage_month DATE NOT NULL,
                    login_count INT NOT NULL,
                    feature_breadth_score INT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
                );
            """)

            cursor.execute("""
                CREATE TABLE fact_support_tickets (
                    ticket_id VARCHAR(20) PRIMARY KEY,
                    customer_id VARCHAR(20) NOT NULL,
                    ticket_date DATE NOT NULL,
                    issue_type VARCHAR(30) NOT NULL,
                    resolution_status VARCHAR(20) NOT NULL,
                    resolution_time_hours DECIMAL(6, 1) NOT NULL,
                    satisfaction_score INT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
                );
            """)
            print("Tables created successfully.")

            # 2. Read and load customers
            print("Loading customers.csv...")
            df_cust = pd.read_csv("data/raw/customers.csv")
            for _, row in df_cust.iterrows():
                cursor.execute("""
                    INSERT IGNORE INTO dim_customers 
                    (customer_id, signup_date, subscription_tier, acquisition_channel, is_churned, churn_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row['customer_id'], row['signup_date'], row['subscription_tier'], 
                    row['acquisition_channel'], row['is_churned'], 
                    row['churn_date'] if pd.notna(row['churn_date']) else None
                ))

            # 3. Read and load transactions
            print("Loading transactions.csv...")
            df_txn = pd.read_csv("data/raw/transactions.csv")
            for _, row in df_txn.iterrows():
                cursor.execute("""
                    INSERT IGNORE INTO fact_transactions 
                    (transaction_id, customer_id, transaction_date, amount, discount_applied, payment_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row['transaction_id'], row['customer_id'], row['transaction_date'], 
                    row['amount'], row['discount_applied'], row['payment_status']
                ))

            # 4. Read and load usage
            print("Loading usage.csv...")
            df_usage = pd.read_csv("data/raw/usage.csv")
            for _, row in df_usage.iterrows():
                cursor.execute("""
                    INSERT INTO fact_usage_monthly 
                    (customer_id, usage_month, login_count, feature_breadth_score)
                    VALUES (%s, %s, %s, %s)
                """, (
                    row['customer_id'], row['usage_month'], row['login_count'], row['feature_breadth_score']
                ))

            # 5. Read and load support tickets
            print("Loading support_tickets.csv...")
            df_tkt = pd.read_csv("data/raw/support_tickets.csv")
            for _, row in df_tkt.iterrows():
                cursor.execute("""
                    INSERT IGNORE INTO fact_support_tickets 
                    (ticket_id, customer_id, ticket_date, issue_type, resolution_status, resolution_time_hours, satisfaction_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['ticket_id'], row['customer_id'], row['ticket_date'], 
                    row['issue_type'], row['resolution_status'], row['resolution_time_hours'], row['satisfaction_score']
                ))

            connection.commit()
            print("All CSV data successfully ingested into MySQL tables!")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    load_data()