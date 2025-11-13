import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",         # Or 127.0.0.1
    user="root",              # Your MySQL username
    password="madihakazi@3107", # Your MySQL password
    database="walmart_analysis"  # The database name where Walmart data is stored
)

# Query the table
query = "SELECT * FROM walmart LIMIT 10"  # Just view first 10 rows
df = pd.read_sql(query, conn)

# Display the result
print("Sample Walmart Data from MySQL:")
print(df)

# Close the connection
conn.close()
