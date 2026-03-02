import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Book Price Monitoring", layout="wide")

# Load data
df = pd.read_csv("jobs_data.csv")

# Clean price
df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True)
df["Price"] = df["Price"].astype(float)

# Anomaly detection
mean_price = df["Price"].mean()
std_price = df["Price"].std()
df["z_score"] = (df["Price"] - mean_price) / std_price
df["Anomaly"] = df["z_score"].abs() > 2

# -----------------------
# Dashboard UI
# -----------------------

st.title("📊 Book Price Monitoring Dashboard")

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Books", len(df))
col2.metric("Average Price", round(mean_price, 2))
col3.metric("Anomalies Detected", df["Anomaly"].sum())

# Price Distribution
st.subheader("Price Distribution")

fig, ax = plt.subplots()
ax.hist(df["Price"], bins=10)
ax.set_xlabel("Price")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Availability Breakdown
st.subheader("Availability Status")
st.bar_chart(df["Availability"].value_counts())

# Search
st.subheader("Search Book")
search = st.text_input("Enter book name")

if search:
    result = df[df["Title"].str.contains(search, case=False)]
    st.write(result)

# Show anomalies table
st.subheader("Detected Price Anomalies")
st.write(df[df["Anomaly"] == True][["Title", "Price", "z_score"]])