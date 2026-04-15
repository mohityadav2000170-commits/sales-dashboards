import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Title
# =========================
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Analytics Dashboard")

# =========================
# Load Data
# =========================
df = pd.read_excel("large_sales_dataset.xlsx")

# =========================
# Data Processing
# =========================
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df["Revenue"] = df["Price"]

# =========================
# Sidebar Filters
# =========================
st.sidebar.header("🔍 Filters")

city = st.sidebar.multiselect("Select City", df["City"].unique(), default=df["City"].unique())
category = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())
channel = st.sidebar.multiselect("Select Channel", df["Channel"].unique(), default=df["Channel"].unique())

filtered_df = df[
    (df["City"].isin(city)) &
    (df["Category"].isin(category)) &
    (df["Channel"].isin(channel))
]

# =========================
# KPIs
# =========================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", int(filtered_df["Revenue"].sum()))
col2.metric("Average Price", int(filtered_df["Price"].mean()))
col3.metric("Max Sale", int(filtered_df["Price"].max()))

# =========================
# Charts
# =========================

# Category Sales
st.subheader("💰 Revenue by Category")
cat_sales = filtered_df.groupby("Category")["Revenue"].sum().reset_index()
fig1 = px.bar(cat_sales, x="Category", y="Revenue", color="Category")
st.plotly_chart(fig1, use_container_width=True)

# City Sales
st.subheader("🏙️ Sales by City")
city_sales = filtered_df.groupby("City")["Revenue"].sum().reset_index()
fig2 = px.pie(city_sales, names="City", values="Revenue")
st.plotly_chart(fig2, use_container_width=True)

# Monthly Trend
st.subheader("📈 Monthly Trend")
monthly_sales = filtered_df.groupby("Month")["Revenue"].sum().reset_index()
fig3 = px.line(monthly_sales, x="Month", y="Revenue", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# =========================
# Top Products
# =========================
st.subheader("🏆 Top 5 Products")
top_products = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)
st.dataframe(top_products)

# =========================
# Full Data
# =========================
st.subheader("📋 Full Data")
st.dataframe(filtered_df)