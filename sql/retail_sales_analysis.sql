/*
Retail & Food Services Sales Analytics Dashboard
SQL Analysis Queries

Dataset: Online Retail Dataset
Source: UCI Machine Learning Repository

Purpose:
These SQL queries are designed to analyze transaction-level retail sales data
and support the Power BI dashboard for sales, product, customer, and geography insights.

Expected table name:
cleaned_online_retail

Main fields:
invoice_no, stock_code, description, quantity, invoice_date,
invoice_year, invoice_month, invoice_month_name, invoice_year_month,
invoice_day, invoice_day_name, invoice_hour, unit_price, total_revenue,
customer_id, known_customer, country
*/


/* ============================================================
   1. Executive KPI Summary
   ============================================================ */

-- Total revenue, orders, customers, quantity sold, and average order value
SELECT
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT CASE WHEN customer_id <> 'Unknown' THEN customer_id END) AS total_customers,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value,
    COUNT(DISTINCT country) AS countries_served
FROM cleaned_online_retail;


/* ============================================================
   2. Monthly Sales Trend
   ============================================================ */

-- Monthly revenue, orders, and quantity sold
SELECT
    invoice_year_month,
    ROUND(SUM(total_revenue), 2) AS monthly_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    SUM(quantity) AS total_quantity_sold,
    COUNT(DISTINCT CASE WHEN customer_id <> 'Unknown' THEN customer_id END) AS total_customers
FROM cleaned_online_retail
GROUP BY invoice_year_month
ORDER BY invoice_year_month;


/* ============================================================
   3. Best and Worst Sales Months
   ============================================================ */

-- Highest revenue months
SELECT
    invoice_year_month,
    ROUND(SUM(total_revenue), 2) AS monthly_revenue
FROM cleaned_online_retail
GROUP BY invoice_year_month
ORDER BY monthly_revenue DESC
LIMIT 5;

-- Lowest revenue months
SELECT
    invoice_year_month,
    ROUND(SUM(total_revenue), 2) AS monthly_revenue
FROM cleaned_online_retail
GROUP BY invoice_year_month
ORDER BY monthly_revenue ASC
LIMIT 5;


/* ============================================================
   4. Product Performance Analysis
   ============================================================ */

-- Top 10 products by revenue
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

-- Top 10 products by quantity sold
SELECT
    stock_code,
    description,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(total_revenue), 2) AS product_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders
FROM cleaned_online_retail
GROUP BY stock_code, description
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- Products with high quantity sold but low revenue
SELECT
    stock_code,
    description,
    SUM(quantity) AS total_quantity_sold,
    ROUND(SUM(total_revenue), 2) AS product_revenue,
    ROUND(AVG(unit_price), 2) AS average_unit_price
FROM cleaned_online_retail
GROUP BY stock_code, description
HAVING SUM(quantity) > 1000
ORDER BY product_revenue ASC
LIMIT 10;


/* ============================================================
   5. Customer Analysis
   ============================================================ */

-- Top 10 customers by revenue
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

-- Repeat customer behavior
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


/* ============================================================
   6. Geographic Sales Analysis
   ============================================================ */

-- Revenue by country
SELECT
    country,
    ROUND(SUM(total_revenue), 2) AS country_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT CASE WHEN customer_id <> 'Unknown' THEN customer_id END) AS total_customers,
    SUM(quantity) AS total_quantity_sold
FROM cleaned_online_retail
GROUP BY country
ORDER BY country_revenue DESC;

-- Country revenue contribution percentage
SELECT
    country,
    ROUND(SUM(total_revenue), 2) AS country_revenue,
    ROUND(
        SUM(total_revenue) * 100.0 / (
            SELECT SUM(total_revenue)
            FROM cleaned_online_retail
        ),
        2
    ) AS revenue_percentage
FROM cleaned_online_retail
GROUP BY country
ORDER BY country_revenue DESC;


/* ============================================================
   7. Time-Based Sales Analysis
   ============================================================ */

-- Revenue by day of week
SELECT
    invoice_day_name,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    SUM(quantity) AS total_quantity_sold
FROM cleaned_online_retail
GROUP BY invoice_day_name
ORDER BY revenue DESC;

-- Revenue by hour of day
SELECT
    invoice_hour,
    ROUND(SUM(total_revenue), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    SUM(quantity) AS total_quantity_sold
FROM cleaned_online_retail
GROUP BY invoice_hour
ORDER BY invoice_hour;


/* ============================================================
   8. Business Insight Queries
   ============================================================ */

-- Average revenue per country
SELECT
    country,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    ROUND(SUM(total_revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
FROM cleaned_online_retail
GROUP BY country
HAVING COUNT(DISTINCT invoice_no) >= 10
ORDER BY average_order_value DESC;

-- Products appearing in the most orders
SELECT
    stock_code,
    description,
    COUNT(DISTINCT invoice_no) AS order_frequency,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    SUM(quantity) AS total_quantity_sold
FROM cleaned_online_retail
GROUP BY stock_code, description
ORDER BY order_frequency DESC
LIMIT 10;