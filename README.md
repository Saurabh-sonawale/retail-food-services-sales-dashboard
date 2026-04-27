# Retail & Food Services Sales Analytics Dashboard

## Project Status
In Progress

## Project Overview

This project analyzes transaction-level retail sales data to uncover revenue trends, customer purchasing behavior, product performance, and geographic sales patterns.

The goal is to build a professional business intelligence dashboard that helps stakeholders understand what drives sales performance and where business opportunities exist.

## Business Problem

Retail and food service businesses need to understand which products, customers, regions, and time periods generate the most revenue. Without a clear analytics dashboard, it becomes difficult to identify growth opportunities, underperforming areas, and customer purchasing patterns.

This project solves that problem by transforming raw transaction data into actionable business insights using SQL, Python, and Power BI.

## Objectives

- Clean and prepare raw transaction data
- Analyze monthly revenue trends
- Identify top-selling and low-performing products
- Measure customer purchasing behavior
- Analyze revenue by country
- Build an interactive Power BI dashboard
- Provide business recommendations based on insights

## Dataset

Dataset: Online Retail Dataset  
Source: UCI Machine Learning Repository

The dataset contains transactions from a UK-based online retail business between December 2010 and December 2011. It includes invoice details, product information, quantity sold, invoice date, unit price, customer ID, and country.

## Tools Used

- SQL
- Python
- Pandas
- Power BI
- DAX
- Excel
- GitHub

## Key Business Questions

1. What is the total revenue generated?
2. Which months had the highest and lowest sales?
3. Which products generated the most revenue?
4. Which countries contributed the most sales?
5. Who are the highest-value customers?
6. What is the average order value?
7. Which products had high quantity sold but low revenue?
8. What business recommendations can improve sales performance?

## Planned Dashboard Pages

### 1. Executive Summary
- Total revenue
- Total orders
- Total customers
- Average order value
- Monthly revenue trend

### 2. Product Performance
- Top products by revenue
- Top products by quantity sold
- Low-performing products
- Product contribution analysis

### 3. Customer Analysis
- Top customers by revenue
- Repeat purchase behavior
- Customer segmentation
- RFM analysis

### 4. Geographic Analysis
- Revenue by country
- Orders by country
- Customer distribution by country

## Project Workflow

1. Data collection
2. Data cleaning with Python
3. Exploratory data analysis
4. SQL-based business analysis
5. Power BI dashboard development
6. Insight generation
7. Business recommendations
8. Portfolio integration

## Repository Structure

```text
retail-food-services-sales-dashboard/
│
├── README.md
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── data_cleaning_and_eda.ipynb
│
├── sql/
│   └── retail_sales_analysis.sql
│
├── dashboard/
│   ├── screenshots/
│   └── powerbi/
│
├── reports/
│   └── business_insights.md
│
└── requirements.txt
