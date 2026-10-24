# 🛒 Instamart Customer Intelligence & Support Copilot

### End-to-End Data Analytics, Machine Learning & AI Support Automation

*Python | SQL | SQLite | Machine Learning | NLP | TF-IDF*

---

## 📌 1. Project Overview

The *Instamart Customer Intelligence & Support Copilot* is an AI/ML and Data Science capstone project designed to demonstrate how customer analytics, predictive modeling, natural language processing, and policy-based support workflows can work together.

The project analyzes customer and order data, identifies customer segments, predicts customer lapse, classifies support tickets, retrieves relevant policy information, and simulates a refund-support workflow.

> ⚠️ *Important:* This is an educational project that uses generated or simulated data and a mock language-model interface. It is not connected to official Instamart systems and does not perform real refund transactions.

### 🎯 Project Objectives

- Clean and validate customer, product, and order data.
- Perform exploratory data analysis (EDA).
- Store structured data in SQLite.
- Analyze order values, revenue, and statistical distributions.
- Segment customers using purchasing behavior.
- Build a customer-lapse prediction model.
- Classify and route customer-support tickets.
- Retrieve relevant policy information using TF-IDF.
- Simulate refund eligibility and record the result.
- Save reports, predictions, and model artifacts.

---

## ✨ 2. Key Features

| Feature | Description |
|---|---|
| 🧹 Data Cleaning | Detect duplicate orders and prepare cleaned data |
| 📊 Exploratory Data Analysis | Analyze revenue, order values, distributions, and correlations |
| 🗄️ SQLite Database | Store and query structured customer and order data |
| 👥 Customer Segmentation | Group customers using recency, frequency, and monetary value |
| 🔍 Lapse Prediction | Demonstrate customer-lapse classification |
| 🎫 Ticket Triage | Classify customer-support tickets |
| 🚦 Ticket Routing | Assign categories and priorities to support tickets |
| 📚 Policy Assistant | Retrieve relevant policy text using TF-IDF |
| 💳 Refund Simulation | Demonstrate refund eligibility and log simulated outcomes |
| 📁 Output Management | Save reports, predictions, and state files |

---

## 🧰 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| scikit-learn | Machine-learning models and TF-IDF retrieval |
| SQLite | Relational database |
| SQL | Database queries and validation |
| joblib | Model persistence |
| CSV | Datasets, predictions, and reports |
| JSON | Checkpoint and state information |
| TXT | Policy documents |
| Mock LLM | Simulated language-model responses |

---

## 🗂️ 4. Project Structure

text
instamart-customer-copilot/
├── data/
│   ├── clean/
│   ├── policies/
│   ├── raw/
│   └── instamart.db
├── outputs/
├── sql/
├── src/
├── state/
├── .gitignore
├── README.md
├── generate_data.py
├── mock_llm.py
└── requirements.txt


### 📁 Directory Description

| Directory / File | Purpose |
|---|---|
| data/raw/ | Generated source datasets |
| data/clean/ | Cleaned datasets |
| data/policies/ | Policy documents for the support assistant |
| data/instamart.db | SQLite database |
| outputs/ | Analysis results, predictions, reports, and logs |
| sql/ | SQL queries |
| src/ | Source code for project components |
| state/ | Saved models and checkpoint files |
| .gitignore | Excludes unnecessary local files and secrets |
| README.md | Project documentation |
| generate_data.py | Data-generation script |
| mock_llm.py | Mock language-model interface |
| requirements.txt | Python dependencies |

Note: The tree above shows the main repository structure. Individual files inside each directory may vary as the project is updated.

---

## 🚀 5. Reproduce the Project

### 5.1 Prerequisites

- Python 3.10 or later recommended
- pip package manager
- Windows PowerShell or Command Prompt

Git is optional if the repository is downloaded as a ZIP file.

### 5.2 Download the Repository

Repository:

https://github.com/latheesh07/instamart-customer-copilot

Alternatively, download the repository as a ZIP file from GitHub and extract it.

Open PowerShell inside the extracted project directory.

### 5.3 Check Python Installation

powershell
py --version


If this command is unavailable, verify that Python is installed and that the Python launcher is available.

### 5.4 Create a Virtual Environment

powershell
py -m venv .venv


Activate it using PowerShell:

powershell
.\.venv\Scripts\Activate.ps1


If activation is blocked, follow the appropriate PowerShell execution-policy guidance for your computer or use the environment's Python executable directly.

### 5.5 Install Dependencies

powershell
py -m pip install --upgrade pip
py -m pip install -r requirements.txt


### 5.6 Generate Data

From the project root:

powershell
py generate_data.py


Run this step when generated data needs to be recreated. Existing generated files may be overwritten, depending on the script.

### 5.7 Run Project Components

Run only commands whose corresponding Python files exist in src/.

The following commands reflect the recorded project scripts:

powershell
py src/validate_part_a.py
py src/customer_segmentation.py
py src/lapse_prediction.py
py src/ticket_triage.py
py src/evaluate_policy_rag.py
py src/refund_agent.py


Run the components in the order required by their input files.

> *Note:* Confirm the script filenames and dependencies in src/ before running them. The recorded results below describe a previous project run; they do not guarantee that every command will work unchanged on every computer.

---

## 📊 6. Part A — Data Cleaning, EDA & SQL

Part A focuses on data validation, duplicate detection, statistical analysis, and database preparation.

### 6.1 Dataset Summary

| Metric | Recorded Result |
|---|---:|
| Customers | 1,200 |
| Products | 40 |
| Raw Orders | 13,084 |
| Duplicate Orders Identified | 119 |
| Cleaned Orders | 12,309 |
| Completed Orders | 11,110 |
| Cancelled Orders | 1,199 |
| Revenue from Completed Orders | ₹2,998,668.80 |

### 6.2 Statistical Analysis

| Metric | Recorded Result |
|---|---:|
| Mean Order Amount | ₹269.91 |
| Median Order Amount | ₹135.00 |
| Standard Deviation | ₹432.07 |
| Skewness | 4.61 |
| First Quartile (Q1) | ₹64.80 |
| Third Quartile (Q3) | ₹297.00 |
| Upper Outlier Fence | ₹645.30 |
| Outliers Identified | 897 |

### 6.3 Correlation Analysis

| Feature Pair | Correlation |
|---|---:|
| Amount vs. Discount | -0.0951 |
| Amount vs. Quantity | 0.0873 |
| Discount vs. Quantity | -0.0004 |

These recorded correlations are weak. Correlation does not establish causation.

### 6.4 Validation

| Validation Item | Recorded Result |
|---|---:|
| Validation Script | src/validate_part_a.py |
| Checkpoints Passed | 26 |

### 📁 Main Output

- Cleaned datasets
- SQLite database
- SQL query results and validation outputs

---

## 👥 7. Part B — Customer Segmentation & Lapse Prediction

Part B analyzes customer purchasing behavior and demonstrates machine-learning-based lapse prediction.

### 7.1 Customer Segmentation

Customers are grouped using recency, frequency, and monetary-value features.

| Segment | Customers | Mean Recency (Days) | Mean Frequency | Mean Monetary Value |
|---|---:|---:|---:|---:|
| 0 | 423 | 32.78 | 3.40 | ₹1,166.53 |
| 1 | 585 | 12.02 | 16.01 | ₹4,146.37 |
| 2 | 27 | 182.26 | 0.07 | ₹1.22 |
| 3 | 165 | 110.21 | 1.86 | ₹482.22 |

Segment identifiers are model-generated labels, not rankings.

### 7.2 Lapse Prediction Dataset

| Metric | Recorded Result |
|---|---|
| Historical Cutoff | 2025-09-01 |
| Prediction Window | 2025-09-01 to 2025-09-30 |
| Total Customers | 1,200 |
| Lapsed Customers | 468 |
| Training Samples | 960 |
| Test Samples | 240 |

### 7.3 Model Evaluation

| Metric | Recorded Result |
|---|---:|
| Accuracy | 0.7208 |
| ROC-AUC | 0.7724 |

### 7.4 Confusion Matrix

| Actual Class | Predicted Not Lapsed | Predicted Lapsed |
|---|---:|---:|
| Not Lapsed | 89 | 57 |
| Lapsed | 10 | 84 |

### 7.5 Reported Outputs

| File | Purpose |
|---|---|
| outputs/customer_segments.csv | Customer segmentation results |
| outputs/customer_segment_summary.csv | Segment summary |
| outputs/lapse_predictions.csv | Lapse predictions |
| state/lapse_model.joblib | Saved prediction model |

---

## 🎫 8. Part C — AI Support Ticket Triage

Part C demonstrates ticket classification, comparison of zero-shot and few-shot methods, and support-ticket routing.

### 8.1 Classification Results

| Metric | Recorded Result |
|---|---:|
| Tickets Processed | 164 |
| Successful Classifications | 164 |
| Classification Failures | 0 |
| Zero-Shot Accuracy | 0.8293 |
| Few-Shot Accuracy | 0.9756 |

### 8.2 Ticket Category Distribution

| Category | Number of Tickets |
|---|---:|
| Billing | 63 |
| Delivery | 43 |
| Technical | 33 |
| Fraud | 25 |
| *Total* | *164* |

### 8.3 Ticket Routing

| Routing Category | Number of Tickets |
|---|---:|
| Billing | 63 |
| Delivery | 43 |
| Technical | 33 |
| Trust and Safety | 25 |
| *Total* | *164* |

### 8.4 Priority Distribution

| Priority | Number of Tickets |
|---|---:|
| P1 | 63 |
| P2 | 101 |
| *Total* | *164* |

### 8.5 Token Budget

| Metric | Recorded Result |
|---|---:|
| Reported Total Tokens | 11,952 |
| Token Budget | 15,000 |
| Remaining Budget | 3,048 |
| Budget Exceeded | No |

The recorded classification comparison used 160 examples; four tickets were omitted from that comparison report.

### 8.6 Reported Outputs

| File | Purpose |
|---|---|
| outputs/ticket_triage.csv | Ticket classification results |
| outputs/classification_comparison.csv | Classification method comparison |
| outputs/ticket_routing.csv | Ticket routing assignments |
| outputs/token_budget_summary.csv | Token usage summary |

---

## 📚 9. Part D — Policy Assistant & Refund Simulation

Part D demonstrates policy retrieval and a simulated refund-support workflow.

### 9.1 Policy Assistant

The policy assistant retrieves relevant policy text using TF-IDF and generates simulated responses through a mock language-model interface.

The policy documents cover topics including:

- Delivery
- Escalation
- Payment
- Privacy
- Refunds

### 9.2 Policy Evaluation

| Metric | Recorded Result |
|---|---:|
| Fixed Test Cases Passed | 8 |
| Total Fixed Test Cases | 8 |
| Recorded Success Rate | 100% |
| Reported Total Tokens | 781 |

Two predefined questions used deterministic answers and had a reported token count of zero.

The evaluation contains only eight fixed test cases. It does not guarantee accuracy on unseen questions.

### 9.3 Refund-Agent Simulation

| Metric | Recorded Result |
|---|---|
| Sample Order | ORD-111469 |
| Order Status | Completed |
| Simulated Eligible Refund | ₹45.00 |
| Real Transaction | Not Performed |

> ⚠️ *Simulation only:* No real refund was issued. The project is not connected to actual Instamart orders or payment systems.

### 9.4 Reported Outputs

| File | Purpose |
|---|---|
| outputs/refund_agent_log.csv | Simulated refund activity log |
| state/refund_agent_checkpoint.json | Saved agent checkpoint |

Checkpoint saving was verified in the recorded run. Full resume and recovery behavior was not tested.

---

## 📈 10. Overall Project Results

| Part | Main Focus | Recorded Outcome |
|---|---|---|
| Part A | Data Cleaning, EDA & SQL | 26 validation checkpoints passed |
| Part B | Customer Segmentation & Lapse Prediction | Four segments; ROC-AUC 0.7724 |
| Part C | Ticket Classification & Routing | 164 tickets processed; zero classification failures |
| Part D | Policy Retrieval & Refund Simulation | 8 of 8 fixed policy tests passed |

All figures represent recorded results using generated or simulated data. Results may vary if the dataset, random seeds, dependencies, or source code change.

---

## ⚠️ 11. Limitations

| Area | Limitation |
|---|---|
| Dataset | Generated data may not represent real customer behavior |
| Machine Learning | Results on simulated data do not guarantee production performance |
| Segmentation | Model-generated groups require business interpretation |
| Policy Assistant | Evaluation covers only eight fixed test cases |
| Language Model | Uses a mock interface rather than a live production API |
| Token Usage | Reported counts may differ from real API billing |
| Refund Agent | Does not perform real financial transactions |
| Checkpoint Recovery | Full resume and recovery behavior has not been verified |
| Deployment | Additional testing and security controls are needed |

---

## 🚀 12. Next Steps

- Add automated unit and integration tests for all project components.
- Expand the policy assistant evaluation dataset.
- Evaluate lapse prediction with precision, recall, F1-score, and additional validation data.
- Document dataset schemas and data-cleaning rules.
- Record dependency versions and random seeds for reproducibility.
- Add data-quality monitoring and model-performance tracking.
- Improve the interactive dashboard for customer and ticket analytics.
- Test checkpoint recovery and failure-handling scenarios.
- Add authentication, audit logs, and privacy protections before any real-world integration.
- Require human approval before consequential actions.

---

## 🔐 13. Privacy & Security

- Never commit passwords, API keys, access tokens, or .env files.
- Keep virtual environments and Python cache files out of the repository.
- Use .gitignore to exclude unnecessary local files.
- Treat project datasets as generated or simulated data.
- Never represent simulated refund decisions as real transactions.
- Review repository contents before making the project public.

---

## ℹ️ 14. Project Information

| Detail | Information |
|---|---|
| Project Name | Instamart Customer Intelligence & Support Copilot |
| Project Type | AI/ML and Data Science Capstone |
| Repository | [GitHub Repository](https://github.com/latheesh07/instamart-customer-copilot) |
| Primary Branch | main |
| Main Language | Python |
| Database | SQLite |
| Key Areas | Data Analytics, Machine Learning, NLP, Customer Support Automation |

### 🧑‍💻 Core Technologies

Python · SQL · SQLite · pandas · NumPy · scikit-learn · TF-IDF · Machine Learning · NLP

---

### 🎓 Built as an AI/ML & Data Science Capstone Project

*Customer Analytics | Predictive Modeling | Intelligent Support Automation*
