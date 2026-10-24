[1:20 AM, 10/25/2026] Ak Latheesh😘: <div align="center">

# 🛒 Instamart Customer Intelligence & Support Copilot

### End-to-End Data Analytics, Machine Learning & AI Support Automation

*Python | SQL | Machine Learning | NLP | TF-IDF | SQLite*

</div>

---

## 📌 1. Project Overview

The *Instamart Customer Intelligence & Support Copilot* is an end-to-end AI/ML and Data Science capstone project designed to analyze customer behavior, predict customer lapse, classify support tickets, and assist customer support through policy-based information retrieval.

This project combines data engineering, exploratory data analysis, machine learning, natural language processing, and simulated support automation in one organized repository.

### 🎯 Project Objectives

- Clean and validate customer, product, and…
[1:25 AM, 10/25/2026] Ak Latheesh😘: <div align="center">

# Instamart Customer Intelligence & Support Copilot

### An End-to-End Data Analytics, Machine Learning and AI Support Project

Python | SQL | Machine Learning | NLP | SQLite | TF-IDF

</div>

---

## 1. Project Overview

The Instamart Customer Intelligence & Support Copilot is an end-to-end AI/ML and Data Science capstone project.

It analyzes customer and order data, identifies customer segments, predicts customer lapse, classifies support tickets, retrieves relevant policy information, and demonstrates a simulated refund-support workflow.

The project combines data analytics, machine learning, natural language processing, SQL, and customer-support automation.

### Project Objectives

- Clean and validate customer, product, and order d…
[1:30 AM, 10/25/2026] Ak Latheesh😘: <div align="center">

# 🛒 Instamart Customer Intelligence & Support Copilot

### 🚀 End-to-End Data Analytics, Machine Learning & AI Support Automation

*🐍 Python · 🗄️ SQL · 🤖 Machine Learning · 💬 NLP · 🧠 TF-IDF · 🗃️ SQLite*

</div>

---

## 📌 1. Project Overview

The *Instamart Customer Intelligence & Support Copilot* is an end-to-end AI/ML and Data Science capstone project designed to analyze customer behavior, predict customer lapse, classify support tickets, and assist customer support through policy-based information retrieval.

This project combines data engineering, exploratory data analysis, machine learning, natural language processing, and simulated customer-support automation.

### 🎯 Project Objectives

- 🧹 Clean and validate customer, product, and order datasets.
- 📊 Perform exploratory data analysis and statistical analysis.
- 🗄️ Store structured data in an SQLite database.
- 👥 Segment customers based on purchasing behavior.
- 🔮 Predict customer lapse using machine learning.
- 🎫 Classify customer-support tickets.
- 🚦 Route tickets by category and priority.
- 📚 Retrieve relevant policy information using TF-IDF.
- 💳 Simulate refund eligibility and record the outcome.

> ⚠️ *Important:* This project uses generated or simulated data and a mock language-model interface. It is not connected to real Instamart systems, and no real refund transactions are performed.

---

## ✨ 2. Key Features

| Feature | Description |
|---|---|
| 🧹 Data Cleaning | Detect duplicate orders and prepare cleaned datasets |
| 📊 Exploratory Data Analysis | Analyze revenue, order values, distributions, and correlations |
| 🗄️ SQLite Database | Store structured customer, product, and order data |
| 👥 Customer Segmentation | Group customers using recency, frequency, and monetary value |
| 🔮 Lapse Prediction | Predict customer lapse using a classification model |
| 🎫 AI Ticket Triage | Classify customer-support tickets |
| 🚦 Ticket Routing | Assign ticket categories and priorities |
| 📚 Policy Assistant | Retrieve policy information using TF-IDF |
| 💳 Refund Simulation | Simulate refund eligibility and record the result |
| 📁 Output Management | Save reports, predictions, logs, and model artifacts |

---

## 🧰 3. Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Main programming language |
| 🐼 pandas | Data manipulation and analysis |
| 🔢 NumPy | Numerical computations |
| 🤖 scikit-learn | Machine learning and TF-IDF retrieval |
| 🗄️ SQLite | Relational database |
| 🔍 SQL | Database queries and validation |
| 💾 joblib | Saving and loading trained models |
| 📄 CSV | Datasets, predictions, and reports |
| 🧾 JSON | Checkpoint and state information |
| 📚 TXT | Policy documents |
| 🧪 Mock LLM | Simulated language-model responses |

---

## 🗂️ 4. Project Structure

The repository is organized into data, source code, SQL queries, generated outputs, and saved model state.

### 🌳 Directory Tree

The following tree is inside a fenced code block so GitHub preserves its line breaks and indentation.

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

| Directory or File | Purpose |
|---|---|
| data/raw/ | Generated source datasets |
| data/clean/ | Cleaned datasets |
| data/policies/ | Policy documents used by the support assistant |
| data/instamart.db | SQLite database |
| outputs/ | Analysis results, predictions, reports, and logs |
| sql/ | SQL queries |
| src/ | Source code for Parts A, B, C, and D |
| state/ | Saved model and checkpoint files |
| .gitignore | Excludes unnecessary local files and secrets |
| README.md | Project documentation |
| generate_data.py | Data-generation script |
| mock_llm.py | Mock language-model interface |
| requirements.txt | Python dependencies |

---

## 🚀 5. Reproduce

Follow these steps to set up and run the project on Windows.

### 💻 5.1 Prerequisites

- Python 3.10 or later recommended
- pip package manager
- Windows PowerShell or Command Prompt

Git is optional if you download the repository as a ZIP file.

### 📥 5.2 Download the Repository

Open PowerShell and run:

powershell
git clone https://github.com/latheesh07/instamart-customer-copilot.git
cd instamart-customer-copilot


Alternatively, open the GitHub repository in your browser, download the ZIP file, extract it, and open PowerShell inside the extracted project folder.

### 🐍 5.3 Check Python Installation

powershell
py --version


If the Python launcher is installed, this command displays the Python version.

If py is not recognized, install Python and enable *Add Python to PATH* during installation. Reopen PowerShell after installation.

### 🧪 5.4 Create a Virtual Environment

Run these commands from the project root:

powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip


If PowerShell blocks virtual-environment activation, you can skip activation and use py -m pip for package installation.

### 📦 5.5 Install Dependencies

powershell
py -m pip install -r requirements.txt


This installs the packages listed in requirements.txt.

### ▶️ 5.6 Run the Project

Run commands from the repository root directory.

First, generate the data if required:

powershell
py generate_data.py


Run Part A validation:

powershell
py src/validate_part_a.py


The following commands assume the corresponding script files exist in src/:

powershell
py src/customer_segmentation.py
py src/lapse_prediction.py
py src/ticket_triage.py
py src/evaluate_policy_rag.py
py src/refund_agent.py


*Execution notes:*

- Confirm the filenames in src/ before running each command.
- Run scripts in the order required by their input files.
- Some scripts depend on datasets or outputs generated by earlier scripts.
- These commands should be adjusted if your repository uses different script names.
- The refund workflow is a simulation only.

---

## 🅰️ 6. Part A — Data Cleaning, EDA & SQL

Part A focuses on data cleaning, duplicate detection, exploratory data analysis, statistical analysis, and SQLite database preparation.

### 📊 6.1 Dataset Summary

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

### 📈 6.2 Statistical Analysis

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

### 🔗 6.3 Correlation Analysis

| Feature Pair | Correlation |
|---|---:|
| Amount vs Discount | -0.0951 |
| Amount vs Quantity | 0.0873 |
| Discount vs Quantity | -0.0004 |

These correlations are weak in the generated dataset. Correlation does not establish causation.

### ✅ 6.4 Validation Results

| Validation Item | Result |
|---|---|
| Validation Script | src/validate_part_a.py |
| Checkpoints Passed | 26 |

---

## 🅱️ 7. Part B — Customer Segmentation & Lapse Prediction

Part B analyzes customer purchasing behavior and builds a machine-learning model to predict customer lapse.

### 👥 7.1 Customer Segmentation

Customers are grouped using recency, frequency, and monetary-value features.

| Segment | Customers | Mean Recency | Mean Frequency | Mean Monetary Value |
|---|---:|---:|---:|---:|
| 0 | 423 | 32.78 | 3.40 | ₹1,166.53 |
| 1 | 585 | 12.02 | 16.01 | ₹4,146.37 |
| 2 | 27 | 182.26 | 0.07 | ₹1.22 |
| 3 | 165 | 110.21 | 1.86 | ₹482.22 |

Recency is measured in days in the recorded analysis. Segment numbers are model-generated labels, not rankings.

### 🔮 7.2 Lapse Prediction Dataset

| Metric | Result |
|---|---|
| Historical Cutoff | 2025-09-01 |
| Prediction Window | 2025-09-01 to 2025-09-30 |
| Total Customers | 1,200 |
| Lapsed Customers | 468 |
| Training Samples | 960 |
| Test Samples | 240 |

### 📏 7.3 Model Evaluation

| Metric | Result |
|---|---:|
| Accuracy | 0.7208 |
| ROC-AUC | 0.7724 |

### 🧮 7.4 Confusion Matrix

| Actual Class | Predicted Not Lapsed | Predicted Lapsed |
|---|---:|---:|
| Not Lapsed | 89 | 57 |
| Lapsed | 10 | 84 |

### 📁 7.5 Reported Outputs

| File | Purpose |
|---|---|
| outputs/customer_segments.csv | Customer segmentation results |
| outputs/customer_segment_summary.csv | Customer segment summary |
| outputs/lapse_predictions.csv | Customer lapse predictions |
| state/lapse_model.joblib | Saved lapse prediction model |

---

## 🅲 8. Part C — AI Support Ticket Triage

Part C classifies customer-support tickets, compares zero-shot and few-shot classification, and routes tickets by category and priority.

### 🎫 8.1 Classification Results

| Metric | Result |
|---|---:|
| Tickets Processed | 164 |
| Successful Classifications | 164 |
| Classification Failures | 0 |
| Zero-Shot Accuracy | 0.8293 |
| Few-Shot Accuracy | 0.9756 |

### 🏷️ 8.2 Ticket Category Distribution

| Category | Number of Tickets |
|---|---:|
| Billing | 63 |
| Delivery | 43 |
| Technical | 33 |
| Fraud | 25 |

### 🚦 8.3 Ticket Routing

| Routing Category | Number of Tickets |
|---|---:|
| Billing | 63 |
| Delivery | 43 |
| Technical | 33 |
| Trust and Safety | 25 |

### ⚡ 8.4 Priority Distribution

| Priority | Number of Tickets |
|---|---:|
| P1 | 63 |
| P2 | 101 |

### 🔢 8.5 Token Budget

| Metric | Result |
|---|---:|
| Reported Total Tokens | 11,952 |
| Token Budget | 15,000 |
| Remaining Budget | 3,048 |
| Budget Exceeded | No |

The recorded classification comparison used 160 examples; four tickets were omitted from that comparison report.

### 📁 8.6 Reported Outputs

| File | Purpose |
|---|---|
| outputs/ticket_triage.csv | Ticket classification results |
| outputs/classification_comparison.csv | Classification method comparison |
| outputs/ticket_routing.csv | Ticket routing assignments |
| outputs/token_budget_summary.csv | Token usage summary |

---

## 🅳 9. Part D — Policy Assistant & Refund Simulation

Part D retrieves policy information and demonstrates a simulated refund-support workflow.

### 📚 9.1 Policy Assistant

The policy assistant retrieves relevant policy text using TF-IDF and generates simulated answers through a mock language-model interface.

The policy documents cover delivery, escalation, payment, privacy, and refund-related topics.

### ✅ 9.2 Policy Evaluation

| Metric | Recorded Result |
|---|---:|
| Fixed Test Cases Passed | 8 |
| Total Fixed Test Cases | 8 |
| Recorded Success Rate | 100% |
| Reported Total Tokens | 781 |

Two predefined questions used deterministic answers and had a reported token count of zero.

*Evaluation limitation:* This evaluation contains only eight fixed test cases. It does not guarantee accuracy on unseen questions.

### 💳 9.3 Refund-Agent Simulation

| Metric | Recorded Result |
|---|---|
| Sample Order | ORD-111469 |
| Order Status | Completed |
| Simulated Eligible Refund | ₹45.00 |
| Real Transaction | Not Performed |

> ⚠️ *Important:* This is a simulation only. No real refund was issued. The project is not connected to real Instamart order or payment systems.

### 📁 9.4 Reported Outputs

| File | Purpose |
|---|---|
| outputs/refund_agent_log.csv | Simulated refund activity log |
| state/refund_agent_checkpoint.json | Saved agent checkpoint |

Checkpoint saving was verified in the recorded run. Full resume and recovery behavior was not tested.

---

## 🏆 10. Overall Project Results

| Part | Main Focus | Recorded Outcome |
|---|---|---|
| Part A | Data Cleaning, EDA & SQL | 26 validation checkpoints passed |
| Part B | Customer Segmentation & Lapse Prediction | Four segments; ROC-AUC 0.7724 |
| Part C | AI Ticket Classification & Routing | 164 tickets processed; zero classification failures |
| Part D | Policy Retrieval & Refund Simulation | 8 out of 8 fixed policy tests passed |

All results are from a recorded run using generated or simulated data. Results may vary if the dataset, random seeds, dependencies, or source code change.

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

## 🔭 12. Next Steps

- 🧪 Add automated unit and integration tests for Parts A–D.
- 📚 Expand the policy assistant evaluation dataset.
- 📏 Evaluate the lapse model using precision, recall, F1-score, and additional validation data.
- 📝 Document dataset schemas and data-cleaning rules.
- 🎲 Improve reproducibility by recording dependency versions and random seeds.
- 📊 Add data-quality monitoring and model-performance tracking.
- 📈 Build an interactive dashboard for customer and ticket analytics.
- 🔄 Test checkpoint recovery and failure-handling scenarios.
- 🔐 Add authentication, audit logs, and privacy protections before real-world integration.
- 👩‍💻 Require human approval before consequential actions.

---

## 🔐 13. Privacy & Security

- Never commit passwords, API keys, access tokens, or .env files.
- Keep virtual environments and Python cache files out of the repository.
- Use .gitignore to exclude unnecessary local files.
- Treat the project datasets as generated or simulated data.
- Do not represent simulated refund decisions as real transactions.

---

## 👤 14. Project Information

| Detail | Information |
|---|---|
| Project Name | Instamart Customer Intelligence & Support Copilot |
| Project Type | AI/ML and Data Science Capstone |
| Repository | [GitHub Repository](https://github.com/latheesh07/instamart-customer-copilot) |
| Primary Branch | main |
| Main Language | Python |
| Database | SQLite |
| Key Areas | Data Analytics, Machine Learning, NLP, Customer Support Automation |

### 🧩 Core Technologies

Python · SQL · SQLite · pandas · NumPy · scikit-learn · TF-IDF · Machine Learning · NLP

---

<div align="center">

### 🎓 AI/ML & Data Science Capstone Project

*📊 Customer Analytics · 🔮 Predictive Modeling · 🤖 Intelligent Support Automation*

</div>
