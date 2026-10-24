\# Instamart Customer Intelligence \& Support Copilot



\## Project Overview



Instamart Customer Intelligence \& Support Copilot is an AI/ML-based

customer intelligence and support automation capstone project.



The project combines data cleaning, SQL analytics, customer

segmentation, customer lapse prediction, AI-based ticket classification,

policy retrieval, and a simulated refund-support agent.



\## Key Features



\### Part A: Data Engineering and SQL Analytics

\- Data quality auditing and cleaning

\- Duplicate order detection

\- Customer and product data validation

\- SQLite database creation

\- Revenue reconciliation using SQL and pandas

\- Order statistics and correlation analysis



\### Part B: Customer Intelligence

\- Customer segmentation using machine learning

\- Customer lapse prediction

\- Model evaluation using accuracy, ROC-AUC, and a confusion matrix



\### Part C: AI Customer Support

\- Customer ticket classification

\- Zero-shot and few-shot classification comparison

\- Retry handling for simulated LLM failures

\- Ticket routing and priority assignment

\- Token usage tracking



\### Part D: Policy RAG and Refund Agent

\- TF-IDF-based policy retrieval

\- Policy question answering

\- Policy evaluation tests

\- Simulated refund eligibility checks

\- Agent logs and checkpoint files



\## Technologies Used



\- Python

\- Pandas

\- NumPy

\- Scikit-learn

\- SQLite

\- Joblib

\- TF-IDF

\- PowerShell

\- Git and GitHub



\## Project Results



\- Raw orders processed: 13,084

\- Clean orders: 12,309

\- Clean customers: 1,200

\- Unique products: 40

\- Completed-order revenue: INR 2,998,668.80

\- Part A validation: 26/26 checkpoints passed

\- Zero-shot ticket classification accuracy: 82.93%

\- Few-shot ticket classification accuracy: 97.56%

\- Policy RAG evaluation: 8/8 test cases passed

\- Customer lapse prediction ROC-AUC: 0.7724



Note: Classification and RAG results apply to the project's evaluation

datasets. Further testing is required before production deployment.



\## Project Structure



```text

instamart-customer-copilot/

├── data/

│   ├── raw/

│   ├── clean/

│   ├── policies/

│   └── instamart.db

├── outputs/

├── sql/

├── src/

├── state/

├── mock\_llm.py

├── generate\_data.py

├── requirements.txt

├── .gitignore

└── README.md

