from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"


def audit_file(filename):
    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )

    # Preserve blank strings in ticket text.
    if filename == "tickets.csv":
        df = pd.read_csv(file_path, keep_default_na=False)
    else:
        df = pd.read_csv(file_path)

    print("\n" + "=" * 70)
    print(f"FILE: {filename}")
    print("=" * 70)

    print(f"\nShape: {df.shape}")

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nMissing values:")
    missing_count = df.isna().sum()
    missing_percent = (missing_count / len(df) * 100).round(2)

    missing_report = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percent": missing_percent,
    })

    print(missing_report.to_string())

    return df


def main():
    customers = audit_file("customers.csv")
    products = audit_file("products.csv")
    orders = audit_file("orders.csv")
    tickets = audit_file("tickets.csv")

    print("\n" + "=" * 70)
    print("RAW DATA CHECKPOINTS")
    print("=" * 70)

    print(f"Customers: {len(customers)}")
    print(f"Products: {len(products)}")
    print(f"Raw orders: {len(orders)}")
    print(f"Tickets: {len(tickets)}")

    print(f"Exact duplicate order rows: {orders.duplicated().sum()}")

    if "status" in orders.columns:
        print(
            "Pending orders:",
            orders["status"].astype(str).str.strip().str.lower()
            .eq("pending").sum()
        )

    if "order_id" in orders.columns:
        print("Distinct order IDs:", orders["order_id"].nunique())

    if "order_amount" in orders.columns:
        numeric_amount = pd.to_numeric(
            orders["order_amount"], errors="coerce"
        )
        print(
            "Nonnumeric order amounts:",
            (
                orders["order_amount"].notna()
                & numeric_amount.isna()
            ).sum()
        )

    if "delivery_minutes" in orders.columns:
        delivery = pd.to_numeric(
            orders["delivery_minutes"], errors="coerce"
        )
        print("Negative delivery minutes:", (delivery < 0).sum())
        print("Blank delivery minutes:", delivery.isna().sum())

    if "age" in customers.columns:
        age = pd.to_numeric(customers["age"], errors="coerce")
        print("Blank customer ages:", age.isna().sum())
        print(
            "Customer ages outside 10-100:",
            ((age < 10) | (age > 100)).sum()
        )

    if "city" in customers.columns:
        print("Distinct raw city spellings:", customers["city"].nunique())

    if "gender" in customers.columns:
        gender = customers["gender"].astype(str).str.strip()
        print(
            "Distinct nonblank raw gender spellings:",
            gender[gender.ne("")].nunique()
        )
        print("Blank gender values:", gender.eq("").sum())

    print("\nRAW DATA AUDIT FINISHED")


if __name__ == "__main__":
    main()
