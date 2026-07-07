import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

# Set style for visuals
sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

def run_analysis_and_export():
    print("Loading raw transaction data...")
    raw_path = "C:/Users/AdminHK/.gemini/antigravity/scratch/SpendSense-AI/data/raw/raw_transaction_data.csv"
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data not found at {raw_path}")
        
    df = pd.read_csv(raw_path)
    
    # ------------------ Data Cleaning ------------------
    print("Performing data cleaning...")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Day_of_Week'] = df['Date'].dt.day_name()
    
    # ------------------ Feature Engineering ------------------
    print("Performing feature engineering...")
    # 1. Weekend Flag (Yes/No)
    df['Weekend_Flag'] = df['Date'].dt.weekday.apply(lambda x: 'Yes' if x >= 5 else 'No')
    
    # 2. Salary Week Flag (Yes/No) - Day 1 to 7
    df['Salary_Week'] = df['Date'].dt.day.apply(lambda x: 'Yes' if x <= 7 else 'No')
    
    # 3. Calculate Monthly savings and savings percentage per employee
    # Income per employee per month
    income_df = df[df['Transaction_Type'] == 'Income'].groupby(['Employee_ID', 'Year', 'Month'])['Amount'].sum().reset_index()
    income_df.rename(columns={'Amount': 'Monthly_Income'}, inplace=True)
    
    # Expense per employee per month
    expense_df = df[df['Transaction_Type'] == 'Expense'].groupby(['Employee_ID', 'Year', 'Month'])['Amount'].sum().reset_index()
    expense_df.rename(columns={'Amount': 'Monthly_Expense'}, inplace=True)
    
    # Investment per employee per month
    invest_df = df[df['Transaction_Type'] == 'Investment'].groupby(['Employee_ID', 'Year', 'Month'])['Amount'].sum().reset_index()
    invest_df.rename(columns={'Amount': 'Monthly_Investment'}, inplace=True)
    
    # Merge monthly aggregates
    monthly_summary = pd.merge(income_df, expense_df, on=['Employee_ID', 'Year', 'Month'], how='left').fillna(0)
    monthly_summary = pd.merge(monthly_summary, invest_df, on=['Employee_ID', 'Year', 'Month'], how='left').fillna(0)
    
    # Monthly Savings = Income - Expense
    monthly_summary['Monthly_Savings'] = monthly_summary['Monthly_Income'] - monthly_summary['Monthly_Expense']
    monthly_summary['Savings_Percentage'] = (monthly_summary['Monthly_Savings'] / monthly_summary['Monthly_Income']) * 100
    monthly_summary['Savings_Percentage'] = monthly_summary['Savings_Percentage'].fillna(0)
    
    # Merge back to main dataframe
    df = pd.merge(df, monthly_summary[['Employee_ID', 'Year', 'Month', 'Monthly_Expense', 'Monthly_Savings', 'Savings_Percentage']], 
                  on=['Employee_ID', 'Year', 'Month'], how='left')
    
    # 4. Synthesize ground truth target variable 'is_leakage' using rule-based scoring
    # Rules:
    # - If Expense_Type == 'Want' (+2)
    # - If Weekend_Flag == 'Yes' AND Expense_Type == 'Want' (+2)
    # - If Subscription == 'Yes' AND Expense_Type == 'Want' (+2)
    # - If Amount < 300 AND Expense_Type == 'Want' (+1) (micro spend want)
    # - If Salary_Week == 'Yes' AND Expense_Type == 'Want' (+1) (post salary week splurge)
    # - If Payment_Method in ['Credit Card', 'UPI'] AND Expense_Type == 'Want' (+1)
    
    def calculate_leakage_score(row):
        if row['Transaction_Type'] != 'Expense':
            return 0
        score = 0
        if row['Expense_Type'] == 'Want':
            score += 2
            if row['Weekend_Flag'] == 'Yes':
                score += 2
            if row['Subscription'] == 'Yes':
                score += 2
            if row['Amount'] < 300:
                score += 1
            if row['Salary_Week'] == 'Yes':
                score += 1
            if row['Payment_Method'] in ['Credit Card', 'UPI']:
                score += 1
        return score

    df['leakage_score'] = df.apply(calculate_leakage_score, axis=1)
    df['is_leakage'] = df['leakage_score'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Generate rule-based explanations for leakage
    def get_leakage_reason(row):
        if row['is_leakage'] == 0:
            return "Normal Spend"
        reasons = []
        if row['Weekend_Flag'] == 'Yes':
            reasons.append("Weekend spending spike")
        if row['Subscription'] == 'Yes':
            reasons.append("Discretionary subscription charge")
        if row['Amount'] < 300:
            reasons.append("Unnecessary micro-expense")
        if row['Salary_Week'] == 'Yes':
            reasons.append("Post-salary week splurging")
        if row['Payment_Method'] in ['Credit Card', 'UPI']:
            reasons.append("High-convenience digital transaction")
        return "Potential Leakage due to: " + ", ".join(reasons) if reasons else "High discretionary spend"

    df['leakage_reason'] = df.apply(get_leakage_reason, axis=1)
    
    # ------------------ Exploratory Data Analysis (EDA) ------------------
    print("Generating EDA charts...")
    os.makedirs("C:/Users/AdminHK/.gemini/antigravity/scratch/SpendSense-AI/images", exist_ok=True)
    images_dir = "C:/Users/AdminHK/.gemini/antigravity/scratch/SpendSense-AI/images"
    
    # 1. Monthly Spending Trend
    plt.figure()
    monthly_spend_total = df[df['Transaction_Type']=='Expense'].groupby(['Year', 'Month'])['Amount'].sum().reset_index()
    monthly_spend_total['Date_Str'] = monthly_spend_total.apply(lambda r: f"{int(r['Year'])}-{int(r['Month']):02d}", axis=1)
    sns.lineplot(data=monthly_spend_total, x='Date_Str', y='Amount', marker='o', color='#3f51b5', linewidth=2.5)
    plt.title('Monthly Expense Trend (All Employees)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Spend (₹)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/monthly_spending_trend.png", dpi=150)
    plt.close()
    
    # 2. Monthly Savings Trend
    plt.figure()
    monthly_savings_total = df.groupby(['Year', 'Month'])['Monthly_Savings'].mean().reset_index()
    monthly_savings_total['Date_Str'] = monthly_savings_total.apply(lambda r: f"{int(r['Year'])}-{int(r['Month']):02d}", axis=1)
    sns.lineplot(data=monthly_savings_total, x='Date_Str', y='Monthly_Savings', marker='s', color='#2e7d32', linewidth=2.5)
    plt.title('Average Monthly Savings Trend per Professional', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Average Savings (₹)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/monthly_savings_trend.png", dpi=150)
    plt.close()
    
    # 3. Need vs Want Spend Analysis
    plt.figure()
    need_want_spend = df[df['Transaction_Type']=='Expense'].groupby('Expense_Type')['Amount'].sum().reset_index()
    colors = ['#1565c0', '#e53935']
    plt.pie(need_want_spend['Amount'], labels=need_want_spend['Expense_Type'], autopct='%1.1f%%', startangle=90, 
            colors=colors, textprops={'fontsize': 12, 'weight': 'bold'}, explode=(0.05, 0))
    plt.title('Expense Breakdown: Needs vs Wants', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/need_vs_want_pie.png", dpi=150)
    plt.close()
    
    # 4. Weekend vs Weekday Spending
    plt.figure()
    weekend_spend = df[df['Transaction_Type']=='Expense'].groupby(['Weekend_Flag', 'Category'])['Amount'].mean().reset_index()
    sns.barplot(data=weekend_spend, x='Category', y='Amount', hue='Weekend_Flag', palette='muted')
    plt.title('Average Category Spend: Weekdays vs Weekends', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Average Transaction Amount (₹)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/weekend_vs_weekday_spend.png", dpi=150)
    plt.close()
    
    # 5. Payment Method Distribution
    plt.figure()
    pm_counts = df[df['Transaction_Type']=='Expense']['Payment_Method'].value_counts().reset_index()
    sns.barplot(data=pm_counts, x='Payment_Method', y='count', palette='viridis')
    plt.title('Payment Method Distribution for Expenses', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Payment Method', fontsize=12)
    plt.ylabel('Transaction Count', fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/payment_method_distribution.png", dpi=150)
    plt.close()
    
    # 6. Work Mode Impact
    plt.figure()
    work_mode_spend = df[df['Transaction_Type']=='Expense'].groupby('Work_Mode')['Amount'].mean().reset_index()
    sns.barplot(data=work_mode_spend, x='Work_Mode', y='Amount', palette='rocket')
    plt.title('Average Transaction Value by Employee Work Mode', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Work Mode', fontsize=12)
    plt.ylabel('Average Spend per Transaction (₹)', fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/work_mode_spend_impact.png", dpi=150)
    plt.close()
    
    # 7. Salary Band vs Savings Percentage
    plt.figure()
    # Deduplicate employee data to look at employee characteristics
    emp_dedup = df.drop_duplicates(subset=['Employee_ID'])
    sns.boxplot(data=emp_dedup, x='Salary_Band', y='Savings_Percentage', palette='Set2')
    plt.title('Savings Percentage Distribution by Salary Band', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Salary Band', fontsize=12)
    plt.ylabel('Savings Percentage (%)', fontsize=12)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/salary_band_vs_savings_percentage.png", dpi=150)
    plt.close()
    
    # 8. Top Leakage Categories
    plt.figure()
    leakage_by_cat = df[df['is_leakage']==1].groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=leakage_by_cat, x='Amount', y='Category', palette='Reds_r')
    plt.title('Top Expense Categories by Total Leakage Volume', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Total Leakage Spend (₹)', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    plt.tight_layout()
    plt.savefig(f"{images_dir}/top_leakage_categories.png", dpi=150)
    plt.close()
    
    # ------------------ Machine Learning ------------------
    print("Preparing data for Machine Learning model...")
    # Filter only Expense transactions
    ml_df = df[df['Transaction_Type'] == 'Expense'].copy()
    
    # Keep only features for prediction, drop targets/explanations/identifiers
    # CRITICAL: Dropping leakage_score and Expense_Type to prevent target leakage
    features_to_drop = [
        'Transaction_ID', 'Employee_ID', 'Date', 'Transaction_Type', 
        'Merchant', 'leakage_score', 'is_leakage', 'leakage_reason',
        'Year', 'Month', 'Day_of_Week', 'Monthly_Expense', 'Monthly_Savings', 
        'Savings_Percentage', 'Expense_Type'
    ]
    
    X = ml_df.drop(columns=features_to_drop, errors='ignore')
    y = ml_df['is_leakage']
    
    print("Features used for training:", X.columns.tolist())
    
    # Stratified Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    # Categorical and Numeric Columns setup
    categorical_cols = ['Salary_Band', 'Work_Mode', 'Category', 'Payment_Method', 'Weekend_Flag', 'Salary_Week', 'Subscription', 'Time_of_Day']
    numeric_cols = ['Monthly_Salary', 'Amount']
    
    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )
    
    # Models comparison
    results = {}
    
    # 1. Logistic Regression
    lr_pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])
    print("Training Logistic Regression...")
    lr_pipe.fit(X_train, y_train)
    lr_preds = lr_pipe.predict(X_test)
    lr_probs = lr_pipe.predict_proba(X_test)[:, 1]
    
    results['Logistic Regression'] = {
        'accuracy': accuracy_score(y_test, lr_preds),
        'precision': precision_score(y_test, lr_preds),
        'recall': recall_score(y_test, lr_preds),
        'f1': f1_score(y_test, lr_preds),
        'roc_auc': roc_auc_score(y_test, lr_probs),
        'cm': confusion_matrix(y_test, lr_preds),
        'model': lr_pipe
    }
    
    # 2. Random Forest
    rf_pipe = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', max_depth=12))
    ])
    print("Training Random Forest...")
    rf_pipe.fit(X_train, y_train)
    rf_preds = rf_pipe.predict(X_test)
    rf_probs = rf_pipe.predict_proba(X_test)[:, 1]
    
    results['Random Forest'] = {
        'accuracy': accuracy_score(y_test, rf_preds),
        'precision': precision_score(y_test, rf_preds),
        'recall': recall_score(y_test, rf_preds),
        'f1': f1_score(y_test, rf_preds),
        'roc_auc': roc_auc_score(y_test, rf_probs),
        'cm': confusion_matrix(y_test, rf_preds),
        'model': rf_pipe
    }
    
    # Save Random Forest Confusion Matrix Chart
    plt.figure(figsize=(6, 5))
    sns.heatmap(results['Random Forest']['cm'], annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Normal Spend', 'Leakage'], yticklabels=['Normal Spend', 'Leakage'])
    plt.title('Random Forest Confusion Matrix', fontsize=12, fontweight='bold')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig(f"{images_dir}/rf_confusion_matrix.png", dpi=150)
    plt.close()
    
    # Feature Importance (Random Forest)
    rf_model = rf_pipe.named_steps['classifier']
    feature_names = numeric_cols + list(rf_pipe.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_cols))
    
    importances = rf_model.feature_importances_
    feat_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False).head(15)
    
    plt.figure()
    sns.barplot(data=feat_df, x='Importance', y='Feature', palette='viridis')
    plt.title('Top 15 Feature Importances (Random Forest)', fontsize=12, fontweight='bold')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig(f"{images_dir}/rf_feature_importance.png", dpi=150)
    plt.close()
    
    # Print metrics summary
    print("\n--- MODEL METRICS COMPARISON ---")
    for name, r in results.items():
        print(f"Model: {name}")
        print(f"  Accuracy:  {r['accuracy']:.4f}")
        print(f"  Precision: {r['precision']:.4f}")
        print(f"  Recall:    {r['recall']:.4f}")
        print(f"  F1 Score:  {r['f1']:.4f}")
        print(f"  ROC-AUC:   {r['roc_auc']:.4f}\n")
        
    # Export predictions on the entire dataset
    print("Generating predictions on entire dataset...")
    # Add predictions column
    # For full dataset, predict class using Random Forest (as it's the more powerful tree classifier)
    full_X = df[df['Transaction_Type'] == 'Expense'].drop(columns=features_to_drop, errors='ignore')
    rf_full_preds = rf_pipe.predict(full_X)
    rf_full_probs = rf_pipe.predict_proba(full_X)[:, 1]
    
    # Merge predictions back to main df
    df.loc[df['Transaction_Type'] == 'Expense', 'predicted_leakage'] = rf_full_preds
    df.loc[df['Transaction_Type'] == 'Expense', 'predicted_leakage_prob'] = rf_full_probs
    
    df['predicted_leakage'] = df['predicted_leakage'].fillna(0).astype(int)
    df['predicted_leakage_prob'] = df['predicted_leakage_prob'].fillna(0)
    
    os.makedirs("C:/Users/AdminHK/.gemini/antigravity/scratch/SpendSense-AI/data/processed", exist_ok=True)
    processed_path = "C:/Users/AdminHK/.gemini/antigravity/scratch/SpendSense-AI/data/processed/cleaned_transaction_data.csv"
    df.to_csv(processed_path, index=False)
    print(f"Processed and labeled dataset exported to {processed_path}!")
    
    return results, feat_df

if __name__ == "__main__":
    run_analysis_and_export()
