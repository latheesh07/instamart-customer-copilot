from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ORDERS_PATH = ROOT / "data" / "clean" / "orders.csv"


def main():
    if not ORDERS_PATH.exists():
        raise FileNotFoundError(f"Orders file not found: {ORDERS_PATH}")

    orders = pd.read_csv(ORDERS_PATH)

    completed = orders.loc[
        orders["status"] == "completed"
    ].copy()

    completed["order_amount"] = pd.to_numeric(
        completed["order_amount"], errors="coerce"
    )
    completed["discount_pct"] = pd.to_numeric(
        completed["discount_pct"], errors="coerce"
    )
    completed["quantity"] = pd.to_numeric(
        completed["quantity"], errors="coerce"
    )

    columns = ["order_amount", "discount_pct", "quantity"]
    correlation = completed[columns].corr()

    print("Correlation Matrix:")
    print(correlation.round(4))

    amount_discount = correlation.loc["order_amount", "discount_pct"]
    amount_quantity = correlation.loc["order_amount", "quantity"]

    print(f"\nAmount vs Discount correlation: {amount_discount:.4f}")
    print(f"Amount vs Quantity correlation: {amount_quantity:.4f}")

    if abs(amount_discount) >= abs(amount_quantity):
        print("Largest absolute correlation: order_amount vs discount_pct")
    else:
        print("Largest absolute correlation: order_amount vs quantity")

    print("\nNote: Correlation does not establish causation.")


if __name__ == "__main__":
    main()