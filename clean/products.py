from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def clean_products():
    input_path = RAW_DIR / "products.csv"
    output_path = CLEAN_DIR / "products.csv"

    df = pd.read_csv(input_path)

    required_columns = {
        "product_id",
        "product_name",
        "category",
        "price_inr",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df["product_id"] = df["product_id"].astype("string").str.strip()
    df["product_name"] = df["product_name"].astype("string").str.strip()
    df["category"] = df["category"].astype("string").str.strip()

    df["price_inr"] = pd.to_numeric(
        df["price_inr"], errors="raise"
    )

    if df["product_id"].isna().any() or df["product_id"].eq("").any():
        raise ValueError("Product IDs cannot be blank.")

    if df["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs found.")

    if df["price_inr"].isna().any() or (df["price_inr"] <= 0).any():
        raise ValueError("Product prices must be positive numbers.")

    df.to_csv(output_path, index=False)

    print("Cleaned products:", len(df))
    print("Unique product IDs:", df["product_id"].nunique())
    print("Missing values:", int(df.isna().sum().sum()))
    print("Saved:", output_path)


if __name__ == "__main__":
    clean_products()
