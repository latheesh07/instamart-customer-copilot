from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "instamart.db"


def main():
    with sqlite3.connect(DB_PATH) as connection:
        sql_result = pd.read_sql_query(
            """
            SELECT
                c.city,
                p.category,
                SUM(o.order_amount) AS revenue
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            JOIN products p
                ON o.product_id = p.product_id
            WHERE o.status = 'completed'
            GROUP BY c.city, p.category
            ORDER BY c.city, p.category
            """,
            connection,
        )

        customers = pd.read_sql_query(
            "SELECT * FROM customers", connection
        )
        products = pd.read_sql_query(
            "SELECT * FROM products", connection
        )
        orders = pd.read_sql_query(
            "SELECT * FROM orders", connection
        )

    completed = orders[orders["status"] == "completed"].copy()

    merged = completed.merge(
        customers[["customer_id", "city"]],
        on="customer_id",
    ).merge(
        products[["product_id", "category"]],
        on="product_id",
    )

    pandas_result = (
        merged.groupby(["city", "category"], as_index=False)
        .agg(revenue=("order_amount", "sum"))
        .sort_values(["city", "category"])
        .reset_index(drop=True)
    )

    sql_result = sql_result.reset_index(drop=True)

    pd.testing.assert_frame_equal(
        sql_result[["city", "category"]],
        pandas_result[["city", "category"]],
    )

    pd.testing.assert_series_equal(
        sql_result["revenue"].round(2),
        pandas_result["revenue"].round(2),
        check_names=False,
    )

    sql_total = round(sql_result["revenue"].sum(), 2)
    pandas_total = round(pandas_result["revenue"].sum(), 2)

    print(f"SQL revenue total: {sql_total:.2f}")
    print(f"Pandas revenue total: {pandas_total:.2f}")
    print(f"Revenue difference: {sql_total - pandas_total:.2f}")

    assert sql_total == 2998668.80
    assert pandas_total == 2998668.80

    print("REVENUE CROSS-CHECK PASSED")


if __name__ == "__main__":
    main()