from pathlib import Path

import pandas as pd
import numpy as np


def main():
    raw_path = Path("data/raw/Online Retail.xlsx")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    if not raw_path.exists():
        raise FileNotFoundError(
            "Could not find data/raw/Online Retail.xlsx. "
            "Make sure the dataset is inside the data/raw folder."
        )

    print("Loading raw dataset...")
    df = pd.read_excel(raw_path)

    print(f"Raw rows: {len(df):,}")
    print(f"Raw columns: {list(df.columns)}")

    # Standardize column names
    df = df.rename(
        columns={
            "InvoiceNo": "invoice_no",
            "StockCode": "stock_code",
            "Description": "description",
            "Quantity": "quantity",
            "InvoiceDate": "invoice_date",
            "UnitPrice": "unit_price",
            "CustomerID": "customer_id",
            "Country": "country",
        }
    )

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Convert invoice number to string for cancelled invoice detection
    df["invoice_no"] = df["invoice_no"].astype(str)

    # Remove cancelled transactions
    df = df[~df["invoice_no"].str.startswith("C", na=False)]

    # Remove invalid quantity and price rows
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] > 0]

    # Remove rows without product description
    df = df.dropna(subset=["description"])

    # Clean text fields
    df["description"] = df["description"].astype(str).str.strip()
    df["country"] = df["country"].astype(str).str.strip()

    # Convert invoice date
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df = df.dropna(subset=["invoice_date"])

    # Customer ID handling
    df["known_customer"] = np.where(df["customer_id"].isna(), "No", "Yes")
    df["customer_id"] = df["customer_id"].fillna(0).astype(int).astype(str)
    df["customer_id"] = df["customer_id"].replace("0", "Unknown")

    # Create revenue metric
    df["total_revenue"] = df["quantity"] * df["unit_price"]

    # Date features for dashboarding
    df["invoice_year"] = df["invoice_date"].dt.year
    df["invoice_month"] = df["invoice_date"].dt.month
    df["invoice_month_name"] = df["invoice_date"].dt.month_name()
    df["invoice_year_month"] = df["invoice_date"].dt.to_period("M").astype(str)
    df["invoice_day"] = df["invoice_date"].dt.day
    df["invoice_day_name"] = df["invoice_date"].dt.day_name()
    df["invoice_hour"] = df["invoice_date"].dt.hour

    # Reorder columns
    final_columns = [
        "invoice_no",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "invoice_year",
        "invoice_month",
        "invoice_month_name",
        "invoice_year_month",
        "invoice_day",
        "invoice_day_name",
        "invoice_hour",
        "unit_price",
        "total_revenue",
        "customer_id",
        "known_customer",
        "country",
    ]

    df_clean = df[final_columns].copy()

    print(f"Cleaned rows: {len(df_clean):,}")
    print(f"Total revenue: ${df_clean['total_revenue'].sum():,.2f}")

    # Export cleaned full dataset
    df_clean.to_csv(processed_dir / "cleaned_online_retail.csv", index=False)

    # KPI summary
    kpi_summary = pd.DataFrame(
        {
            "metric": [
                "total_revenue",
                "total_orders",
                "total_customers",
                "total_quantity_sold",
                "average_order_value",
                "countries_served",
            ],
            "value": [
                df_clean["total_revenue"].sum(),
                df_clean["invoice_no"].nunique(),
                df_clean.loc[df_clean["customer_id"] != "Unknown", "customer_id"].nunique(),
                df_clean["quantity"].sum(),
                df_clean.groupby("invoice_no")["total_revenue"].sum().mean(),
                df_clean["country"].nunique(),
            ],
        }
    )
    kpi_summary.to_csv(processed_dir / "kpi_summary.csv", index=False)

    # Monthly sales summary
    monthly_sales = (
        df_clean.groupby("invoice_year_month")
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_orders=("invoice_no", "nunique"),
            total_quantity=("quantity", "sum"),
            total_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .sort_values("invoice_year_month")
    )
    monthly_sales.to_csv(processed_dir / "monthly_sales_summary.csv", index=False)

    # Product performance summary
    product_performance = (
        df_clean.groupby(["stock_code", "description"])
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_quantity=("quantity", "sum"),
            total_orders=("invoice_no", "nunique"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    product_performance.to_csv(processed_dir / "product_performance_summary.csv", index=False)

    # Customer summary
    customer_summary = (
        df_clean[df_clean["customer_id"] != "Unknown"]
        .groupby("customer_id")
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_orders=("invoice_no", "nunique"),
            total_quantity=("quantity", "sum"),
            first_purchase=("invoice_date", "min"),
            last_purchase=("invoice_date", "max"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    customer_summary.to_csv(processed_dir / "customer_summary.csv", index=False)

    # Country sales summary
    country_sales = (
        df_clean.groupby("country")
        .agg(
            total_revenue=("total_revenue", "sum"),
            total_orders=("invoice_no", "nunique"),
            total_customers=("customer_id", "nunique"),
            total_quantity=("quantity", "sum"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    country_sales.to_csv(processed_dir / "country_sales_summary.csv", index=False)

    print("Data cleaning complete.")
    print("Files created in data/processed:")
    for file in processed_dir.glob("*.csv"):
        print(f"- {file.name}")


if __name__ == "__main__":
    main()