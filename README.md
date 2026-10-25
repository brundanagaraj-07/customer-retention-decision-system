# 🛡️ RevGuard: Customer Value & Retention Decision System

**RevGuard** is an end-to-end, production-grade machine learning and data analytics platform designed to proactively identify customer churn risks, compute customer lifetime value metrics, and empower retention teams with real-time decision intelligence.

The system integrates a relational database architecture, automated feature engineering pipelines, class-balanced machine learning models, a lightweight FastAPI backend service, and an interactive Streamlit dashboard.

---

## Executive Summary & Architecture

Modern subscription and SaaS businesses face revenue leakage due to unmitigated churn. RevGuard bridges raw transactional data with actionable operational workflows through a 5-tier modular pipeline:

```text
[ MySQL Database & Views ] ──► [ Data Loader (data_loader.py) ]
                                            │
                                            ▼
[ Interactive Dashboard ] ◄── [ API Service ] ◄── [ ML Pipeline ]
   (Streamlit + Plotly)        (FastAPI)         (Scikit-Learn)
```

1. **Analytical Data Layer (MySQL):** Standardized database views extracting RFM metrics, engagement friction, and monthly revenue trends.
2. **Data Pipeline & Preprocessing:** Handles dynamic schema loads, missing value imputations, variable scaling, and feature encoding.
3. **Machine Learning Core:** Class-weighted Random Forest Classifier predicting granular customer churn probabilities.
4. **REST API Service:** FastAPI backend delivering low-latency inference endpoints and risk tier classifications.
5. **Executive Decision Dashboard:** Streamlit UI displaying portfolio risk distributions, prioritized high-risk customer tables, and real-time scenario simulation capabilities.

---

## 🛠️ Tech Stack

* **Database & ORM:** MySQL 8.0+, SQLAlchemy, PyMySQL
* **Data Processing & Feature Engineering:** Python 3.10+, Pandas, NumPy
* **Machine Learning Engine:** Scikit-Learn (Random Forest Classifier), Joblib
* **API Service Framework:** FastAPI, Uvicorn, Pydantic
* **Visualization & Frontend:** Streamlit, Plotly Express
* **Environment & Security:** Python-Dotenv, Git

---

## 📁 Repository Directory Structure

```text
revguard-retention-system/
├── data/                       # Local dataset dumps and SQL scripts
├── models/                     # Trained ML model artifacts (.pkl)
│   └── churn_model.pkl
├── src/                        # Core source code modules
│   ├── __init__.py
│   ├── api.py                  # FastAPI server & route handlers
│   ├── dashboard.py            # Streamlit executive UI app
│   ├── data_loader.py          # SQLAlchemy database connection engine
│   ├── feature_engineering.py  # Feature transformations & ratio pipelines
│   ├── predict.py              # Single/batch inference utilities
│   └── train_model.py          # ML training & evaluation script
├── .env.example                # Template for environment variables
├── .gitignore                  # Git tracking exclusions
├── README.md                   # Complete system documentation
└── requirements.txt            # Python dependency definitions
```

---

## 🗄️ Database Architecture & Analytical Views

RevGuard transforms transactional tables into three specialized analytical database views:

1. **`vw_customer_rfm`**: Calculates **Recency** (days since last active session), **Frequency** (total transactions), and **Monetary Value** (total spend).
2. **`vw_customer_value_friction`**: Quantifies product usage intensity and operational friction by merging `avg_monthly_logins`, `total_support_tickets`, and `avg_resolution_time_hours`.
3. **`vw_cohort_monthly_revenue`**: Tracks customer retention cohorts and monthly recurring revenue (MRR) performance over time.

---

## ⚙️ Feature Engineering & Modeling Strategy

### Feature Transformations

* **Support-to-Login Ratio**: Evaluates operational friction relative to platform usage intensity:
  ```text
  Friction Ratio = total_support_tickets / (avg_monthly_logins + 1)
  ```
* **Tier Encoding**: Categorical attributes (`subscription_tier`) are transformed via One-Hot Encoding.
* **Missing Value Imputation**: Zero-filling missing engagement records for inactive users.

### Machine Learning Pipeline

* **Algorithm**: Random Forest Classifier (150 estimators, max depth 10).
* **Class Weighting**: `balanced` setting to handle churn class imbalances without synthetic data leakage.
* **Evaluation Metrics**: Stratified train-test splits (80 / 20) evaluated via **ROC-AUC** and precision-recall metrics.

---

## 🔌 API Serving (FastAPI) & Risk Tier Logic

The FastAPI service exposes a REST endpoint (`POST /predict-churn`) to return real-time predictions and automated retention recommendations.

### Decision Matrix

| Risk Tier | Churn Probability ($P$) | Automated Action Strategy |
| :--- | :--- | :--- |
| 🟢 **Low Risk** | $0.00 \le P \le 0.30$ | Standard automated engagement and feature updates |
| 🟡 **Medium Risk** | $0.30 < P \le 0.70$ | Targeted feature nudges and proactive support outreach |
| 🔴 **High Risk** | $0.70 < P \le 1.00$ | **Immediate priority intervention** (Custom discounts, CSM call) |

---

##  Streamlit Executive Dashboard

The interactive UI (`src/dashboard.py`) contains two primary modules:

1. **Portfolio Risk Analytics**: High-level metrics showing aggregate portfolio health, pie chart visualizations of risk tiers, and exportable tables of high-risk customers requiring intervention.
2. **Live Customer Simulator**: Slider-based tool enabling product managers to tweak customer usage parameters and compute instant churn probabilities.

---

## 🚀 Setup & Installation Instructions

### 1. Clone Repository & Setup Environment

```bash
git clone https://github.com/your-username/revguard-retention-system.git
cd revguard-retention-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=revguard_db
DB_USER=root
DB_PASSWORD=YourSecurePassword123!
```

### 3. Run Pipeline Execution Sequence

1. **Train Model Artifact:**
   ```bash
   python src/train_model.py
   ```

2. **Launch FastAPI Backend:**
   ```bash
   uvicorn src.api:app --reload
   ```
   * *Swagger Documentation:* Navigate to `http://127.0.0.1:8000/docs`

3. **Launch Streamlit Dashboard:**
   ```bash
   streamlit run src/dashboard.py
   ```
   * *Dashboard UI:* Opens automatically at `http://localhost:8501`

---

## 📄 License

Distributed under the **MIT License**.
