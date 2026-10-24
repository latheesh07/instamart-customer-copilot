# 🛒 Instamart Customer Intelligence & Support Copilot

### End-to-End Data Analytics, Machine Learning & AI Support Automation

*Python · SQL · Machine Learning · NLP · TF-IDF · SQLite*

</div>

---

## 📌 Overview

The *Instamart Customer Intelligence & Support Copilot* is an end-to-end AI/ML and data science capstone project designed to analyze customer behavior, predict customer lapse, classify support tickets, and provide policy-based support assistance.

The project combines data engineering, exploratory data analysis, machine learning, natural language processing, information retrieval, and simulated customer-support automation.

### 🎯 Project Objectives

- Clean and validate customer, product, and order datasets.
- Perform exploratory data analysis and statistical analysis.
- Store structured data in an SQLite database.
- Segment customers using purchasing behavior.
- Predict customer lapse using machine learning.
- Classify and route customer-support tickets.
- Retrieve relevant policy information using TF-IDF.
- Simulate a refund-support workflow and record its results.

> *Important:* This project uses generated or simulated data and a mock language-model interface. It is not connected to a real Instamart system, and no real refund transactions are performed.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| Data Cleaning | Detect duplicate records and prepare clean datasets |
| Exploratory Data Analysis | Analyze order values, revenue, distributions, and correlations |
| SQLite Database | Store customers, products, and orders in a relational database |
| Customer Segmentation | Group customers using recency, frequency, and monetary value |
| Lapse Prediction | Train and evaluate a customer-lapse classification model |
| AI Ticket Triage | Classify customer-support tickets into relevant categories |
| Ticket Routing | Assign ticket categories and priorities |
| Policy Assistant | Retrieve policy information using TF-IDF |
| Refund Simulation | Simulate refund eligibility and record the result |
| Output Management | Save reports, predictions, logs, and model artifacts |

---

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| scikit-learn | Machine learning and TF-IDF retrieval |
| SQLite | Relational database |
| SQL | Database queries and validation |
| joblib | Saving and loading trained models |
| CSV | Datasets, predictions, and reports |
| JSON | Checkpoint and state information |
| TXT | Policy documents |
| Mock LLM | Simulated language-model responses |

---

## 🗂️ Project Structure

text
instamart-customer-copilot/
│
├── data/
│   ├── clean/
│   ├── policies/
│   ├── raw/
│   └── instamart.db
│
├── outputs/
│
├── sql/
│
├── src/
│
├── state/
│
├── .gitignore
├── README.md
├── generate_data.py
├── mock_llm.py
└── requirements.txt


### 📁 Directory Description

| Directory/File | Purpose |
|---|---|
| data/raw/ | Generated source datasets |
| data/clean/ | Cleaned datasets |
| data/policies/ | Policy documents for the support assistant |
| data/instamart.db | SQLite database |
| outputs/ | Analysis results, predictions, reports, and logs |
| sql/ | SQL queries |
| src/ | Source scripts for Parts A–D |
| state/ | Saved model and checkpoint files |
| .gitignore | Excludes unnecessary and sensitive local files |
| generate_data.py | Data-generation script |
| mock_llm.py | Mock language-model interface |
| requirements.txt | Python dependencies |

---

## 🚀 Reproduce

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.10 or later recommended
- pip package manager
- Git, or the ability to download a ZIP from GitHub

### 2. Clone the Repository

bash
git clone https://github.com/latheesh07/instamart-customer-copilot.git
cd instamart-customer-copilot


Alternatively, download the repository ZIP from GitHub and extract it.

### 3. Create a Virtual Environment

*Windows PowerShell*

powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip


### 4. Install Dependencies

powershell
py -m pip install -r requirements.txt


If the py command is unavailable, install Python and enable *Add Python to PATH* during installation.

### 5. Run the Project

Run commands from the repository root directory.

powershell
py generate_data.py
py src/validate_part_a.py
py src/customer_segmentation.py
py src/lapse_prediction.py
py src/ticket_triage.py
py src/evaluate_policy_rag.py
py src/refund_agent.py


*Execution notes:*

- Run data generation before scripts that require generated datasets.
- Some scripts depend on outputs from earlier steps.
- Confirm that each script exists in src/ before running its command.
- Run the validation and evaluation scripts to check the results.
- The refund workflow is a simulation only.

---

## 🅰️ Part A — Data Cleaning, EDA & SQL

Part A prepares the datasets, identifies duplicate orders, calculates descriptive statistics, analyzes correlations, and stores structured data in SQLite.

### Dataset Summary

| Metric | Result |
|---|---:|
| Customers | 1,200 |
| Products | 40 |
| Raw Orders | 13,084 |
| Duplicate Orders Identified | 119 |
| Cleaned Orders | 12,309 |
| Completed Orders | 11,110 |
| Cancelled Orders | 1,199 |
| Revenue from Completed Orders | ₹2,998,668.80 |

### Statistical Analysis

| Metric | Result |
|---|---:|
| Mean Order Amount | ₹269.91 |
| Median Order Amount | ₹135.00 |
| Standard Deviation | ₹432.07 |
| Skewness | 4.61 |
| First Quartile (Q1) | ₹64.80 |
| Third Quartile (Q3) | ₹297.00 |
| Upper Outlier Fence | ₹645.30 |
| Outliers Identified | 897 |

### Correlation Analysis

| Feature Pair | Correlation |
|---|---:|
| Amount vs Discount | -0.0951 |
| Amount vs Quantity | 0.0873 |
| Discount vs Quantity | -0.0004 |

The correlations are weak in this generated dataset. Correlation does not establish causation.

### Validation

| Validation Item | Recorded Result |
|---|---|
| Validation Script | src/validate_part_a.py |
| Checkpoints Passed | 26 |

---

## 🅱️ Part B — Customer Segmentation & Lapse Prediction

Part B identifies customer groups based on purchasing patterns and predicts customer lapse using a machine-learning classifier.

### Customer Segmentation

The segmentation process uses recency, frequency, and monetary-value features.

| Segment | Customers | Mean Recency | Mean Frequency | Mean Monetary Value |
|---|---:|---:|---:|---:|
| 0 | 423 | 32.78 | 3.40 | ₹1,166.53 |
| 1 | 585 | 12.02 | 16.01 | ₹4,146.37 |
| 2 | 27 | 182.26 | 0.07 | ₹1.22 |
| 3 | 165 | 110.21 | 1.86 | ₹482.22 |

Recency is measured in days in the recorded analysis. Segment numbers are model-generated labels, not rankings.

### Lapse Prediction Dataset

| Metric | Result |
|---|---|
| Historical Cutoff | 2025-09-01 |
| Prediction Window | 2025-09-01 to 2025-09-30 |
| Total Customers | 1,200 |
| Lapsed Customers | 468 |
| Training Samples | 960 |
| Test Samples | 240 |

### Model Evaluation

| Metric | Result |
|---|---:|
| Accuracy | 0.7208 |
| ROC-AUC | 0.7724 |

### Confusion Matrix

| Actual Class | Predicted Not Lapsed | Predicted Lapsed |
|---|---:|---:|
| Not Lapsed | 89 | 57 |
| Lapsed | 10 | 84 |

### Reported Outputs

| File | Purpose |
|---|---|
| outputs/customer_segments.csv | Customer segmentation results |
| outputs/customer_segment_summary.csv | Summary of customer segments |
| outputs/lapse_predictions.csv | Customer lapse predictions |
| state/lapse_model.joblib | Saved lapse prediction model |

---

## 🅲 Part C — AI Support Ticket Triage

Part C classifies support tickets, compares zero-shot and few-shot classification, and routes tickets to the relevant support category and priority.

### Classification Results

| Metric | Result |
|---|---:|
| Tickets Processed | 164 |
| Successful Classifications | 164 |
| Classification Failures | 0 |
| Zero-Shot Accuracy | 0.8293 |
| Few-Shot Accuracy | 0.9756 |

### Ticket Category Distribution

| Category | Number of Tickets |
|---|---:|
| Billing | 63 |
| Delivery | 43 |
| Technical | 33 |
| Fraud | 25 |

### Ticket Routing

| Routing Category | Number of Tickets |
|---|---:|
| Billing | 63 |
| Delivery | 43 |
| Technical | 33 |
| Trust and Safety | 25 |

### Priority Distribution

| Priority | Number of Tickets |
|---|---:|
| P1 | 63 |
| P2 | 101 |

### Token Budget

| Metric | Result |
|---|---:|
| Reported Total Tokens | 11,952 |
| Token Budget | 15,000 |
| Remaining Budget | 3,048 |
| Budget Exceeded | No |

The recorded classification comparison used 160 examples; four tickets were omitted from that comparison report.

### Reported Outputs

| File | Purpose |
|---|---|
| outputs/ticket_triage.csv | Ticket classification results |
| outputs/classification_comparison.csv | Classification method comparison |
| outputs/ticket_routing.csv | Ticket routing assignments |
| outputs/token_budget_summary.csv | Token usage summary |

---

## 🅳 Part D — Policy Assistant & Refund Simulation

Part D retrieves policy information and demonstrates a simulated refund-support workflow.

### Policy Assistant

The policy assistant uses TF-IDF to retrieve relevant policy text and a mock language-model interface to generate simulated answers.

The policy documents cover delivery, escalation, payment, privacy, and refund-related topics.

### Policy Evaluation

| Metric | Recorded Result |
|---|---:|
| Fixed Test Cases Passed | 8 |
| Total Fixed Test Cases | 8 |
| Recorded Success Rate | 100% |
| Reported Total Tokens | 781 |

Two predefined questions used deterministic answers and had a reported token count of zero.

*Evaluation limitation:* The recorded result covers only eight fixed test cases. It does not guarantee accuracy on unseen questions.

### Refund-Agent Simulation

| Metric | Recorded Result |
|---|---|
| Sample Order | ORD-111469 |
| Order Status | Completed |
| Simulated Eligible Refund | ₹45.00 |
| Real Transaction | Not Performed |

> ⚠️ *Important:* This is a simulated workflow. No real refund was issued, and the project is not connected to Instamart's real order or payment systems.

### Reported Outputs

| File | Purpose |
|---|---|
| outputs/refund_agent_log.csv | Simulated refund activity log |
| state/refund_agent_checkpoint.json | Saved agent checkpoint |

Checkpoint saving was verified in the recorded run. Full resume and recovery behavior was not tested.

---

## 📊 Overall Project Results

| Part | Main Focus | Recorded Outcome |
|---|---|---|
| Part A | Data Cleaning, EDA & SQL | 26 validation checkpoints passed |
| Part B | Customer Segmentation & Lapse Prediction | Four customer segments; ROC-AUC 0.7724 |
| Part C | AI Ticket Classification & Routing | 164 tickets processed; zero classification failures |
| Part D | Policy Retrieval & Refund Simulation | 8/8 fixed policy tests passed |

All results are from a recorded run using generated or simulated project data. Results may vary if the dataset, random seeds, dependencies, or source code change.

---

## ⚠️ Limitations

| Area | Limitation |
|---|---|
| Dataset | Generated data may not represent real customer behavior |
| Machine Learning | Performance on simulated data does not guarantee production performance |
| Segmentation | Model-generated groups require business interpretation |
| Policy Assistant | Evaluation covers only eight fixed test cases |
| Language Model | The project uses a mock interface rather than a live production API |
| Token Usage | Reported counts may differ from real API billing |
| Refund Agent | No real financial transaction is performed |
| Checkpoint Recovery | Full resume and recovery behavior has not been verified |
| Deployment | Additional testing and security controls are needed before real-world use |

---

## 🔭 Next Steps

- Add automated unit and integration tests for Parts A–D.
- Expand the policy assistant evaluation dataset.
- Evaluate the lapse model using precision, recall, F1-score, and additional validation data.
- Document dataset schemas and data-cleaning rules.
- Improve reproducibility by recording dependency versions and random seeds.
- Add data-quality monitoring and model-performance tracking.
- Build an interactive dashboard for customer and support-ticket analytics.
- Test checkpoint recovery and failure-handling scenarios.
- Add authentication, audit logs, and privacy protections before any real-world integration.
- Require human approval before any consequential action.

---

## 🔐 Privacy & Security

- Never commit passwords, API keys, access tokens, or .env files.
- Keep virtual environments and Python cache files out of the repository.
- Use .gitignore to exclude unnecessary local files.
- Treat the project datasets as generated or simulated data.
- Do not represent simulated refund decisions as real transactions.

---

## 👤 Project Information

| Detail | Information |
|---|---|
| Project Name | Instamart Customer Intelligence & Support Copilot |
| Project Type | AI/ML and Data Science Capstone |
| Repository | [instamart-customer-copilot](https://github.com/latheesh07/instamart-customer-copilot) |
| Primary Branch | main |
| Main Language | Python |
| Database | SQLite |
| Key Areas | Data Analytics, Machine Learning, NLP, Customer Support Automation |

### Core Technologies

Python · SQL · SQLite · pandas · NumPy · scikit-learn · TF-IDF · Machine Learning · NLP

---

<div align="center">

### Built as an AI/ML and Data Science Capstone Project

*Customer Analytics · Predictive Modeling · Intelligent Support Automation*

</div>
