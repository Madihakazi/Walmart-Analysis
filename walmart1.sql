SELECT * FROM walmart_analysis.walmart;

DESCRIBE walmart;

ALTER TABLE walmart ADD COLUMN StoreID INT;
DESCRIBE walmart;

SELECT StoreID, SUM(Weekly_Sales) 
FROM walmart 
GROUP BY StoreID;

SHOW tables;
SELECT * FROM walmart LIMIT 10;
SELECT COUNT(*) FROM walmart;
SELECT * FROM walmart LIMIT 10;





