from pathlib import Path

import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
ORDERS_PATH = ROOT / "data" / "clean" / "orders.csv"
CUSTOMERS_PATH = ROOT / "data" / "clean" / "customers.csv"
OUTPUT_DIR = ROOT / "outputs"
MODEL_DIR = ROOT / "state"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    orders = pd.read_csv(ORDERS_PATH)
    customers = pd.read_csv(CUSTOMERS_PATH)

    orders["order_ts"] = pd.to_datetime(
        orders["order_ts"], errors="coerce"
    )
    orders["order_amount"] = pd.to_numeric(
        orders["order_amount"], errors="coerce"
    )

    completed = orders.loc[
        (orders["status"] == "completed")
        & orders["order_ts"].notna()
    ].copy()

    if completed.empty:
        raise ValueError("No completed orders available.")

    # Use the last 30 days as the future outcome window.
    last_date = completed["order_ts"].max().normalize()
    outcome_start = last_date - pd.Timedelta(days=29)
    cutoff_date = outcome_start

    # Historical features use only orders strictly before the cutoff.
    history = completed.loc[
        completed["order_ts"] < cutoff_date
    ].copy()

    future = completed.loc[
        completed["order_ts"] >= cutoff_date
    ].copy()

    if history.empty or future.empty:
        raise ValueError(
            "Insufficient history or future orders for a time-based label."
        )

    features = history.groupby("customer_id").agg(
        frequency=("order_id", "nunique"),
        monetary=("order_amount", "sum"),
        average_order_value=("order_amount", "mean"),
        last_order_date=("order_ts", "max"),
    )

    reference_date = cutoff_date
    features["recency_days"] = (
        reference_date - features["last_order_date"]
    ).dt.days
    features = features.drop(columns=["last_order_date"])

    dataset = customers[["customer_id"]].merge(
        features.reset_index(),
        on="customer_id",
        how="left",
    )

    dataset["frequency"] = dataset["frequency"].fillna(0)
    dataset["monetary"] = dataset["monetary"].fillna(0)
    dataset["average_order_value"] = (
        dataset["average_order_value"].fillna(0)
    )

    # Customers without historical orders receive a large recency value.
    dataset["recency_days"] = dataset["recency_days"].fillna(
        (cutoff_date - completed["order_ts"].min()).days + 1
    )

    # Label = 1 if customer made no completed purchase in the future window.
    future_customer_ids = set(future["customer_id"].unique())
    dataset["lapsed"] = (
        ~dataset["customer_id"].isin(future_customer_ids)
    ).astype(int)

    feature_columns = [
        "frequency",
        "monetary",
        "average_order_value",
        "recency_days",
    ]

    X = dataset[feature_columns]
    y = dataset["lapsed"]

    if y.nunique() < 2:
        raise ValueError(
            "The future-window label contains only one class. "
            "Cannot train a binary classifier."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    print(f"Historical feature cutoff: {cutoff_date.date()}")
    print(
        f"Future outcome window: {outcome_start.date()} "
        f"to {last_date.date()}"
    )
    print(f"Customers: {len(dataset)}")
    print(f"Lapsed customers (no future purchase): {int(y.sum())}")
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, probabilities):.4f}")

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, predictions))

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    dataset["lapse_probability"] = pipeline.predict_proba(X)[:, 1]

    predictions_path = OUTPUT_DIR / "lapse_predictions.csv"
    dataset.to_csv(predictions_path, index=False)

    model_path = MODEL_DIR / "lapse_model.joblib"
    joblib.dump(pipeline, model_path)

    print(f"\nSaved predictions: {predictions_path}")
    print(f"Saved model: {model_path}")


if __name__ == "__main__":
    main()