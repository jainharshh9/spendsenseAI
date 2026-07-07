# SpendSense AI - Power BI Dashboard Guide

This guide details the structure, data connection, and configurations for the **SpendSense AI** interactive Power BI dashboard (`SpendSense_AI.pbix`). 

The dashboard is designed to provide actionable business and financial insights for recruiters, demonstrating data modeling, visual storytelling, and advanced analytics capabilities.

---

## 📈 Dashboard Layout & Theme
- **Theme:** Modern Dark/Deep Blue Palette (Midnight Blue `#0f172a`, Accent Indigo `#6366f1`, Emerald Green `#10b981` for savings, Rose Red `#f43f5e` for leakages, Slate Gray for typography).
- **Format:** Recruiter-friendly executive summary layout (16:9 ratio, clear visual hierarchy, dynamic hover tooltips).

---

## 🔗 Data Connection & Refresh Instructions
To connect the dashboard to the processed dataset on your local machine:
1. Open **Power BI Desktop**.
2. Click on **Transform Data** (Home Tab) -> **Data Source Settings**.
3. Select the file source and click **Change Source**.
4. Browse and select the processed dataset: `SpendSense-AI/data/processed/cleaned_transaction_data.csv`.
5. Click **Close & Apply** to refresh and reload the data model.

---

## 🧮 DAX Measures & KPIs
The dashboard uses the following DAX measures to display high-level KPI cards:

```dax
// 1. Total Income
Total Income = CALCULATE(SUM(spendsense_transactions[Amount]), spendsense_transactions[Transaction_Type] = "Income")

// 2. Total Expense
Total Expense = CALCULATE(SUM(spendsense_transactions[Amount]), spendsense_transactions[Transaction_Type] = "Expense")

// 3. Savings (Net)
Savings = [Total Income] - [Total Expense]

// 4. Savings Percentage
Savings % = DIVIDE([Savings], [Total Income], 0) * 100

// 5. Total Leakage Spend
Total Leakage = CALCULATE(SUM(spendsense_transactions[Amount]), spendsense_transactions[is_leakage] = 1)

// 6. Leakage Percentage
Leakage % = DIVIDE([Total Leakage], [Total Expense], 0) * 100

// 7. ML Model Prediction Accuracy
Model Accuracy = 
VAR TotalExpenses = CALCULATE(COUNTROWS(spendsense_transactions), spendsense_transactions[Transaction_Type] = "Expense")
VAR CorrectPredictions = CALCULATE(COUNTROWS(spendsense_transactions), spendsense_transactions[Transaction_Type] = "Expense" && spendsense_transactions[is_leakage] = spendsense_transactions[predicted_leakage])
RETURN DIVIDE(CorrectPredictions, TotalExpenses, 0) * 100
```

---

## 📊 Dashboard Visuals & Configurations

### 1. KPI Panel (Cards)
- **Total Income:** Value in ₹ (formatted as Currency - ₹ Indian Rupee).
- **Total Expense:** Value in ₹.
- **Savings:** Emerald-colored value demonstrating net wealth retention.
- **Savings Rate (%):** Gauge chart with a target value of 25%.
- **Leakage Rate (%):** Rose-colored value showing the percentage of expenses flagged as waste.
- **Prediction Accuracy (%):** Displays the Machine Learning model's performance (~99.85%).

### 2. Interactive Slicers (Filters)
- **Salary Band:** Filter by Band A, B, C, or D.
- **Work Mode:** Office, Hybrid, or WFH.
- **Payment Method:** UPI, Credit Card, Debit Card, Net Banking, Cash.
- **Month/Year:** Dynamic date slider.

### 3. Core Visual Charts
- **Monthly Trend (Line & Clustered Column Chart):**
  - *X-axis:* Month
  - *Columns:* Total Income vs. Total Expense
  - *Line:* Savings Percentage
- **Expense Category Breakdown (Treemap):**
  - Displays proportional spending across Groceries, Rent, Utilities, Dining Out, Shopping, Commute, etc.
- **Payment Method Distribution (Donut Chart):**
  - Shows how payment mode choices relate to spending volume, highlighting that Credit Cards and UPI dominate expense counts.
- **Savings Trend (Area Chart):**
  - Illustrates the rolling accumulation of monthly savings over the 12-month period.
- **Top Leakage Categories (Clustered Bar Chart):**
  - Lists want-based categories (Gym, Shopping, Dining Out, OTT Subscriptions) ordered by total leakage volume.
- **Salary Band Analysis (Scatter Plot):**
  - *X-axis:* Monthly Income
  - *Y-axis:* Savings Percentage
  - *Size:* Transaction Count
  - Helps identify which income segments are most disciplined.
