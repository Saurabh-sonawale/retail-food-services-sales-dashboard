from pathlib import Path
import sqlite3

import pandas as pd


def main():
    processed_dir = Path("data/processed")
    csv_path = processed_dir / "cleaned_online_retail.csv"
    db_path = processed_dir / "retail_sales.db"

    if not csv_path.exists():
        raise FileNotFoundError(
            "Could not find data/processed/cleaned_online_retail.csv. "
            "Run src/data_cleaning.py first."
        )

    print("Loading cleaned CSV file...")
    df = pd.read_csv(csv_path, low_memory=False)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    print("Creating SQLite database...")
    connection = sqlite3.connect(db_path)

    table_name = "cleaned_online_retail"

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print(f"Table created: {table_name}")

    cursor = connection.cursor()

    # Basic validation checks
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]

    cursor.execute(f"SELECT ROUND(SUM(total_revenue), 2) FROM {table_name};")
    total_revenue = cursor.fetchone()[0]

    cursor.execute(f"SELECT COUNT(DISTINCT invoice_no) FROM {table_name};")
    total_orders = cursor.fetchone()[0]

    cursor.execute(
        f"""
        SELECT COUNT(DISTINCT customer_id)
        FROM {table_name}
        WHERE customer_id <> 'Unknown';
        """
    )
    total_customers = cursor.fetchone()[0]

    print("\nDatabase validation summary:")
    print(f"- Row count: {row_count:,}")
    print(f"- Total revenue: ${total_revenue:,.2f}")
    print(f"- Total orders: {total_orders:,}")
    print(f"- Known customers: {total_customers:,}")

    # Show top 5 countries by revenue
    print("\nTop 5 countries by revenue:")
    cursor.execute(
        f"""
        SELECT
            country,
            ROUND(SUM(total_revenue), 2) AS country_revenue
        FROM {table_name}
        GROUP BY country
        ORDER BY country_revenue DESC
        LIMIT 5;
        """
    )

    for country, revenue in cursor.fetchall():
        print(f"- {country}: ${revenue:,.2f}")

    connection.close()

    print(f"\nSQLite database created successfully:")
    print(f"- {db_path}")


if __name__ == "__main__":
    main()