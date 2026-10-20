create database if not exists revguard_db;

use revguard_db;

drop table if exists fact_support_tickets;
drop table if exists fact_usage_monthly;
drop table if exists fact_transactions;
drop table if exists dim_customers

create table dim_customers(
    customer_id varchar(20) primary key,
    signup_date DATE NOT NULL,
    subscription_tier VARCHAR(20) NOT NULL,
    acquisition_channel VARCHAR(30) NOT NULL,
    is_churned TINYINT NOT NULL,
    churn_date DATE DEFAULT NULL
);

CREATE TABLE fact_transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    discount_applied DECIMAL(4, 2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

CREATE TABLE fact_usage_monthly (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    usage_month DATE NOT NULL,
    login_count INT NOT NULL,
    feature_breadth_score INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

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