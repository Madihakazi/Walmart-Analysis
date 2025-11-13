from flask import Flask, render_template, request, redirect
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import os
import numpy as np

app = Flask(__name__)

   # database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'madihakazi@3107',
    'database': 'walmart_DATABASE'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def clean_data(df):
    """Clean and prepare the data for database insertion"""
    # Flexible date parsing
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
    
    # Report invalid dates before dropping
    invalid_dates = df[df['Date'].isna()]
    if not invalid_dates.empty:
        print(f"Rows with invalid dates: {len(invalid_dates)}")
    
    # Keep only rows with valid dates
    df = df[df['Date'].notna()]
    
    # Keep only date part
    df['Date'] = df['Date'].dt.date
    
    # Replace NaN values with None for SQL
    df.replace([np.nan], [None], inplace=True)
    
    # Ensure numeric types
    df = df.astype({
        'Store': 'int',
        'Weekly_Sales': 'float',
        'Holiday_Flag': 'int',
        'Temperature': 'float',
        'Fuel_Price': 'float',
        'CPI': 'float',
        'Unemployment': 'float'
    }, errors='ignore')
    
    return df


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    try:
        # Read CSV
        df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Store', 'Date', 'Weekly_Sales', 'Holiday_Flag',
                            'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
        if not all(col in df.columns for col in required_columns):
            return "CSV file is missing required columns", 400
        
        # Clean data
        df = clean_data(df)
        
        # Connect to DB
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS walmart_SALES (
            Place VARCHAR(50),
            Store INT,
            Date DATE,
            Weekly_Sales FLOAT,
            Holiday_Flag BOOLEAN,
            Temperature FLOAT,
            Fuel_Price FLOAT,
            CPI FLOAT,
            Unemployment FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Insert data
        for _, row in df.iterrows():
            values = (
                row['Place'],
                int(row['Store']),
                row['Date'],
                float(row['Weekly_Sales']),
                int(row['Holiday_Flag']),
                float(row['Temperature']),
                float(row['Fuel_Price']),
                float(row['CPI']),
                float(row['Unemployment'])
            )
            cursor.execute("""
                INSERT INTO walmart_SALES 
                (Place, Store, Date, Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, values)
        
        conn.commit()
        
        # Generate reports
        report_data = generate_reports(df)
        
        cursor.close()
        conn.close()
        
        return render_template('report.html', **report_data)
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 400

def generate_reports(df):
    """Generate report data and visualizations"""
    os.makedirs('static', exist_ok=True)
    
    # Basic statistics
    stats = {
        'row_count': len(df),
        'start_date': df['Date'].min(),
        'end_date': df['Date'].max(),
        'total_sales': round(df['Weekly_Sales'].sum(), 2)
    }
    
    # Sales by year
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    sales_by_year = df.groupby('Year')['Weekly_Sales'].sum().reset_index()
    
    # Holiday vs Non-Holiday
    holiday_sales = round(df[df['Holiday_Flag'] == 1]['Weekly_Sales'].sum(), 2)
    non_holiday_sales = round(df[df['Holiday_Flag'] == 0]['Weekly_Sales'].sum(), 2)
    
    # Store-wise summary
    summary_df = df.groupby(['Store'])['Weekly_Sales'].sum().reset_index()
    summary_df.columns = ['Store', 'Total_Sales']
    stats['summary_table'] = summary_df.to_html(classes='table table-bordered', index=False)
    
    # Charts
    stats['bar_chart'] = generate_bar_chart(
        sales_by_year['Year'], sales_by_year['Weekly_Sales'],
        'Year', 'Total Sales ($)', 'Walmart Yearly Sales', 'yearly_sales.png'
    )
    
    stats['pie_chart'] = generate_pie_chart(
        [holiday_sales, non_holiday_sales],
        ['Holiday Sales', 'Non-Holiday Sales'],
        'Holiday vs Non-Holiday Sales',
        'holiday_sales.png'
    )
    
    stats['compare_chart'] = generate_bar_chart(
        summary_df['Store'], summary_df['Total_Sales'],
        'Store', 'Total Sales ($)', 'Store-wise Sales Comparison', 'store_sales.png'
    )
    
    return stats

def generate_bar_chart(x, y, xlabel, ylabel, title, filename):
    plt.figure(figsize=(8,5))
    plt.bar(x, y, color='#0071ce')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    path = os.path.join('static', filename)
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return filename

def generate_pie_chart(data, labels, title, filename):
    plt.figure(figsize=(6,6))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#f28e2b','#4e79a7'])
    plt.title(title)
    path = os.path.join('static', filename)
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return filename

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route("/analysis")
def analysis_page():
    return render_template("analysis.html")

@app.route('/')
def dashboard():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
