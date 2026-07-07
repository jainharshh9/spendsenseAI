# SpendSense AI: Financial Leakage Detection for Corporate Professionals
## Executive Business & Technical Analysis Report
**Author:** Portfolio Project (Data & Business Analyst)  
**Date:** July 2026  
**Status:** Complete  

---

## 1. Executive Summary & Business Problem

Salaried corporate professionals in India (earning between ₹35,000 and ₹1,50,000 per month) frequently struggle with "saving leakages"—small, frequent, non-essential expenditures that accumulate over time and silently deplete monthly savings. While large fixed expenses (like rent, utilities, and EMIs) are easy to track, discretionary habits such as weekend dining, frictionless UPI/Credit Card transactions, duplicate subscriptions, and office-commute coffee runs go unnoticed.

**SpendSense AI** is an end-to-end data analytics and machine learning solution designed to address this problem. By analyzing a simulated dataset of **500 corporate employees** over 12 months (~156,700 transactions), this project:
- Identifies where unnecessary money is being spent.
- Isolates behavioral patterns (weekends vs. weekdays, salary weeks vs. mid-month, work-from-home vs. office days).
- Implements a machine learning classifier to predict potential expense leakage.
- Delivers a Power BI dashboard to help users visualize and reclaim their savings.

---

## 2. Dataset & Methodology
*Disclaimer: The dataset used is synthetically generated for educational and portfolio demonstration purposes.*

The dataset models a diverse corporate workforce categorized into four Salary Bands:
- **Band A (₹35k-50k):** Entry-level Analyst/Associate (~40% of users)
- **Band B (₹50k-80k):** Senior Analyst/Specialist (~30% of users)
- **Band C (₹80k-120k):** Team Lead/Consultant (~20% of users)
- **Band D (₹120k-150k):** Manager/Senior Consultant (~10% of users)

### Columns Generated:
- `Transaction_ID`, `Employee_ID`, `Date`, `Transaction_Type` (Income, Expense, Investment), `Category`, `Amount`, `Merchant`, `Payment_Method` (UPI, Credit Card, Debit Card, Net Banking, Cash), `Work_Mode` (Office, Hybrid, WFH), `Expense_Type` (Need, Want), `Subscription` (Yes, No), `Time_of_Day`.
- **Derived Features:** `Weekend_Flag` (Saturday/Sunday transactions), `Salary_Week` (first week after salary credit, Day 1 to 7).

---

## 3. Exploratory Data Analysis (EDA) Findings

The Python EDA revealed several critical spend behaviors:
1. **Expense Breakdown (Needs vs. Wants):** Discretionary "Want" spending accounts for approximately **35.4%** of the workforce's overall spending.
2. **Monthly Savings Rate:** The organizational savings rate is stable between **20.1% and 21.0%** of monthly income.
3. **Frictionless Payment Spikes:** UPI and Credit Cards account for **over 70%** of all transactions. Credit Cards show an average transaction value of ₹3,100, indicating high discretionary spending, while UPI dominates high-frequency micro-spends.
4. **Work Mode Impact:** Employees working in **Work From Home (WFH)** mode show the highest average daily discretionary spend (₹2,047.45) due to high-frequency food deliveries and online shopping, compared to Office-based employees (₹1,706.08) and Hybrid employees (₹1,908.80).
5. **Salary Week Splurge:** During the first week of the month (salary week), discretionary want spending values increase by **30-50%**, reflecting a strong post-salary splurging effect.
6. **Weekend Effect:** Average transaction values on weekends increase by **20%** compared to weekdays in the "Dining Out" and "Shopping" categories.

---

## 4. SQL Business Analytics Insights

A total of 8 business-focused SQL queries were developed and run. The highlights include:
- **Top Leakage Categories:** The biggest leakage areas by annual spend are:
  1. *Gym Memberships:* ₹12.99M (High rate of inactive, unused memberships)
  2. *Shopping:* ₹10.17M (Impulse buying on Amazon/Myntra)
  3. *Dining Out:* ₹9.43M (Weekend dinners/drinks)
  4. *Food Delivery:* ₹4.72M (Swiggy/Zomato orders)
  5. *OTT Subscriptions:* ₹2.93M (Multiple active streaming services)
- **MoM Leakage Trend:** Leakage spend peaked in March (₹3.52M) and hit a low in May (₹3.29M), reflecting seasonal variations and festive cycles.
- **Payment Method Risk Index:**
  - *Credit Cards* carry the highest leakage rate (**41.87%** of transactions are classified as leakages).
  - *UPI* is second at **26.71%**.
  - *Cash* is at **8.67%**, and *Debit Cards/Net Banking* are under **2%**, reflecting that debit-linked channels introduce spending friction.
- **Unused Subscription Bleed:** Unused annual gym subscriptions (Cult.fit, Gold Gym) and OTT platforms (Netflix, Spotify, YouTube Premium) accounted for over ₹15.9M in leakage.

---

## 5. Machine Learning Results

To flag transactions as leakage, we trained two binary classification models using the features: `Salary_Band`, `Monthly_Salary`, `Work_Mode`, `Category`, `Amount`, `Payment_Method`, `Weekend_Flag`, `Salary_Week`, `Subscription`, and `Time_of_Day`.
*Note: To avoid target leakage, `leakage_score` and `Expense_Type` were completely dropped prior to training.*

### Model Performance Comparison:
| Metric | Logistic Regression | Random Forest Classifier |
| :--- | :---: | :---: |
| **Accuracy** | 99.50% | **99.85%** |
| **Precision** | 98.19% | **99.20%** |
| **Recall** | 99.19% | **100.00%** |
| **F1 Score** | 98.69% | **99.60%** |
| **ROC-AUC** | 99.98% | **100.00%** |

### Explainability & Feature Importance:
The Random Forest model identified the top 3 most important features for predicting leakage:
1. **Amount:** Larger discretionary spend values are highly predictive of leakage.
2. **Category_Shopping:** Online shopping categories show high leakage probability.
3. **Weekend_Flag_Yes:** Transactions on weekends have strong associations with leakage behavior.

---

## 6. Power BI Dashboard Summary

The Power BI dashboard `SpendSense_AI.pbix` contains an interactive executive interface:
- **KPI Cards:** Shows organization-wide metrics including Total Income, Total Expenses, Net Savings, Savings %, and Leakage % (~10.9% of total spending).
- **Interactive Filters:** Recruiters can filter all charts by *Work Mode*, *Salary Band*, *Payment Method*, and *Month*.
- **Core Charts:** Includes Monthly Cash Flow trend, Expense Category Treemap, Payment Method Donut chart, and Top Leakage Categories bar chart.

---

## 7. Actionable Recommendations & Business Impact

Based on the rule-based patterns and machine learning predictions, corporate professionals can reclaim **₹5,000 – ₹15,000 per month** by adopting these targeted policies:

1. **Credit Card & UPI Caps:** Place a monthly transaction limit of ₹10,000 on credit cards for discretionary categories, and disable UPI auto-pay features.
2. **Unsubscribe Auditing:** Conduct a quarterly check on subscription services. Consolidate OTT platforms and replace unused annual gym packages with per-session memberships.
3. **The "48-Hour Shopping Rule":** Keep want-based items in online shopping carts for 48 hours before purchasing to eliminate impulsive buy decisions.
4. **Post-Salary Discipline:** Establish an automated SIP (Systematic Investment Plan) that debits 20-30% of income on the 1st or 2nd day of the month, enforcing savings before discretionary spending can occur.

### Business Impact:
Implementing these steps and reducing the top 10% leakage transactions by half will increase the average professional's savings rate from **20% to over 26%**, representing an extra **₹60,000 – ₹1,80,000** in annual wealth accumulation!
