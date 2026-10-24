<div align="center">

# 🛒 Instamart Customer Intelligence & Support Copilot

### An End-to-End AI/ML, Data Analytics & Customer Support Automation Project

*Python | SQL | Machine Learning | NLP | TF-IDF | SQLite*

</div>

---

## 📌 Overview

The *Instamart Customer Intelligence & Support Copilot* is an end-to-end data science and AI/ML capstone project designed to analyze customer behavior, predict customer lapse, classify support tickets, and assist customer support using policy-based information retrieval.

The project combines data analytics, machine learning, natural language processing, and simulated support automation in a single reproducible workflow.

> *Note:* This project uses generated or simulated data and a mock language-model interface. It is not connected to real Instamart systems.

## ✨ Key Features

- 🧹 Data cleaning and quality validation
- 📊 Exploratory data analysis and SQL queries
- 👥 Customer segmentation using purchasing behavior
- 🤖 Customer lapse prediction
- 🎫 AI-powered support ticket classification
- 🚦 Ticket routing and priority assignment
- 📚 Policy retrieval using TF-IDF
- 💰 Simulated refund eligibility workflow
- 📁 Structured outputs, model files, and logs

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| pandas | Data processing and analysis |
| NumPy | Numerical operations |
| scikit-learn | Machine learning and TF-IDF |
| SQLite | Relational database |
| SQL | Data querying and validation |
| joblib | Model persistence |
| CSV / JSON / TXT | Data, reports, logs, and policies |

## 🗂️ Project Structure

```text
instamart-customer-copilot/
│
├── data/
│   ├── clean/
│   ├── policies/
│   ├── raw/
│   └── instamart.db
│
├── outputs/
├── sql/
├── src/
├── state/
│
├── .gitignore
├── README.md
├── generate_data.py
├── mock_llm.py
└── requirements.txt

🚀 Reproduce
1. Clone the repository
git clone https://github.com/latheesh07/instamart-customer-copilot.git
cd instamart-customer-copilot
Alternatively, download the repository as a ZIP file from GitHub.
2. Install dependencies
Make sure Python is installed.
On Windows PowerShell:
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
If py is unavailable, install Python and reopen the terminal.
3. Run the project
Run commands from the project root directory. Start with data generation and then execute the relevant scripts in src/.
py generate_data.py
py src/validate_part_a.py
py src/customer_segmentation.py
py src/lapse_prediction.py
py src/ticket_triage.py
py src/evaluate_policy_rag.py
py src/refund_agent.py
The exact order and required inputs may depend on the scripts in the repository. The refund workflow is a simulation only.
🅰️ Part A — Data Cleaning, EDA & SQL
This module cleans generated datasets, identifies duplicate orders, calculates descriptive statistics, and stores data in SQLite.
Dataset Summary
Metric
Result
Customers
1,200
Products
40
Raw orders
13,084
Duplicate orders identified
119
Cleaned orders
12,309
Completed orders
11,110
Cancelled orders
1,199
Completed-order revenue
₹2,998,668.80
Statistical Analysis
Metric
Result
Mean order amount
₹269.91
Median order amount
₹135.00
Standard deviation
₹432.07
Skewness
4.61
First quartile (Q1)
₹64.80
Third quartile (Q3)
₹297.00
Upper outlier fence
₹645.30
Outliers identified
897
Correlation Analysis
Feature Pair
Correlation
Amount vs Discount
-0.0951
Amount vs Quantity
0.0873
Discount vs Quantity
-0.0004
Validation result: 26 checkpoints passed in the recorded run.
🅱️ Part B — Customer Segmentation & Lapse Prediction
Customer Segmentation
Customers are grouped using recency, frequency, and monetary-value features.
Segment
Customers
Mean Recency
Mean Frequency
Mean Monetary Value
0
423
32.78
3.40
₹1,166.53
1
585
12.02
16.01
₹4,146.37
2
27
182.26
0.07
₹1.22
3
165
110.21
1.86
₹482.22
Lapse Prediction
The classification model predicts customer lapse over a defined future window.
Metric
Result
Historical cutoff
2025-09-01
Prediction window
2025-09-01 to 2025-09-30
Customers evaluated
1,200
Lapsed customers
468
Training samples
960
Test samples
240
Accuracy
0.7208
ROC-AUC
0.7724
Confusion Matrix
                 Predicted
                 Not Lapsed   Lapsed
Actual Not Lapsed     89        57
Actual Lapsed         10        84
Reported outputs include customer segment files, lapse predictions, and the saved model.
🅲 Part C — AI Support Ticket Triage
This module classifies support tickets, compares zero-shot and few-shot classification, and routes tickets to the appropriate category.
Classification Results
Metric
Result
Tickets processed
164
Successful classifications
164
Classification failures
0
Zero-shot accuracy
0.8293
Few-shot accuracy
0.9756
Ticket Categories
Category
Count
Billing
63
Delivery
43
Technical
33
Fraud
25
Token Budget
Metric
Result
Total reported tokens
11,952
Token budget
15,000
Remaining budget
3,048
Budget exceeded
No
The recorded classification comparison used 160 examples; four tickets were omitted from that comparison report.
🅳 Part D — Policy Assistant & Refund Simulation
Policy Assistant
The policy assistant retrieves relevant text from policy documents using TF-IDF and produces simulated responses through a mock language-model interface.
Evaluation Metric
Result
Fixed test cases passed
8/8
Reported success rate
100%
Reported total tokens
781
This evaluation uses eight fixed test cases and does not guarantee accuracy on unseen questions.
Refund Simulation
The refund agent checks a sample order and records a simulated refund decision.
Metric
Recorded Result
Sample order
ORD-111469
Order status
Completed
Simulated eligible refund
₹45.00
⚠️ No real refund was issued. This is a simulated workflow and is not connected to a payment system.
The checkpoint file was saved in the recorded run, but full resume/recovery behavior was not tested.
📊 Overall Results
Part
Main Outcome
Part A
Data cleaning, EDA, SQLite, and 26 validation checks passed
Part B
Four customer segments and lapse prediction model
Part C
164 tickets processed with zero classification failures
Part D
Eight fixed policy tests passed and refund workflow simulated
These metrics are from a recorded run on generated or simulated data. Results may vary if the data, random seeds, dependencies, or code change.
⚠️ Limitations
The datasets are generated and may not represent real customer behavior.
Model results on simulated data do not establish production performance.
Policy retrieval was evaluated on only eight fixed test cases.
The mock language-model interface is not a live production API.
Token counts are project-reported and may differ from real model billing.
The refund workflow does not execute real financial transactions.
Full checkpoint recovery has not been verified.
Customer segments require business interpretation before real-world use.
🔭 Next Steps
Expand the evaluation dataset with more diverse test cases.
Add automated tests for every project module.
Improve model evaluation with precision, recall, and F1-score.
Add data-quality monitoring and a documented data dictionary.
Improve reproducibility by recording dependency versions and random seeds.
Build an interactive dashboard for customer and ticket insights.
Add privacy controls, audit logs, and human approval before any real-world action.
🔐 Privacy & Security
Never commit passwords, API keys, or .env files.
Keep virtual environments and Python cache files out of the repository.
Treat all project data as simulated data.
Do not represent simulated refund results as real transactions.
�

Built as an AI/ML and Data Science Capstone Project
Python · SQL · Machine Learning · NLP · Customer Analytics
�
```
