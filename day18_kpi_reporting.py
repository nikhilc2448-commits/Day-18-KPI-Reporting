# ============================================================
# DAY 18 - KPI REPORTING
# Capstone Dataset: Customers + Orders
# ============================================================

import pandas as pd

# 1. LOAD DATA

customers = pd.read_csv("Capstone Customers.csv")
orders = pd.read_csv("Capstone Orders.csv")

print("Customers Dataset Loaded Successfully")
print("Orders Dataset Loaded Successfully")



# 2. DATA CLEANING

# Clean column names
customers.columns = customers.columns.str.strip()
orders.columns = orders.columns.str.strip()

# Clean text columns
customers["Region"] = (
    customers["Region"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

customers["Segment"] = (
    customers["Segment"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

orders["Category"] = (
    orders["Category"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

# Convert dates
customers["JoinDate"] = pd.to_datetime(
    customers["JoinDate"],
    errors="coerce"
)

orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"],
    errors="coerce"
)



# 3. MERGE DATA

df = pd.merge(
    orders,
    customers,
    on="CustomerID",
    how="inner"
)

print("\nMerged Dataset Shape:")
print(df.shape)



# KPI 1: TOTAL REVENUE

# Used by: Business owners and Finance Managers
# Helps to track overall revenue.

total_revenue = df["Sales"].sum()

print("\n================================")
print("KPI 1 - TOTAL REVENUE")
print("Total Revenue: ₹", round(total_revenue, 2))


# KPI 2: AVERAGE ORDER VALUE

# Used by: Sales and Marketing Managers
# Helps with pricing and upselling decisions.

average_order_value = (
    df["Sales"].sum() / df["OrderID"].nunique()
)

print("\n================================")
print("KPI 2 - AVERAGE ORDER VALUE")
print("Average Order Value: ₹", round(average_order_value, 2))


# KPI 3: REPEAT CUSTOMERS

# Used by: Customer Success and Marketing Teams
# Helps to understand customer loyalty.

customer_orders = (
    df.groupby("CustomerID")["OrderID"]
    .nunique()
)

repeat_customers = (customer_orders > 1).sum()

print("\n================================")
print("KPI 3 - REPEAT CUSTOMERS")
print("Repeat Customers:", repeat_customers)


# KPI 4: CUSTOMER RETENTION RATE

# Used by: Business Managers and Customer Success Teams
# Helps to measure customer retention.

total_customers = customers["CustomerID"].nunique()

retention_rate = (
    repeat_customers / total_customers
) * 100

print("\n================================")
print("KPI 4 - CUSTOMER RETENTION RATE")
print(
    "Customer Retention Rate:",
    round(retention_rate, 2),
    "%"
)


# KPI 5: REVENUE PER REGION

# Used by: Regional Managers
# Helps to compare revenue between regions.

revenue_per_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n================================")
print("KPI 5 - REVENUE PER REGION")
print(revenue_per_region)


# KPI 6: REVENUE PER CATEGORY

# Used by: Product and Category Managers
# Helps to identify top and low performing categories.

revenue_per_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n================================")
print("KPI 6 - REVENUE PER CATEGORY")
print(revenue_per_category)


# 4. COHORT ANALYSIS

# Group customers by the month they joined
# Then calculate total sales for each cohort.

df["JoinMonth"] = (
    df["JoinDate"]
    .dt.to_period("M")
    .astype(str)
)

cohort_sales = (
    df.groupby("JoinMonth")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n================================")
print("COHORT ANALYSIS - SALES BY JOIN MONTH")
print(cohort_sales)



# 5. BEST KPI

# Best KPI: Customer Retention Rate
#
# Retention rate is 100% in this dataset because all customers
# have placed more than one order.
# This shows strong repeat purchasing in the given data.
# However, a longer time period would give a better view of retention.

print("\n================================")
print("BEST KPI")
print(
    "Customer Retention Rate:",
    round(retention_rate, 2),
    "%"
)


# 6. WORST KPI

# Ignore Unknown because it represents missing region data.

known_region_revenue = revenue_per_region[
    revenue_per_region.index != "Unknown"
]

lowest_region = known_region_revenue.idxmin()
lowest_region_revenue = known_region_revenue.min()

# Worst KPI: Lowest Revenue Region
#
# East has the lowest revenue among the known regions.
# This may be due to fewer customers, lower order values,
# or lower demand.

print("\n================================")
print("WORST KPI")
print("Lowest Revenue Region:", lowest_region)
print("Revenue: ₹", round(lowest_region_revenue, 2))


# 7. INTERPRETATION QUESTION 1

# Misleading:
# "Customer retention is 100%, so the business has perfect loyalty."
#
# Honest:
# The calculation is based on customers with more than one order
# in this dataset. The data may not cover a long enough period,
# so the result should be interpreted carefully.


# 8. INTERPRETATION QUESTION 2

# A decrease is bad news when it continues over multiple periods
# and shows a clear negative trend.
#
# A small one-time decrease may just be normal variation or noise.
#
# We can compare sales across different periods, regions and
# customer cohorts to identify whether the decline continues.


# 9. END-OF-DAY CHECK

# Vanity metric:
# A metric that looks good but does not help in making decisions.
#
# Why retention matters:
# Retention shows whether customers continue buying.
# Total customer count alone does not show this.
#
# Before trusting a KPI:
# Check how it was calculated, what data was used,
# what time period it covers, and whether the data is accurate.


# 10. FINAL SUMMARY

print("\n================================")
print("FINAL KPI SUMMARY")
print("================================")

print("Total Revenue: ₹", round(total_revenue, 2))

print(
    "Average Order Value: ₹",
    round(average_order_value, 2)
)

print("Repeat Customers:", repeat_customers)

print(
    "Customer Retention Rate:",
    round(retention_rate, 2),
    "%"
)

print("\nRevenue Per Region:")
print(revenue_per_region)

print("\nRevenue Per Category:")
print(revenue_per_category)

print("\nDay 18 KPI Reporting Completed Successfully!")