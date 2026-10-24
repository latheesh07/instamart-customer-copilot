from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
DB = ROOT / "data" / "instamart.db"

checks_passed = 0


def check(condition, message):
    global checks_passed

    if not condition:
        raise AssertionError(f"CHECK FAILED: {message}")

    checks_passed += 1
    print(f"PASS: {message}")


def main():
    # Check 1: Raw orders
    raw_orders = pd.read_csv(RAW / "orders.csv")
    check(
        len(raw_orders) == 13084,
        "Raw orders contain 13,084 rows"
    )

    # Check 2: Duplicate rows
    duplicate_count = int(raw_orders.duplicated().sum())
    check(
        duplicate_count == 119,
        "Raw orders contain 119 exact duplicate rows"
    )

    # Check 3: Clean customers
    customers = pd.read_csv(CLEAN / "customers.csv")
    check(
        len(customers) == 1200,
        "Clean customers contain 1,200 rows"
    )

    check(
        customers["customer_id"].is_unique,
        "Clean customer IDs are unique"
    )

    check(
        customers["age"].notna().all()
        and customers["age"].between(18, 60).all(),
        "Customer ages are complete and between 18 and 60"
    )

    # Check 4: Clean products
    products = pd.read_csv(CLEAN / "products.csv")
    check(
        len(products) == 40
        and products["product_id"].is_unique,
        "Clean products contain 40 unique products"
    )

    # Check 5: Clean orders
    orders = pd.read_csv(CLEAN / "orders.csv")

    check(
        len(orders) == 12309,
        "Clean orders contain 12,309 rows"
    )

    check(
        orders["order_id"].is_unique,
        "Clean order IDs are unique"
    )

    check(
        set(orders["status"].dropna().unique())
        == {"completed", "cancelled"},
        "Clean orders contain only completed and cancelled statuses"
    )

    completed = orders.loc[orders["status"] == "completed"]
    cancelled = orders.loc[orders["status"] == "cancelled"]

    check(
        len(completed) == 11110 and len(cancelled) == 1199,
        "Completed and cancelled order counts match expected values"
    )

    check(
        orders["order_amount"].notna().all(),
        "All cleaned order amounts are present"
    )

    check(
        completed["delivery_minutes"].notna().all(),
        "Completed orders have delivery times"
    )

    check(
        cancelled["delivery_minutes"].isna().all(),
        "Cancelled orders have no delivery times"
    )

    completed_revenue = round(
        completed["order_amount"].sum(), 2
    )

    check(
        completed_revenue == 2998668.80,
        "Completed order revenue equals INR 2,998,668.80"
    )

    # Check 6: SQLite database
    check(DB.exists(), "SQLite database file exists")

    with sqlite3.connect(DB) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

        check(
            {"customers", "products", "orders"}.issubset(tables),
            "SQLite contains customers, products and orders tables"
        )

        db_order_count = conn.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        check(
            db_order_count == 12309,
            "SQLite orders table contains 12,309 rows"
        )

        sql_revenue = conn.execute(
            """
            SELECT ROUND(SUM(order_amount), 2)
            FROM orders
            WHERE status = 'completed'
            """
        ).fetchone()[0]

        check(
            sql_revenue is not None
            and round(sql_revenue, 2) == completed_revenue,
            "SQLite revenue matches cleaned CSV revenue"
        )

    # Check 7: SQL query file
    query_file = ROOT / "sql" / "queries.sql"
    check(query_file.exists(), "SQL query file exists")

    query_text = query_file.read_text(encoding="utf-8").upper()
    check(
        all(f"Q{i}" in query_text for i in range(1, 8)),
        "SQL file contains all seven query labels"
    )

    # Check 8: Order statistics
    mean_amount = completed["order_amount"].mean()
    median_amount = completed["order_amount"].median()
    q1 = completed["order_amount"].quantile(0.25)
    q3 = completed["order_amount"].quantile(0.75)
    upper_fence = q3 + 1.5 * (q3 - q1)
    outliers_above = int(
        (completed["order_amount"] > upper_fence).sum()
    )

    check(
        round(mean_amount, 2) == 269.91,
        "Mean completed order amount matches INR 269.91"
    )

    check(
        round(median_amount, 2) == 135.00,
        "Median completed order amount matches INR 135.00"
    )

    check(
        round(q1, 2) == 64.80 and round(q3, 2) == 297.00,
        "First and third quartiles match expected values"
    )

    check(
        round(upper_fence, 2) == 645.30
        and outliers_above == 897,
        "Upper outlier fence and outlier count match"
    )

    # Check 9: Correlation
    correlations = completed[
        ["order_amount", "discount_pct", "quantity"]
    ].corr()

    amount_discount = correlations.loc[
        "order_amount", "discount_pct"
    ]
    amount_quantity = correlations.loc[
        "order_amount", "quantity"
    ]

    check(
        round(amount_discount, 4) == -0.0951,
        "Amount-discount correlation matches -0.0951"
    )

    check(
        round(amount_quantity, 4) == 0.0873,
        "Amount-quantity correlation matches 0.0873"
    )

    print("\n" + "=" * 45)
    print(f"CHECKPOINTS PASSED: {checks_passed}")
    print("ALL CHECKPOINTS PASSED")
    print("=" * 45)


if __name__ == "__main__":
    main()