from pathlib import Path
import sqlite3

import pandas as pd


def run_query(connection, query, output_path):
    df = pd.read_sql_query(query, connection)
    df.to_csv(output_path, index=False)
    print(f"Created: {output_path.name} | Shape: {df.shape}")


def main():
    db_path = Path("data/processed/retail_sales.db")
    output_dir = Path("reports/sql_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not db_path.exists():
        raise FileNotFoundError(
            "Could not find data/processed/retail_sales.db. "
            "Run src/create_sqlite_database.py first."
        )

    connection = sqlite3.connect(db_path)

    queries = {
        "executive_kpi_summary.csv": """
            SELECT
                ROUND(SUM(total_revenue), 2) AS total_revenue,
                COUNT(DISTINCT invoice_no) AS total_orders,
                COUNT(DISTINCT CASE WHEN customer_id <> 'Unknown' THEN customer_id END) AS total_customers,
                SUM(quantity) AS total_quantity_sold,
                ROUND(SUM(total_revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value,
                COUNT(DISTINCT country) AS countries_served
            FROM cleaned_online_retail;
        """,

        "monthly_sales_trend.csv": """
            SELECT
                invoice_year_month,
                ROUND(SUM(total_revenue), 2) AS monthly_revenue,
                COUNT(DISTINCT invoice_no) AS total_orders,
                SUM(quantity) AS total_quantity_sold,
                COUNT(DISTINCT CASE WHEN customer_id <> 'Unknown' THEN customer_id END) AS total_customers
            FROM cleaned_online_retail
            GROUP BY invoice_year_month
            ORDER BY invoice_year_month;
        """,

        "top_10_products_by_revenue.csv": """
            SELECT
                stock_code,
                description,
                ROUND(SUM(total_revenue), 2) AS product_revenue,
                SUM(quantity) AS total_quantity_sold,
                COUNT(DISTINCT invoice_no) AS total_orders
            FROM cleaned_online_retail
            GROUP BY stock_code, description
            ORDER BY product_revenue DESC
            LIMIT 10;
        """,

        "top_10_customers_by_revenue.csv": """
            SELECT
                customer_id,
                ROUND(SUM(total_revenue), 2) AS customer_revenue,
                COUNT(DISTINCT invoice_no) AS total_orders,
                SUM(quantity) AS total_quantity_purchased,
                ROUND(SUM(total_revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
            FROM cleaned_online_retail
            WHERE customer_id <> 'Unknown'
            GROUP BY customer_id
            ORDER BY customer_revenue DESC
            LIMIT 10;
        """,

        "country_sales_analysis.csv": """
            SELECT
                country,
                ROUND(SUM(total_revenue), 2) AS country_revenue,
                COUNT(DISTINCT invoice_no) AS total_orders,
                COUNT(DISTINCT CASE WHEN customer_id <> 'Unknown' THEN customer_id END) AS total_customers,
                SUM(quantity) AS total_quantity_sold
            FROM cleaned_online_retail
            GROUP BY country
            ORDER BY country_revenue DESC;
        """,

        "sales_by_day_of_week.csv": """
            SELECT
                invoice_day_name,
                ROUND(SUM(total_revenue), 2) AS revenue,
                COUNT(DISTINCT invoice_no) AS total_orders,
                SUM(quantity) AS total_quantity_sold
            FROM cleaned_online_retail
            GROUP BY invoice_day_name
            ORDER BY revenue DESC;
        """,

        "sales_by_hour.csv": """
            SELECT
                invoice_hour,
                ROUND(SUM(total_revenue), 2) AS revenue,
                COUNT(DISTINCT invoice_no) AS total_orders,
                SUM(quantity) AS total_quantity_sold
            FROM cleaned_online_retail
            GROUP BY invoice_hour
            ORDER BY invoice_hour;
        """,

        "customer_segments.csv": """
            SELECT
                CASE
                    WHEN total_orders = 1 THEN 'One-time Customer'
                    WHEN total_orders BETWEEN 2 AND 5 THEN 'Repeat Customer'
                    WHEN total_orders BETWEEN 6 AND 10 THEN 'Loyal Customer'
                    ELSE 'High-Value Loyal Customer'
                END AS customer_segment,
                COUNT(*) AS number_of_customers,
                ROUND(SUM(customer_revenue), 2) AS segment_revenue,
                ROUND(AVG(customer_revenue), 2) AS average_customer_revenue
            FROM (
                SELECT
                    customer_id,
                    COUNT(DISTINCT invoice_no) AS total_orders,
                    SUM(total_revenue) AS customer_revenue
                FROM cleaned_online_retail
                WHERE customer_id <> 'Unknown'
                GROUP BY customer_id
            ) customer_orders
            GROUP BY customer_segment
            ORDER BY segment_revenue DESC;
        """
    }

    print("Running SQL analysis queries...\n")

    for file_name, query in queries.items():
        output_path = output_dir / file_name
        run_query(connection, query, output_path)

    connection.close()

    print("\nSQL analysis complete.")
    print("Files created in reports/sql_outputs.")


if __name__ == "__main__":
    main()