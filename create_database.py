from pathlib import Path
import sqlite3

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
CLEAN_DIR = ROOT / "data" / "clean"
DATABASE_PATH = ROOT / "data" / "instamart.db"


def create_database():
    required_files = {
        "customers": CLEAN_DIR / "customers.csv",
        "products": CLEAN_DIR / "products.csv",
        "orders": CLEAN_DIR / "orders.csv",
    }

    for table_name, file_path in required_files.items():
        if not file_path.exists():
            raise FileNotFoundError(
                f"Required cleaned file not found: {file_path}"
            )

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        for table_name, file_path in required_files.items():
            df = pd.read_csv(file_path)

            if table_name == "customers":
                df["signup_date"] = pd.to_datetime(
                    df["signup_date"], errors="raise"
                ).dt.strftime("%Y-%m-%d")

            if table_name == "orders":
                df["order_ts"] = pd.to_datetime(
                    df["order_ts"], errors="raise"
                ).dt.strftime("%Y-%m-%d %H:%M:%S")

            df.to_sql(
                table_name,
                connection,
                if_exists="replace",
                index=False,
            )

            print(f"Created table: {table_name} ({len(df)} rows)")

        # Validate the tables and their row counts.
        expected_counts = {
            "customers": 1200,
            "products": 40,
            "orders": 12309,
        }

        for table_name, expected_count in expected_counts.items():
            actual_count = connection.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            if actual_count != expected_count:
                raise AssertionError(
                    f"{table_name}: expected {expected_count}, "
                    f"got {actual_count}"
                )

        # Validate order timestamp format.
        bad_timestamps = connection.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE length(order_ts) != 19
            """
        ).fetchone()[0]

        if bad_timestamps:
            raise AssertionError(
                "Some order timestamps are not YYYY-MM-DD HH:MM:SS."
            )

    print("Database created and validated:", DATABASE_PATH)


if __name__ == "__main__":
    create_database()