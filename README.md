🛡️ RevGuard: Customer Value & Retention Decision SystemRevGuard is an end-to-end, production-grade machine learning and data analytics platform designed to proactively identify customer churn risks, compute customer lifetime value metrics, and empower retention teams with real-time decision intelligence.The system integrates a relational database architecture, automated feature engineering pipelines, class-balanced machine learning models, a lightweight FastAPI backend service, and an interactive Streamlit dashboard.📌 Executive Summary & ArchitectureModern subscription and SaaS businesses face revenue leakage due to unmitigated churn. RevGuard bridges raw transactional data with actionable operational workflows through a 5-tier modular pipeline:[ MySQL Database & Views ] ──► [ Data Loader (data_loader.py) ]
                                            │
                                            ▼
[ Interactive Dashboard ] ◄── [ API Service ] ◄── [ ML Pipeline ]
   (Streamlit + Plotly)        (FastAPI)         (Scikit-Learn)
Analytical Data Layer (MySQL): Standardized database views extracting RFM metrics, engagement friction, and monthly revenue trends.Data Pipeline & Preprocessing: Handles dynamic schema loads, missing value imputations, variable scaling, and feature encoding.Machine Learning Core: Class-weighted Random Forest Classifier predicting granular customer churn probabilities.REST API Service: FastAPI backend delivering low-latency inference endpoints and risk tier classifications.Executive Decision Dashboard: Streamlit UI displaying portfolio risk distributions, prioritized high-risk customer tables, and real-time scenario simulation capabilities.🛠️ Tech StackDatabase & ORM: MySQL 8.0+, SQLAlchemy, PyMySQLData Processing & Feature Engineering: Python 3.10+, Pandas, NumPyMachine Learning Engine: Scikit-Learn (Random Forest Classifier), JoblibAPI Service Framework: FastAPI, Uvicorn, PydanticVisualization & Frontend: Streamlit, Plotly ExpressEnvironment & Security: Python-Dotenv, Git📁 Repository Directory Structurerevguard-retention-system/
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
🗄️ Database Architecture & Analytical ViewsRevGuard transforms transactional tables into three specialized analytical database views:vw_customer_rfm:Calculates Recency (days since last active session), Frequency (total transactions), and Monetary Value (total spend).vw_customer_value_friction:Quantifies product usage intensity and operational friction by merging avg_monthly_logins, total_support_tickets, and avg_resolution_time_hours.vw_cohort_monthly_revenue:Tracks customer retention cohorts and monthly recurring revenue (MRR) performance over time.⚙️ Feature Engineering & Modeling StrategyFeature TransformationsSupport-to-Login Ratio: Evaluates friction relative to usage intensity:
$$\text{Friction Ratio} = \frac{\text{total\_support\_tickets}}{\text{avg\_monthly\_logins} + 1}$$Tier Encoding: Categorical attributes (subscription_tier) are transformed via One-Hot Encoding.Missing Value Imputation: Zero-filling missing engagement records for inactive users.Machine Learning PipelineAlgorithm: Random Forest Classifier ($150$ estimators, max depth $10$).Class Weighting: balanced setting to handle churn class imbalances without synthetic data leakage.Evaluation Metrics: Stratified train-test splits ($80/20$) evaluated via ROC-AUC and precision-recall metrics.🔌 API Serving (FastAPI) & Risk Tier LogicThe FastAPI service exposes a REST endpoint (POST /predict-churn) to return real-time predictions and automated retention recommendations.Decision MatrixRisk TierChurn Probability (P)Automated Action Strategy🟢 Low Risk$0.00 \le P \le 0.30$Standard automated engagement and feature updates🟡 Medium Risk$0.30 < P \le 0.70$Targeted feature nudges and proactive support outreach🔴 High Risk$0.70 < P \le 1.00$Immediate priority intervention (Custom discounts, CSM call)🖥️ Streamlit Executive DashboardThe interactive UI (src/dashboard.py) contains two primary modules:Portfolio Risk Analytics: High-level metrics showing aggregate portfolio health, pie chart visualizations of risk tiers, and exportable tables of high-risk customers requiring intervention.Live Customer Simulator: Slider-based tool enabling product managers to tweak customer usage parameters and compute instant churn probabilities.🚀 Setup & Installation Instructions1. Clone Repository & Setup Environmentgit clone https://github.com/your-username/revguard-retention-system.git
cd revguard-retention-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2. Configure Environment VariablesCreate a .env file in the project root based on .env.example:DB_HOST=localhost
DB_PORT=3306
DB_NAME=revguard_db
DB_USER=root
DB_PASSWORD=YourSecurePassword123!
3. Run Pipeline Execution SequenceTrain Model Artifact:python src/train_model.py
Launch FastAPI Backend:uvicorn src.api:app --reload
Swagger Documentation: Navigate to http://127.0.0.1:8000/docsLaunch Streamlit Dashboard:streamlit run src/dashboard.py
Dashboard UI: Opens automatically at http://localhost:8501📄 LicenseDistributed under the MIT License. See LICENSE for more details.
