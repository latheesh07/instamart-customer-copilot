from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "instamart.db"
SQL_PATH = ROOT / "sql" / "queries.sql"


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_PATH}")

    sql_text = SQL_PATH.read_text(encoding="utf-8")

    queries = [
        statement.strip()
        for statement in sql_text.split(";")
        if statement.strip()
    ]

    if len(queries) != 7:
        raise AssertionError(
            f"Expected 7 SQL queries, but found {len(queries)}"
        )

    with sqlite3.connect(DB_PATH) as connection:
        for index, query in enumerate(queries, start=1):
            result = pd.read_sql_query(query, connection)

            print("\n" + "=" * 50)
            print(f"QUERY {index}")
            print(f"Rows returned: {len(result)}")
            print(result.head(5).to_string(index=False))

            if index == 2:
                print(
                    "Total revenue:",
                    round(result["revenue"].sum(), 2)
                )

            if index == 5:
                spend_summary = pd.read_sql_query(
                    """
                    SELECT
                        customer_id,
                        SUM(order_amount) AS total_spend
                    FROM orders
                    WHERE status = 'completed'
                    GROUP BY customer_id
                    """,
                    connection
                )

                print(
                    "Average completed spend per customer:",
                    round(spend_summary["total_spend"].mean(), 2)
                )

            if index == 7:
                print(
                    "Final cumulative revenue:",
                    round(result["cumulative_revenue"].iloc[-1], 2)
                )

    print("\nAll 7 SQL queries executed successfully.")


if __name__ == "__main__":
    main()