CREATE DATABASE walmart_db;
USE walmart_db;
CREATE TABLE walmart (
    Store INT,
    Date DATE,
    Weekly_Sales FLOAT,
    Holiday_Flag BOOLEAN,
    Temperature FLOAT,
    Fuel_Price FLOAT,
    CPI FLOAT,
    Unemployment FLOAT
);
USE walmart_db;
SHOW TABLES;
SELECT * FROM walmart_db.walmart;
DESCRIBE walmart;
ALTER TABLE walmart ADD COLUMN StoreID INT;
DESCRIBE walmart;
SELECT StoreID, SUM(Weekly_Sales) 
FROM walmart 
GROUP BY StoreID;
SHOW tables;
SELECT * FROM walmart LIMIT 10;
