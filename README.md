# Instamart Customer Intelligence & Support Copilot

## Overview

Instamart Customer Intelligence & Support Copilot is an AI/ML capstone
project demonstrating a customer-data workflow across data quality, SQL
analytics, customer segmentation, lapse prediction, support-ticket
classification, policy retrieval, and a simulated refund-support agent.

The project uses project-generated data and a mock LLM interface. Refund
handling is a simulation only: it does not issue real refunds or move
money.

### Technology stack

-   Python, pandas, NumPy
-   scikit-learn and joblib
-   SQLite and SQL
-   TF-IDF retrieval
-   PowerShell and GitHub

## Reproduce

Run commands from the repository root in Windows PowerShell. Use a
supported Python 3 installation.

### 1. Create and activate a virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Run the project

Run the scripts in dependency order, from the repository root. The core
validation and analysis commands used for this project include:

``` powershell
python src/validate_part_a.py
python src/customer_segmentation.py
python src/lapse_prediction.py
python src/ticket_triage.py
python src/evaluate_policy_rag.py
```

Other Part A--D scripts are located in `src/`. Check each script's
inputs and arguments before running it; some steps rely on data,
database, output, or state files produced by earlier steps. The refund
agent is a demonstration and does not process real payments.

## Part A

### Data engineering and SQL analytics

  Measure                                          Result
  ------------------------------------ ------------------
  Raw customers                                     1,200
  Unique products                                      40
  Raw orders                                       13,084
  Exact duplicate orders identified                   119
  Cleaned orders                                   12,309
  Completed orders                                 11,110
  Cancelled orders                                  1,199
  Completed-order revenue                INR 2,998,668.80
  Mean order amount                            INR 269.91
  Median order amount                          INR 135.00
  Standard deviation of order amount           INR 432.07
  Order-amount skewness                              4.61
  First quartile (Q1)                           INR 64.80
  Third quartile (Q3)                          INR 297.00
  Upper outlier fence                          INR 645.30
  Outlier orders                                      897
  Amount--discount correlation                    -0.0951
  Amount--quantity correlation                     0.0873
  Discount--quantity correlation                  -0.0004
  Validation checkpoints passed                     26/26

Part A covers data-quality checks, duplicate detection, cleaning, SQLite
database creation, SQL/pandas revenue reconciliation, descriptive
statistics, and correlation analysis. SQL queries are stored in
`sql/queries.sql`.

## Part B

### Customer segmentation

The segmentation workflow produced **4 segments**.

  -----------------------------------------------------------------------
  Segment          Customers   Mean recency Mean frequency  Mean monetary
                                                                    value
  ----------- -------------- -------------- -------------- --------------
  0                      423          32.78           3.40   INR 1,166.53

  1                      585          12.02          16.01   INR 4,146.37

  2                       27         182.26           0.07       INR 1.22

  3                      165         110.21           1.86     INR 482.22
  -----------------------------------------------------------------------

Reported segmentation outputs: - `outputs/customer_segments.csv` -
`outputs/customer_segment_summary.csv`

### Customer lapse prediction

  Measure                                         Result
  --------------------------- --------------------------
  Historical cutoff                           2025-09-01
  Future observation window     2025-09-01 to 2025-09-30
  Customers evaluated                              1,200
  Lapsed customers                                   468
  Training rows                                      960
  Test rows                                          240
  Accuracy                                        0.7208
  ROC-AUC                                         0.7724
  Confusion matrix                `[[89, 57], [10, 84]]`

Reported prediction/model files: - `outputs/lapse_predictions.csv` -
`state/lapse_model.joblib`

## Part C

### Support-ticket classification and routing

  Measure                                        Result
  ----------------------------------- -----------------
  Tickets processed successfully                    164
  Processing failures                                 0
  Zero-shot classification accuracy     82.93% (0.8293)
  Few-shot classification accuracy      97.56% (0.9756)
  Total token usage                              11,952
  Token budget                                   15,000
  Prompt tokens                                  10,804
  Completion tokens                               1,148
  Remaining token budget                          3,048
  Budget exceeded                                    No

Ticket categories: - Billing: **63** - Delivery: **43** - Technical:
**33** - Fraud: **25**

Retry attempt counts: - 1 attempt: **124** - 2 attempts: **33** - 3
attempts: **6** - 4 attempts: **1**

Routing totals: - Billing Support: **63** - Delivery Support: **43** -
Technical Support: **33** - Trust and Safety: **25** - P1 priority:
**63** - P2 priority: **101**

The reported classification metrics used an evaluation set with support
**160**; **4** items were omitted from that metric set. Reported outputs
include `outputs/ticket_triage.csv`,
`outputs/classification_comparison.csv`, `outputs/ticket_routing.csv`,
and `outputs/token_budget_summary.csv`.

## Part D

### Policy retrieval and refund-agent simulation

The policy question-answering workflow uses TF-IDF retrieval with a mock
LLM interface.

  Measure                                       Result
  ------------------------------------------- --------
  Predefined policy evaluation cases passed        8/8
  Evaluation pass rate                            100%
  Total evaluation tokens reported                 781

The evaluation is limited to **8 predefined questions**. Two questions
use deterministic answers and report **0 tokens** for those answers;
these results do not establish general accuracy for arbitrary policy
questions.

Reported evaluation output: `outputs/policy_rag_evaluation.csv`.

The refund agent was tested with order `ORD-111469`: - Order status:
**completed** - Simulated eligible refund amount: **INR 45.00** -
Recorded message:
`SIMULATION ONLY - no real refund was issued. Eligible refund: INR 45.0 issued.`

Reported agent artifacts: - `outputs/refund_agent_log.csv` -
`state/refund_agent_checkpoint.json`

No real refund or money transfer occurred. Checkpoint saving was
verified, but full resume/recovery behavior was not fully implemented or
tested.

## Limitations

-   Results are based on the project's available data and predefined
    evaluation cases; they are not a production-performance guarantee.
-   Classification and lapse-prediction metrics need validation on
    separate, representative data.
-   The policy evaluation contains only **8** predefined questions. Two
    answers use deterministic logic rather than the mock LLM.
-   The mock LLM is not a live production language model.
-   The refund agent is a simulation and does not connect to a payment
    provider.
-   Checkpoint persistence was checked, but full resume behavior was not
    verified.
-   Production use would require additional review of privacy, security,
    data leakage, fairness, monitoring, latency, and model drift.

## Next Steps

-   Add automated tests for cleaning, SQL reconciliation, segmentation,
    lapse prediction, classification, retrieval, and refund rules.
-   Expand policy evaluation to cover more questions, edge cases,
    unsupported requests, and evidence from source policies.
-   Evaluate models on representative holdout data and monitor
    precision, recall, ROC-AUC, calibration, and drift.
-   Add auditable human approval controls for sensitive or high-value
    refund cases.
-   Implement and test reliable checkpoint resume behavior.
-   Pin dependency versions and document data provenance and
    reproducible setup.
-   Add structured logging, configuration management, and production
    deployment safeguards.

## Repository Structure

The repository follows this layout:

``` text
instamart-customer-copilot/
├── data/
│   ├── clean/
│   ├── policies/
│   ├── raw/
│   └── instamart.db
├── outputs/
├── sql/
│   └── queries.sql
├── src/
├── state/
├── .gitignore
├── README.md
├── generate_data.py
├── mock_llm.py
└── requirements.txt
```

Keep the supplied `generate_data.py` and `mock_llm.py` files unchanged.
Commit all required source files, `sql/queries.sql`, and the required
output artifacts to the single `main` branch. Do not commit virtual
environments, cache folders, credentials, API keys, or `.env` files.
