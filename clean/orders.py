from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def clean_orders():
    orders_path = RAW_DIR / "orders.csv"
    products_path = CLEAN_DIR / "products.csv"
    output_path = CLEAN_DIR / "orders.csv"

    orders = pd.read_csv(orders_path)
    products = pd.read_csv(products_path)

    print("Raw order rows:", len(orders))

    # 1. Convert order timestamps to datetime.
    orders["order_ts"] = pd.to_datetime(
        orders["order_ts"], errors="raise"
    )

    # 2. Remove exact duplicate rows.
    before = len(orders)
    orders = orders.drop_duplicates().copy()
    print("Exact duplicate rows removed:", before - len(orders))

    # 3. Keep the latest record for each order_id.
    # A stable sort makes the selection reproducible.
    orders = orders.sort_values(
        ["order_ts"], kind="mergesort"
    )

    orders = orders.drop_duplicates(
        subset=["order_id"], keep="last"
    ).copy()

    if orders["order_id"].duplicated().any():
        raise AssertionError("Duplicate order IDs remain.")

    # 4. Convert order amounts to numeric.
    orders["order_amount"] = pd.to_numeric(
        orders["order_amount"], errors="coerce"
    )

    # Prepare product information for amount calculation
    # and category-based delivery imputation.
    required_product_columns = {
        "product_id",
        "price_inr",
        "category",
    }

    if not required_product_columns.issubset(products.columns):
        raise ValueError(
            "Products file must contain product_id, price_inr, category."
        )

    product_info = products[
        ["product_id", "price_inr", "category"]
    ].copy()

    orders = orders.merge(
        product_info,
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    if orders["price_inr"].isna().any():
        raise AssertionError("Some orders have no matching product price.")

    orders["quantity"] = pd.to_numeric(
        orders["quantity"], errors="raise"
    )
    orders["discount_pct"] = pd.to_numeric(
        orders["discount_pct"], errors="raise"
    )

    calculated_amount = (
        orders["price_inr"]
        * orders["quantity"]
        * (1 - orders["discount_pct"] / 100)
    ).round(2)

    missing_amount = orders["order_amount"].isna()

    orders.loc[missing_amount, "order_amount"] = (
        calculated_amount.loc[missing_amount]
    )

    # 5. Convert delivery times to numeric.
    orders["delivery_minutes"] = pd.to_numeric(
        orders["delivery_minutes"], errors="coerce"
    )

    # 6. Negative delivery times become missing.
    negative_delivery = orders["delivery_minutes"] < 0
    orders.loc[negative_delivery, "delivery_minutes"] = pd.NA

    # 7. Fill missing delivery times for completed orders
    # using the completed-order median for each product category.
    completed_mask = orders["status"].eq("completed")

    completed_category_medians = (
        orders.loc[completed_mask]
        .groupby("category")["delivery_minutes"]
        .transform("median")
    )

    completed_indices = orders.index[completed_mask]

    missing_completed_delivery = (
        orders.loc[completed_indices, "delivery_minutes"].isna()
    )

    missing_indices = completed_indices[missing_completed_delivery]

    category_medians = (
        orders.loc[completed_mask]
        .groupby("category")["delivery_minutes"]
        .median()
    )

    orders.loc[missing_indices, "delivery_minutes"] = (
        orders.loc[missing_indices, "category"]
        .map(category_medians)
    )

    # 8. Cancelled-order delivery times remain missing.
    cancelled_mask = orders["status"].eq("cancelled")

    # Keep the required columns in the clean output.
    orders["order_ts"] = orders["order_ts"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    clean_columns = [
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "order_ts",
        "status",
        "discount_pct",
        "order_amount",
        "delivery_minutes",
    ]

    clean_orders_df = orders[clean_columns].copy()

    # Validation checks.
    if clean_orders_df["order_id"].nunique() != len(clean_orders_df):
        raise AssertionError("Order IDs are not unique.")

    if clean_orders_df["order_amount"].isna().any():
        raise AssertionError("Missing order amounts remain.")

    completed = clean_orders_df["status"].eq("completed")
    cancelled = clean_orders_df["status"].eq("cancelled")

    if clean_orders_df.loc[completed, "delivery_minutes"].isna().any():
        raise AssertionError(
            "Completed orders still have missing delivery times."
        )

    if clean_orders_df.loc[cancelled, "delivery_minutes"].notna().any():
        raise AssertionError(
            "Cancelled orders should retain missing delivery times."
        )

    clean_orders_df.to_csv(output_path, index=False)

    print("\nCleaned order rows:", len(clean_orders_df))
    print("\nStatus counts:")
    print(clean_orders_df["status"].value_counts().to_string())

    print(
        "\nMissing completed delivery times:",
        clean_orders_df.loc[completed, "delivery_minutes"].isna().sum(),
    )

    print(
        "Missing cancelled delivery times:",
        clean_orders_df.loc[cancelled, "delivery_minutes"].isna().sum(),
    )

    print(
        "Missing order amounts:",
        clean_orders_df["order_amount"].isna().sum(),
    )

    print(
        "Completed order amount sum:",
        round(clean_orders_df.loc[completed, "order_amount"].sum(), 2),
    )

    print("Saved:", output_path)


if __name__ == "__main__":
    clean_orders()
