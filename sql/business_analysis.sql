-- ==========================================
-- SpendSense AI: Simple SQL Business Queries
-- Target Table: spendsense_transactions
-- ==========================================


-- 1. TOTAL INCOME, EXPENSE & INVESTMENT
-- Objective: Find the total amount for each transaction type.

SELECT 
    Transaction_Type,
    SUM(Amount) AS Total_Amount
FROM spendsense_transactions
GROUP BY Transaction_Type;


-- 2. SPENDING BY CATEGORY
-- Objective: Find which expense categories have the highest spending.

SELECT 
    Category,
    SUM(Amount) AS Total_Spending
FROM spendsense_transactions
WHERE Transaction_Type = 'Expense'
GROUP BY Category
ORDER BY Total_Spending DESC;


-- 3. WANT VS NEED SPENDING
-- Objective: Compare spending on Wants and Needs.

SELECT 
    Expense_Type,
    SUM(Amount) AS Total_Spending
FROM spendsense_transactions
WHERE Transaction_Type = 'Expense'
GROUP BY Expense_Type;


-- 4. LEAKAGE SPENDING BY CATEGORY
-- Objective: Identify categories where unnecessary spending is highest.

SELECT 
    Category,
    SUM(Amount) AS Leakage_Amount
FROM spendsense_transactions
WHERE Transaction_Type = 'Expense'
  AND is_leakage = 1
GROUP BY Category
ORDER BY Leakage_Amount DESC;


-- 5. SPENDING BY PAYMENT METHOD
-- Objective: Find spending and number of transactions for each payment method.

SELECT 
    Payment_Method,
    COUNT(*) AS Total_Transactions,
    SUM(Amount) AS Total_Spending
FROM spendsense_transactions
WHERE Transaction_Type = 'Expense'
GROUP BY Payment_Method
ORDER BY Total_Spending DESC;


-- 6. EMPLOYEE-WISE SPENDING
-- Objective: Find which employees have the highest total spending.

SELECT 
    Employee_ID,
    SUM(Amount) AS Total_Spending
FROM spendsense_transactions
WHERE Transaction_Type = 'Expense'
GROUP BY Employee_ID
ORDER BY Total_Spending DESC;
  




   



  
    
