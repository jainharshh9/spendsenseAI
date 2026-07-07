-- ==========================================
-- SpendSense AI: SQL Business Analytics Queries
-- Target Table: spendsense_transactions
-- Designed for recruiter-ready portfolio presentation.
-- Focuses on CTEs, Window Functions, LAG, DENSE_RANK, MoM analysis.
-- ==========================================

-- 1. MONTHLY CASH FLOW & SAVINGS TRENDS (CTE)
-- Objective: Calculate total income, expenses, and savings rate per month to check the overall financial health of corporate professionals.
WITH MonthlyAggregates AS (
    SELECT 
        STRFTIME('%Y-%m', Date) AS Month_Year,
        SUM(CASE WHEN Transaction_Type = 'Income' THEN Amount ELSE 0 END) AS Total_Income,
        SUM(CASE WHEN Transaction_Type = 'Expense' THEN Amount ELSE 0 END) AS Total_Expense,
        SUM(CASE WHEN Transaction_Type = 'Investment' THEN Amount ELSE 0 END) AS Total_Investment
    FROM spendsense_transactions
    GROUP BY Month_Year
)
SELECT 
    Month_Year,
    Total_Income,
    Total_Expense,
    Total_Investment,
    (Total_Income - Total_Expense) AS Net_Savings,
    ROUND(((Total_Income - Total_Expense) * 100.0) / Total_Income, 2) AS Savings_Rate_Pct
FROM MonthlyAggregates
ORDER BY Month_Year;


-- 2. TOP LEAKAGE CATEGORIES RANKED BY TOTAL SPEND (DENSE_RANK)
-- Objective: Rank each expense category based on the total leakage amount to identify the biggest areas of waste.
WITH CategoryLeakage AS (
    SELECT 
        Category,
        SUM(Amount) AS Total_Leakage_Spend,
        COUNT(*) AS Transaction_Count,
        ROUND(AVG(Amount), 2) AS Avg_Leakage_Amount
    FROM spendsense_transactions
    WHERE Transaction_Type = 'Expense' AND is_leakage = 1
    GROUP BY Category
)
SELECT 
    DENSE_RANK() OVER (ORDER BY Total_Leakage_Spend DESC) AS Leakage_Rank,
    Category,
    Total_Leakage_Spend,
    Transaction_Count,
    Avg_Leakage_Amount
FROM CategoryLeakage
ORDER BY Leakage_Rank;


-- 3. MONTH-OVER-MONTH GROWTH IN EXPENSE LEAKAGE (LAG)
-- Objective: Track if leakage spending is increasing or decreasing month-over-month.
WITH MonthlyLeakage AS (
    SELECT 
        STRFTIME('%Y-%m', Date) AS Month_Year,
        SUM(Amount) AS Monthly_Leakage_Spend
    FROM spendsense_transactions
    WHERE Transaction_Type = 'Expense' AND is_leakage = 1
    GROUP BY Month_Year
),
MoM_Comparison AS (
    SELECT 
        Month_Year,
        Monthly_Leakage_Spend,
        LAG(Monthly_Leakage_Spend, 1) OVER (ORDER BY Month_Year) AS Previous_Month_Leakage
    FROM MonthlyLeakage
)
SELECT 
    Month_Year,
    Monthly_Leakage_Spend,
    COALESCE(Previous_Month_Leakage, 0) AS Previous_Month_Leakage,
    CASE 
        WHEN Previous_Month_Leakage IS NULL THEN 'N/A - Baseline'
        ELSE ROUND(((Monthly_Leakage_Spend - Previous_Month_Leakage) * 100.0) / Previous_Month_Leakage, 2) || '%'
    END AS MoM_Leakage_Growth_Pct
FROM MoM_Comparison;


-- 4. RUNNING TOTAL OF CUMULATIVE SAVINGS FOR SELECTED EMPLOYEES
-- Objective: Demonstrate a running total (rolling accumulation) of savings over the months for high-saving employees.
WITH EmployeeMonthlySavings AS (
    SELECT 
        Employee_ID,
        STRFTIME('%Y-%m', Date) AS Month_Year,
        -- Savings is Income - Expense
        SUM(CASE WHEN Transaction_Type = 'Income' THEN Amount ELSE 0 END) - 
        SUM(CASE WHEN Transaction_Type = 'Expense' THEN Amount ELSE 0 END) AS Monthly_Savings
    FROM spendsense_transactions
    GROUP BY Employee_ID, Month_Year
)
SELECT 
    Employee_ID,
    Month_Year,
    Monthly_Savings,
    SUM(Monthly_Savings) OVER (PARTITION BY Employee_ID ORDER BY Month_Year) AS Cumulative_Savings_Running_Total
FROM EmployeeMonthlySavings
WHERE Employee_ID IN ('EMP1001', 'EMP1002', 'EMP1003')
ORDER BY Employee_ID, Month_Year;


-- 5. BUDGET VS. ACTUAL SPENDING BY EXPENSE TYPE
-- Objective: Compare actual wants spending against a fixed recommended budget (e.g., 30% of Income) per Salary Band.
WITH BandBudgets AS (
    -- Group by employee to find their fixed salary and actual want spending
    SELECT 
        Employee_ID,
        Salary_Band,
        Monthly_Salary,
        -- 30% Want Budget Rule
        ROUND(Monthly_Salary * 0.30) AS Monthly_Wants_Budget,
        SUM(CASE WHEN Expense_Type = 'Want' THEN Amount ELSE 0 END) / 12.0 AS Avg_Monthly_Wants_Spend
    FROM spendsense_transactions
    GROUP BY Employee_ID, Salary_Band, Monthly_Salary
)
SELECT 
    Salary_Band,
    ROUND(AVG(Monthly_Wants_Budget), 2) AS Avg_Monthly_Wants_Budget,
    ROUND(AVG(Avg_Monthly_Wants_Spend), 2) AS Actual_Avg_Wants_Spend,
    ROUND(AVG(Avg_Monthly_Wants_Spend - Monthly_Wants_Budget), 2) AS Budget_Variance,
    CASE 
        WHEN AVG(Avg_Monthly_Wants_Spend) > AVG(Monthly_Wants_Budget) THEN 'Over Budget (Action Required)'
        ELSE 'Under Budget (Good Discipline)'
    END AS Budget_Status
FROM BandBudgets
GROUP BY Salary_Band
ORDER BY Avg_Monthly_Wants_Budget DESC;


-- 6. RISK ANALYSIS: LEAKAGE TRANSACTION RATE BY PAYMENT CHANNEL (RANK)
-- Objective: Identify which payment channels are associated with the highest rate of impulse leakage transactions.
WITH ChannelMetrics AS (
    SELECT 
        Payment_Method,
        COUNT(*) AS Total_Transactions,
        SUM(CASE WHEN is_leakage = 1 THEN 1 ELSE 0 END) AS Leakage_Transactions,
        SUM(CASE WHEN is_leakage = 1 THEN Amount ELSE 0 END) AS Total_Leakage_Amount
    FROM spendsense_transactions
    WHERE Transaction_Type = 'Expense'
    GROUP BY Payment_Method
),
ChannelRates AS (
    SELECT 
        Payment_Method,
        Total_Transactions,
        Leakage_Transactions,
        Total_Leakage_Amount,
        ROUND((Leakage_Transactions * 100.0) / Total_Transactions, 2) AS Leakage_Rate_Pct
    FROM ChannelMetrics
)
SELECT 
    RANK() OVER (ORDER BY Leakage_Rate_Pct DESC) AS Channel_Risk_Rank,
    Payment_Method,
    Total_Transactions,
    Leakage_Transactions,
    Total_Leakage_Amount,
    Leakage_Rate_Pct
FROM ChannelRates
ORDER BY Channel_Risk_Rank;


-- 7. RECURRING DISCRETIONARY MERCHANTS ANALYSIS
-- Objective: Highlight recurring unwanted monthly subscription payments that deplete savings.
SELECT 
    Merchant,
    Category,
    COUNT(DISTINCT Employee_ID) AS Subscribed_Users_Count,
    SUM(Amount) AS Total_Annual_Leakage_Spend,
    ROUND(AVG(Amount), 2) AS Avg_Subscription_Amount
FROM spendsense_transactions
WHERE Transaction_Type = 'Expense' 
  AND Subscription = 'Yes' 
  AND Expense_Type = 'Want'
GROUP BY Merchant, Category
ORDER BY Total_Annual_Leakage_Spend DESC;


-- 8. WORK MODE IMPACT ON SPENDING BEHAVIOR
-- Objective: Compare average daily discretionary transaction values for employees across work modes.
WITH EmployeeDailySpends AS (
    SELECT 
        Employee_ID,
        Work_Mode,
        Date,
        SUM(Amount) AS Daily_Discretionary_Spend
    FROM spendsense_transactions
    WHERE Transaction_Type = 'Expense' AND Expense_Type = 'Want'
    GROUP BY Employee_ID, Work_Mode, Date
)
SELECT 
    Work_Mode,
    ROUND(AVG(Daily_Discretionary_Spend), 2) AS Avg_Daily_Discretionary_Spend,
    MAX(Daily_Discretionary_Spend) AS Max_Discretionary_Spend_In_A_Day,
    COUNT(DISTINCT Employee_ID) AS Total_Employees_Represented
FROM EmployeeDailySpends
GROUP BY Work_Mode
ORDER BY Avg_Daily_Discretionary_Spend DESC;
