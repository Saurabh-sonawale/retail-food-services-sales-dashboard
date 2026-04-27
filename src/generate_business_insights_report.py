from pathlib import Path

import pandas as pd


def format_currency(value):
    return f"${value:,.2f}"


def main():
    outputs_dir = Path("reports/sql_outputs")
    report_path = Path("reports/business_insights.md")

    required_files = {
        "kpi": outputs_dir / "executive_kpi_summary.csv",
        "monthly": outputs_dir / "monthly_sales_trend.csv",
        "products": outputs_dir / "top_10_products_by_revenue.csv",
        "customers": outputs_dir / "top_10_customers_by_revenue.csv",
        "countries": outputs_dir / "country_sales_analysis.csv",
        "segments": outputs_dir / "customer_segments.csv",
        "days": outputs_dir / "sales_by_day_of_week.csv",
        "hours": outputs_dir / "sales_by_hour.csv",
    }

    for name, path in required_files.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")

    kpi = pd.read_csv(required_files["kpi"])
    monthly = pd.read_csv(required_files["monthly"])
    products = pd.read_csv(required_files["products"])
    customers = pd.read_csv(required_files["customers"])
    countries = pd.read_csv(required_files["countries"])
    segments = pd.read_csv(required_files["segments"])
    days = pd.read_csv(required_files["days"])
    hours = pd.read_csv(required_files["hours"])

    kpi_row = kpi.iloc[0]

    best_month = monthly.sort_values("monthly_revenue", ascending=False).iloc[0]
    lowest_month = monthly.sort_values("monthly_revenue", ascending=True).iloc[0]

    top_product = products.iloc[0]
    top_customer = customers.iloc[0]
    top_country = countries.iloc[0]
    top_segment = segments.sort_values("segment_revenue", ascending=False).iloc[0]
    top_day = days.iloc[0]
    top_hour = hours.sort_values("revenue", ascending=False).iloc[0]

    report = f"""# Business Insights Report

## Project Title

Retail & Food Services Sales Analytics Dashboard

## Executive Summary

This project analyzes transaction-level retail sales data from a UK-based online retail business. The analysis focuses on revenue trends, product performance, customer purchasing behavior, geographic sales contribution, and time-based sales patterns.

The cleaned dataset contains **{int(kpi_row["total_orders"]):,} orders**, **{int(kpi_row["total_customers"]):,} known customers**, and **{int(kpi_row["countries_served"]):,} countries served**. Total revenue after cleaning is **{format_currency(kpi_row["total_revenue"])}**.

## Key Performance Indicators

| Metric | Value |
|---|---:|
| Total Revenue | {format_currency(kpi_row["total_revenue"])} |
| Total Orders | {int(kpi_row["total_orders"]):,} |
| Total Customers | {int(kpi_row["total_customers"]):,} |
| Total Quantity Sold | {int(kpi_row["total_quantity_sold"]):,} |
| Average Order Value | {format_currency(kpi_row["average_order_value"])} |
| Countries Served | {int(kpi_row["countries_served"]):,} |

## Sales Trend Insights

- The highest revenue month was **{best_month["invoice_year_month"]}**, generating **{format_currency(best_month["monthly_revenue"])}**.
- The lowest revenue month was **{lowest_month["invoice_year_month"]}**, generating **{format_currency(lowest_month["monthly_revenue"])}**.
- Monthly sales trends can help identify seasonal demand patterns and support inventory planning.

## Product Performance Insights

- The top product by revenue was **{top_product["description"]}**, generating **{format_currency(top_product["product_revenue"])}**.
- This product sold **{int(top_product["total_quantity_sold"]):,} units** across **{int(top_product["total_orders"]):,} orders**.
- Product-level revenue analysis helps identify which items should receive priority in inventory, promotions, and merchandising decisions.

## Customer Insights

- The highest-value customer was **Customer {top_customer["customer_id"]}**, generating **{format_currency(top_customer["customer_revenue"])}**.
- This customer placed **{int(top_customer["total_orders"]):,} orders** with an average order value of **{format_currency(top_customer["average_order_value"])}**.
- The strongest customer segment by revenue was **{top_segment["customer_segment"]}**, contributing **{format_currency(top_segment["segment_revenue"])}**.

## Geographic Insights

- The top country by revenue was **{top_country["country"]}**, generating **{format_currency(top_country["country_revenue"])}**.
- This country had **{int(top_country["total_orders"]):,} orders** and **{int(top_country["total_customers"]):,} known customers**.
- Geographic revenue concentration should be considered when planning market expansion and regional campaigns.

## Time-Based Sales Insights

- The strongest sales day was **{top_day["invoice_day_name"]}**, generating **{format_currency(top_day["revenue"])}**.
- The highest revenue hour was **{int(top_hour["invoice_hour"])}:00**, generating **{format_currency(top_hour["revenue"])}**.
- Time-based patterns can support staffing, promotion timing, and operational planning.

## Business Recommendations

1. **Prioritize high-revenue products**  
   Focus inventory planning, promotions, and product placement around the highest revenue-generating products.

2. **Strengthen customer retention efforts**  
   High-value and repeat customers contribute significantly to revenue. Target these customers with loyalty offers, personalized promotions, and retention campaigns.

3. **Analyze revenue concentration by geography**  
   Since top countries contribute heavily to revenue, the business should protect strong markets while exploring growth opportunities in lower-performing regions.

4. **Use monthly trends for demand planning**  
   Peak sales months should guide inventory purchasing, staffing, and marketing campaign timing.

5. **Optimize sales timing**  
   Day-of-week and hour-of-day trends can help determine when to schedule promotions and customer outreach.

## Skills Demonstrated

- Python data cleaning
- SQL business analysis
- SQLite database creation
- KPI development
- Customer segmentation
- Product performance analysis
- Geographic analysis
- Time-based sales analysis
- Business insight communication

## Next Step

The next phase is to build an interactive Power BI dashboard using the cleaned data and SQL output summaries.
"""

    report_path.write_text(report, encoding="utf-8")
    print(f"Business insights report created: {report_path}")


if __name__ == "__main__":
    main()