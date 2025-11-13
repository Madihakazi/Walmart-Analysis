import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="madihakazi@3107",        
    database="walmart_analysis"   
)

# Read the full dataset
query = "SELECT * FROM walmart"  
df = pd.read_sql(query, conn)
conn.close()

# Basic overview
print("Original Data Shape:", df.shape)
print("\nColumn Info:")
print(df.info())
print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Rows:", df.duplicated().sum())

# Drop duplicates
df = df.drop_duplicates()

df.to_csv("cleaned_walmart.csv", index=False)

print("\nCleaned data saved as 'cleaned_walmart.csv'")
