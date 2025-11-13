import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_walmart.csv")
print(df.head())
if 'Date' in df.columns:
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df_grouped = df.groupby("Date")["Weekly_Sales"].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(df_grouped["Date"], df_grouped["Weekly_Sales"], marker='o')
plt.title("Total Weekly Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Weekly Sales")
plt.grid(True)
plt.tight_layout()
plt.show()

top_stores = df.groupby("Store")["Weekly_Sales"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
top_stores.plot(kind='bar')
plt.title("Top 10 Performing Stores")
plt.xlabel("Store Number")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.grid(True)
plt.tight_layout()
plt.show()
   
