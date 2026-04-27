/*
Retail & Food Services Sales Analytics Dashboard
SQL Analysis Queries

Dataset: Online Retail Dataset
Source: UCI Machine Learning Repository

This file will contain business analysis queries used for dashboard planning and insight generation.
*/

-- 1. Total revenue
-- SELECT SUM(total_revenue) AS total_revenue
-- FROM cleaned_online_retail;

-- 2. Monthly revenue trend
-- SELECT invoice_year, invoice_month, SUM(total_revenue) AS monthly_revenue
-- FROM cleaned_online_retail
-- GROUP BY invoice_year, invoice_month
-- ORDER BY invoice_year, invoice_month;

-- 3. Top products by revenue
-- SELECT description, SUM(total_revenue) AS product_revenue
-- FROM cleaned_online_retail
-- GROUP BY description
-- ORDER BY product_revenue DESC
-- LIMIT 10;
