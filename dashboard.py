import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

st.set_page_config(page_title="Book Price Monitoring", layout="wide")

# -----------------------------
# Scraping Function
# -----------------------------
@st.cache_data
def scrape_data():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    data = []

    for page in range(1, 6):
        url = base_url.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            availability = book.find("p", class_="instock availability").text.strip()
            data.append([title, price, availability])

    df = pd.DataFrame(data, columns=["Title", "Price", "Availability"])
    df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True)
    df["Price"] = df["Price"].astype(float)

    return df

df = scrape_data()

# -----------------------------
# Anomaly Detection
# -----------------------------
mean_price = df["Price"].mean()
std_price = df["Price"].std()

df["z_score"] = (df["Price"] - mean_price) / std_price
df["Anomaly"] = df["z_score"].abs() > 2

# -----------------------------
# Dashboard UI
# -----------------------------
st.title("📊 Book Price Monitoring Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Books", len(df))
col2.metric("Average Price", round(mean_price, 2))
col3.metric("Anomalies Detected", df["Anomaly"].sum())

st.subheader("Price Distribution")

fig, ax = plt.subplots()
ax.hist(df["Price"], bins=10)
ax.set_xlabel("Price")
ax.set_ylabel("Frequency")
st.pyplot(fig)

st.subheader("Availability Breakdown")
st.bar_chart(df["Availability"].value_counts())

st.subheader("Search Book")
search = st.text_input("Enter book name")

if search:
    result = df[df["Title"].str.contains(search, case=False)]
    st.write(result)

st.subheader("Detected Price Anomalies")
st.write(df[df["Anomaly"] == True][["Title", "Price", "z_score"]])
