CREATE DATABASE walmart_analysis;
USE walmart_analysis;

CREATE TABLE walmart_merged (
    Store INT,
    Date DATE,
    Weekly_Sales FLOAT,
    Holiday_Flag BOOLEAN,
    Temperature FLOAT,
    Fuel_Price FLOAT,
    CPI FLOAT,
    Unemployment FLOAT
);
USE walmart_analysis;
SHOW TABLES;
SELECT * FROM walmart_sales LIMIT 10;
show variables like 'datadir';
show table status like 'walmart_sales';

SELECT * FROM walmart_sales LIMIT 10;
DELETE FROM walmart_sales WHERE Place ='Gautemala';
SELECT * FROM walmart_sales WHERE Place ='Gautemala' limit 1000;
SELECT * FROM walmart_sales WHERE Place ='Gautemala' limit 1000;
