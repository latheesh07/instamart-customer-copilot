from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def clean_customers():
    input_path = RAW_DIR / "customers.csv"
    output_path = CLEAN_DIR / "customers.csv"

    df = pd.read_csv(input_path)

    # Normalize city names.
    df["city"] = df["city"].astype("string").str.strip().str.title()

    valid_cities = {
        "Pune",
        "Delhi",
        "Bengaluru",
        "Chennai",
        "Hyderabad",
        "Mumbai",
    }

    invalid_cities = ~df["city"].isin(valid_cities)

    if invalid_cities.any():
        raise ValueError(
            "Unexpected city values found: "
            f"{df.loc[invalid_cities, 'city'].unique().tolist()}"
        )

    # Normalize gender values.
    gender = df["gender"].astype("string").str.strip().str.lower()

    gender_map = {
        "m": "male",
        "male": "male",
        "man": "male",
        "f": "female",
        "female": "female",
        "woman": "female",
    }

    df["gender"] = gender.map(gender_map).fillna("unknown")

    # Convert ages to numeric and mark invalid ages as missing.
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df.loc[~df["age"].between(10, 100), "age"] = pd.NA

    # Fill missing ages with the median for each city.
    city_medians = df.groupby("city")["age"].transform("median")
    df["age"] = df["age"].fillna(city_medians)

    if df["age"].isna().any():
        raise AssertionError("Missing ages remain after city-median filling.")

    if not df["age"].between(18, 60).all():
        raise AssertionError("Cleaned ages are outside the expected 18-60 range.")

    # Parse signup dates.
    df["signup_date"] = pd.to_datetime(
        df["signup_date"], errors="raise"
    )

    # Save dates in a reproducible format.
    df["signup_date"] = df["signup_date"].dt.strftime("%Y-%m-%d")

    df.to_csv(output_path, index=False)

    print("Cleaned customers:", len(df))
    print("\nCity counts:")
    print(df["city"].value_counts().sort_index().to_string())

    print("\nGender counts:")
    print(df["gender"].value_counts().sort_index().to_string())

    print("\nMissing ages:", df["age"].isna().sum())
    print("Age range:", df["age"].min(), "-", df["age"].max())
    print("Saved:", output_path)


if __name__ == "__main__":
    clean_customers()