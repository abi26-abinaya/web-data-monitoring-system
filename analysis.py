import pandas as pd
import os

# Load data safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "jobs_data.csv")

df = pd.read_csv(file_path)

print("Raw Data:")
print(df.head())

# -----------------------
# Data Cleaning
# -----------------------

# Remove currency symbols & weird characters
df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True)
df["Price"] = df["Price"].astype(float)

print("\nCleaned Data:")
print(df.head())

# -----------------------
# Data Quality Checks
# -----------------------

print("\nMissing Values:")
print(df.isnull().sum())

# -----------------------
# Basic Analysis
# -----------------------

print("\nSummary Statistics:")
print(df["Price"].describe())

# -----------------------
# Anomaly Detection (Z-score)
# -----------------------

mean_price = df["Price"].mean()
std_price = df["Price"].std()

df["z_score"] = (df["Price"] - mean_price) / std_price

outliers = df[df["z_score"].abs() > 2]

print("\nPotential Price Anomalies:")
print(outliers[["Title", "Price", "z_score"]])