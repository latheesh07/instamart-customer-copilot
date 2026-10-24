from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ORDERS_PATH = ROOT / "data" / "clean" / "orders.csv"


def main():
    if not ORDERS_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned orders file not found: {ORDERS_PATH}"
        )

    orders = pd.read_csv(ORDERS_PATH)

    completed = orders.loc[
        orders["status"] == "completed", "order_amount"
    ].dropna()

    if completed.empty:
        raise ValueError("No completed order amounts available.")

    q1 = completed.quantile(0.25)
    median = completed.median()
    q3 = completed.quantile(0.75)
    iqr = q3 - q1

    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    outliers_below = int((completed < lower_fence).sum())
    outliers_above = int((completed > upper_fence).sum())

    print("Completed orders:", len(completed))
    print(f"Mean order amount: ₹{completed.mean():.2f}")
    print(f"Median order amount: ₹{median:.2f}")
    print(f"Standard deviation: ₹{completed.std():.2f}")
    print(f"Skewness: {completed.skew():.2f}")
    print(f"Q1 (25th percentile): ₹{q1:.2f}")
    print(f"Q3 (75th percentile): ₹{q3:.2f}")
    print(f"IQR: ₹{iqr:.2f}")
    print(f"Lower outlier fence: ₹{lower_fence:.2f}")
    print(f"Upper outlier fence: ₹{upper_fence:.2f}")
    print("Outliers below lower fence:", outliers_below)
    print("Outliers above upper fence:", outliers_above)


if __name__ == "__main__":
    main()