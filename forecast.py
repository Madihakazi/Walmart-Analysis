import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings

warnings.filterwarnings("ignore")

# Load the cleaned Walmart dataset
df = pd.read_csv("cleaned_walmart.csv")

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Group by Date to get total sales across all stores
sales_by_date = df.groupby('Date')['Weekly_Sales'].sum().reset_index()

# Set Date as index
sales_by_date.set_index('Date', inplace=True)

# Plot historical sales
sales_by_date.plot(figsize=(12, 6), title="Total Weekly Sales")
plt.ylabel("Sales")
plt.grid(True)
plt.tight_layout()
plt.show()

# Fit SARIMA model
model = SARIMAX(sales_by_date['Weekly_Sales'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 52))
results = model.fit()

# Forecast next 12 weeks
forecast = results.get_forecast(steps=12)
forecast_values = forecast.predicted_mean
conf_int = forecast.conf_int()

# Plot forecast
plt.figure(figsize=(12, 6))
plt.plot(sales_by_date.index, sales_by_date['Weekly_Sales'], label='Historical Sales')
plt.plot(forecast_values.index, forecast_values, label='Forecast', color='green')
plt.fill_between(forecast_values.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='lightgreen', alpha=0.5)
plt.title("Forecast for Next 12 Weeks")
plt.xlabel("Date")
plt.ylabel("Weekly Sales")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
