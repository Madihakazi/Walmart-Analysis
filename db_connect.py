import mysql.connector
import pandas as pd

# Connect to MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='madihakazi@3107',     # replace with your MySQL password
    database='walmart_analysis'  # make sure this DB exists
)

cursor = connection.cursor()

# Load CSV data
df = pd.read_csv("cleaned_walmart.csv")

# Define the INSERT SQL query
query = """
INSERT INTO walmart 
(Store, Date, Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# Prepare list of tuples for insertion
data_to_insert = []
for index, row in df.iterrows():
    values = (
        int(row['Store']),
        row['Date'],
        float(row['Weekly_Sales']),
        int(row['Holiday_Flag']),
        float(row['Temperature']),
        float(row['Fuel_Price']),
        float(row['CPI']),
        float(row['Unemployment'])
    )
    data_to_insert.append(values)

# Execute batch insert
cursor.executemany(query, data_to_insert)
connection.commit()

print(f"{cursor.rowcount} rows inserted.")

# Close connection
cursor.close()
connection.close()
