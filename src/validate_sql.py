from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "instamart.db"


def main():
    with sqlite3.connect(DB_PATH) as connection:
        ranking = pd.read_sql_query(
            """
            WITH customer_city_spend AS (
                SELECT
                    c.city,
                    c.customer_id,
                    SUM(o.order_amount) AS total_spend
                FROM customers c
                JOIN orders o
                    ON c.customer_id = o.customer_id
                WHERE o.status = 'completed'
                GROUP BY c.city, c.customer_id
            )
            SELECT
                city,
                customer_id,
                total_spend,
                RANK() OVER (
                    PARTITION BY city
                    ORDER BY total_spend DESC
                ) AS spend_rank,
                ROW_NUMBER() OVER (
                    PARTITION BY city
                    ORDER BY total_spend DESC, customer_id
                ) AS row_num
            FROM customer_city_spend
            """,
            connection
        )

    differences = int(
        (ranking["spend_rank"] != ranking["row_num"]).sum()
    )

    print("Ranking rows:", len(ranking))
    print("RANK vs ROW_NUMBER differences:", differences)

    assert len(ranking) == 1175, "Unexpected ranking row count"
    assert differences == 8, "Unexpected ranking difference count"

    print("RANKING VALIDATION PASSED")


if __name__ == "__main__":
    main()