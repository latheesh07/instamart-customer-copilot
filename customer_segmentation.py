from pathlib import Path

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent

ORDERS_PATH = ROOT / "data" / "clean" / "orders.csv"
CUSTOMERS_PATH = ROOT / "data" / "clean" / "customers.csv"
OUTPUT_DIR = ROOT / "outputs"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not ORDERS_PATH.exists():
        raise FileNotFoundError(f"Missing file: {ORDERS_PATH}")

    if not CUSTOMERS_PATH.exists():
        raise FileNotFoundError(f"Missing file: {CUSTOMERS_PATH}")

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
        & orders["order_amount"].notna()
    ].copy()

    if completed.empty:
        raise ValueError("No valid completed orders found.")

    # Reference date: one day after the latest completed order.
    reference_date = (
        completed["order_ts"].max().normalize()
        + pd.Timedelta(days=1)
    )

    # Build RFM features.
    rfm = completed.groupby("customer_id").agg(
        last_order_date=("order_ts", "max"),
        frequency=("order_id", "nunique"),
        monetary=("order_amount", "sum"),
    )

    rfm["recency"] = (
        reference_date - rfm["last_order_date"]
    ).dt.days

    rfm = rfm[
        ["recency", "frequency", "monetary"]
    ].reset_index()

    # Include customers who have no completed orders.
    rfm = customers[["customer_id"]].merge(
        rfm, on="customer_id", how="left"
    )

    rfm["frequency"] = rfm["frequency"].fillna(0)
    rfm["monetary"] = rfm["monetary"].fillna(0)
    rfm["recency"] = rfm["recency"].fillna(
        (reference_date - completed["order_ts"].min()).days + 1
    )

    # Scale RFM features before clustering.
    features = rfm[["recency", "frequency", "monetary"]].copy()

    # Log transform reduces the influence of large monetary values.
    features["recency"] = features["recency"].clip(lower=0)
    features["frequency"] = features["frequency"].clip(lower=0)
    features["monetary"] = features["monetary"].clip(lower=0)

    features["frequency"] = __import__("numpy").log1p(
        features["frequency"]
    )
    features["monetary"] = __import__("numpy").log1p(
        features["monetary"]
    )

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Four customer segments.
    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10,
    )

    rfm["segment"] = model.fit_predict(scaled_features)

    # Save customer-level RFM features and cluster assignments.
    output_path = OUTPUT_DIR / "customer_segments.csv"
    rfm.to_csv(output_path, index=False)

    # Summarize each cluster.
    summary = rfm.groupby("segment").agg(
        customer_count=("customer_id", "count"),
        avg_recency_days=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary_inr=("monetary", "mean"),
    ).round(2)

    summary_path = OUTPUT_DIR / "customer_segment_summary.csv"
    summary.to_csv(summary_path)

    print(f"Customers segmented: {len(rfm)}")
    print(f"Completed-order customers: {int((rfm['frequency'] > 0).sum())}")
    print(f"Segments created: {rfm['segment'].nunique()}")

    print("\nSegment summary:")
    print(summary)

    print(f"\nSaved customer segments: {output_path}")
    print(f"Saved segment summary: {summary_path}")


if __name__ == "__main__":
    main()