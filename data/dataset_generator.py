import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

def generate_dataset(num_employees=500, year=2024):
    print(f"Generating synthetic dataset for {num_employees} employees...")
    
    # Define Salary Bands and associated parameters
    salary_bands = {
        'Band A (₹35k-50k)': (35000, 50000, 'Entry-level Analyst/Associate'),
        'Band B (₹50k-80k)': (50000, 80000, 'Senior Analyst/Specialist'),
        'Band C (₹80k-120k)': (80000, 120000, 'Team Lead/Consultant'),
        'Band D (₹120k-150k)': (120000, 150000, 'Manager/Senior Consultant')
    }
    
    # Work Modes
    work_modes = ['Office', 'Hybrid', 'WFH']
    work_modes_weights = [0.3, 0.5, 0.2]
    
    # Payment Methods
    payment_methods = ['UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'Cash']
    
    # Establish employees profiles
    employees = []
    for emp_id in range(1001, 1001 + num_employees):
        band = random.choices(list(salary_bands.keys()), weights=[0.4, 0.3, 0.2, 0.1])[0]
        min_sal, max_sal, role = salary_bands[band]
        salary = round(random.randint(min_sal, max_sal), -3) # Round to nearest thousand
        work_mode = random.choices(work_modes, weights=work_modes_weights)[0]
        
        employees.append({
            'Employee_ID': f"EMP{emp_id}",
            'Salary_Band': band,
            'Monthly_Salary': salary,
            'Work_Mode': work_mode,
            'Role': role
        })
        
    transactions = []
    
    # Merchants list for simulation
    merchants_by_cat = {
        'Rent': ['Landlord Corp', 'Property Management', 'Housing Society'],
        'Utilities': ['State Electricity Board', 'Municipal Water', 'Airtel Broadband', 'Jio Fiber', 'Indane Gas'],
        'Groceries': ['Reliance Fresh', 'BigBasket', 'Zepto', 'Blinkit', 'Local Kirana Store', 'DMart'],
        'Commute': ['Uber', 'Ola', 'Namma Metro', 'Shell Petrol', 'HP Petrol Pump', 'Auto Fare'],
        'Medical': ['Apollo Pharmacy', 'MedPlus', 'Practo Doctor Consult', 'Local Hospital', 'Diagnostics Lab'],
        'EMI': ['HDFC Bank Loan', 'ICICI Finance', 'SBI Credit Card EMI', 'Bajaj Finserv'],
        'Dining Out': ['Barbeque Nation', 'Socials Cafe', 'McDonalds', 'Dominos Pizza', 'Local Restaurant', 'Starbucks', 'Third Wave Coffee'],
        'Food Delivery': ['Swiggy', 'Zomato'],
        'Coffee & Snacks': ['Starbucks', 'Third Wave Coffee', 'Chai Point', 'Local Tea Stall', 'Tapri', 'Bakery'],
        'Shopping': ['Amazon', 'Flipkart', 'Myntra', 'Zara', 'H&M', 'Decathlon'],
        'OTT Subscription': ['Netflix', 'Amazon Prime', 'Spotify', 'Disney+ Hotstar', 'Youtube Premium'],
        'Gym': ['Cult.fit', 'Gold Gym', 'Local Gym Fitness'],
        'SIP Mutual Fund': ['Zerodha Coin', 'Groww SIP', 'UTI Mutual Fund']
    }
    
    # Process each month
    for month in range(1, 13):
        for emp in employees:
            salary_date = datetime(year, month, 1)
            
            # 1. Salary Credit
            transactions.append({
                'Employee_ID': emp['Employee_ID'],
                'Salary_Band': emp['Salary_Band'],
                'Monthly_Salary': emp['Monthly_Salary'],
                'Work_Mode': emp['Work_Mode'],
                'Date': salary_date.strftime('%Y-%m-%d'),
                'Transaction_Type': 'Income',
                'Category': 'Salary',
                'Amount': emp['Monthly_Salary'],
                'Merchant': 'Company Payroll',
                'Payment_Method': 'Net Banking',
                'Expense_Type': 'N/A',
                'Subscription': 'No',
                'Time_of_Day': 'Morning'
            })
            
            # 2. Rent Payment (Need) - between 1st and 5th
            rent_day = random.randint(1, 5)
            rent_date = datetime(year, month, rent_day)
            rent_amount = round(emp['Monthly_Salary'] * random.uniform(0.20, 0.30), -2)
            transactions.append({
                'Employee_ID': emp['Employee_ID'],
                'Salary_Band': emp['Salary_Band'],
                'Monthly_Salary': emp['Monthly_Salary'],
                'Work_Mode': emp['Work_Mode'],
                'Date': rent_date.strftime('%Y-%m-%d'),
                'Transaction_Type': 'Expense',
                'Category': 'Rent',
                'Amount': rent_amount,
                'Merchant': random.choice(merchants_by_cat['Rent']),
                'Payment_Method': 'Net Banking',
                'Expense_Type': 'Need',
                'Subscription': 'No',
                'Time_of_Day': 'Morning'
            })
            
            # 3. Utilities Payment (Need) - between 5th and 10th
            util_day = random.randint(5, 10)
            util_date = datetime(year, month, util_day)
            util_amount = round(random.uniform(1500, 4500))
            transactions.append({
                'Employee_ID': emp['Employee_ID'],
                'Salary_Band': emp['Salary_Band'],
                'Monthly_Salary': emp['Monthly_Salary'],
                'Work_Mode': emp['Work_Mode'],
                'Date': util_date.strftime('%Y-%m-%d'),
                'Transaction_Type': 'Expense',
                'Category': 'Utilities',
                'Amount': util_amount,
                'Merchant': random.choice(merchants_by_cat['Utilities']),
                'Payment_Method': random.choice(['Net Banking', 'UPI', 'Debit Card']),
                'Expense_Type': 'Need',
                'Subscription': 'No',
                'Time_of_Day': 'Afternoon'
            })
            
            # 4. EMI (Need)
            if random.random() < 0.60:
                emi_day = random.randint(3, 8)
                emi_date = datetime(year, month, emi_day)
                emi_amount = round(emp['Monthly_Salary'] * random.uniform(0.10, 0.25), -2)
                transactions.append({
                    'Employee_ID': emp['Employee_ID'],
                    'Salary_Band': emp['Salary_Band'],
                    'Monthly_Salary': emp['Monthly_Salary'],
                    'Work_Mode': emp['Work_Mode'],
                    'Date': emi_date.strftime('%Y-%m-%d'),
                    'Transaction_Type': 'Expense',
                    'Category': 'EMI',
                    'Amount': emi_amount,
                    'Merchant': random.choice(merchants_by_cat['EMI']),
                    'Payment_Method': 'Net Banking',
                    'Expense_Type': 'Need',
                    'Subscription': 'No',
                    'Time_of_Day': 'Morning'
                })
                
            # 5. SIP Investment (Savings)
            if random.random() < 0.70:
                sip_day = random.randint(1, 10)
                sip_date = datetime(year, month, sip_day)
                sip_amount = round(emp['Monthly_Salary'] * random.uniform(0.05, 0.15), -2)
                transactions.append({
                    'Employee_ID': emp['Employee_ID'],
                    'Salary_Band': emp['Salary_Band'],
                    'Monthly_Salary': emp['Monthly_Salary'],
                    'Work_Mode': emp['Work_Mode'],
                    'Date': sip_date.strftime('%Y-%m-%d'),
                    'Transaction_Type': 'Investment',
                    'Category': 'SIP Mutual Fund',
                    'Amount': sip_amount,
                    'Merchant': random.choice(merchants_by_cat['SIP Mutual Fund']),
                    'Payment_Method': 'Net Banking',
                    'Expense_Type': 'N/A',
                    'Subscription': 'Yes',
                    'Time_of_Day': 'Morning'
                })
                
            # 6. Subscriptions (Want)
            for sub_cat in ['OTT Subscription', 'Gym']:
                if random.random() < 0.80 if sub_cat == 'OTT Subscription' else 0.40:
                    sub_day = random.randint(1, 28)
                    sub_date = datetime(year, month, sub_day)
                    sub_amount = random.choice([299, 499, 649, 999]) if sub_cat == 'OTT Subscription' else random.choice([1500, 2000, 3000])
                    transactions.append({
                        'Employee_ID': emp['Employee_ID'],
                        'Salary_Band': emp['Salary_Band'],
                        'Monthly_Salary': emp['Monthly_Salary'],
                        'Work_Mode': emp['Work_Mode'],
                        'Date': sub_date.strftime('%Y-%m-%d'),
                        'Transaction_Type': 'Expense',
                        'Category': sub_cat,
                        'Amount': sub_amount,
                        'Merchant': random.choice(merchants_by_cat[sub_cat]),
                        'Payment_Method': random.choice(['Credit Card', 'UPI']),
                        'Expense_Type': 'Want',
                        'Subscription': 'Yes',
                        'Time_of_Day': 'Night'
                    })
                    
            # 7. Discretionary Spends
            num_discretionary = random.randint(15, 25)
            for _ in range(num_discretionary):
                txn_day = random.randint(1, 28)
                txn_date = datetime(year, month, txn_day)
                
                categories = ['Groceries', 'Commute', 'Medical', 'Dining Out', 'Food Delivery', 'Coffee & Snacks', 'Shopping']
                
                if emp['Work_Mode'] == 'Office':
                    weights = [0.15, 0.35, 0.05, 0.15, 0.10, 0.15, 0.05]
                elif emp['Work_Mode'] == 'WFH':
                    weights = [0.30, 0.05, 0.05, 0.10, 0.25, 0.10, 0.15]
                else: # Hybrid
                    weights = [0.20, 0.20, 0.05, 0.15, 0.15, 0.15, 0.10]
                    
                category = random.choices(categories, weights=weights)[0]
                
                if category == 'Groceries':
                    amount = round(random.uniform(300, 2500))
                    expense_type = 'Need'
                    time_of_day = random.choice(['Morning', 'Afternoon', 'Evening'])
                    pm_methods = ['UPI', 'Debit Card', 'Cash']
                elif category == 'Commute':
                    amount = round(random.uniform(50, 800))
                    expense_type = 'Need'
                    time_of_day = random.choice(['Morning', 'Evening'])
                    pm_methods = ['UPI', 'Debit Card', 'Cash']
                elif category == 'Medical':
                    amount = round(random.uniform(150, 3000))
                    expense_type = 'Need'
                    time_of_day = random.choice(['Morning', 'Afternoon', 'Evening'])
                    pm_methods = ['UPI', 'Credit Card', 'Debit Card']
                elif category == 'Dining Out':
                    amount = round(random.uniform(400, 3500))
                    expense_type = 'Want'
                    time_of_day = random.choice(['Afternoon', 'Evening', 'Night'])
                    pm_methods = ['UPI', 'Credit Card', 'Debit Card']
                elif category == 'Food Delivery':
                    amount = round(random.uniform(150, 1200))
                    expense_type = 'Want'
                    time_of_day = random.choice(['Afternoon', 'Evening', 'Night'])
                    pm_methods = ['UPI', 'Credit Card']
                elif category == 'Coffee & Snacks':
                    amount = round(random.uniform(40, 280))
                    expense_type = 'Want'
                    time_of_day = random.choice(['Morning', 'Afternoon', 'Evening'])
                    pm_methods = ['UPI', 'Cash']
                elif category == 'Shopping':
                    amount = round(random.uniform(500, 6000))
                    expense_type = 'Want'
                    time_of_day = random.choice(['Afternoon', 'Evening', 'Night'])
                    pm_methods = ['Credit Card', 'UPI', 'Net Banking']
                    
                merchant = random.choice(merchants_by_cat[category])
                payment_method = random.choice(pm_methods)
                
                salary_week_flag = 'Yes' if txn_day <= 7 else 'No'
                if salary_week_flag == 'Yes' and expense_type == 'Want':
                    amount = round(amount * random.uniform(1.2, 1.5))
                
                is_weekend = txn_date.weekday() >= 5
                weekend_flag = 'Yes' if is_weekend else 'No'
                
                if weekend_flag == 'Yes' and expense_type == 'Want':
                    amount = round(amount * random.uniform(1.1, 1.3))
                
                transactions.append({
                    'Employee_ID': emp['Employee_ID'],
                    'Salary_Band': emp['Salary_Band'],
                    'Monthly_Salary': emp['Monthly_Salary'],
                    'Work_Mode': emp['Work_Mode'],
                    'Date': txn_date.strftime('%Y-%m-%d'),
                    'Transaction_Type': 'Expense',
                    'Category': category,
                    'Amount': amount,
                    'Merchant': merchant,
                    'Payment_Method': payment_method,
                    'Expense_Type': expense_type,
                    'Subscription': 'No',
                    'Time_of_Day': time_of_day
                })

    df = pd.DataFrame(transactions)
    df = df.sort_values(by=['Employee_ID', 'Date']).reset_index(drop=True)
    df.insert(0, 'Transaction_ID', [f"TXN{i:06d}" for i in range(1, len(df) + 1)])
    
    os.makedirs("C:/Users/AdminHK/SpendSense-AI/data/raw", exist_ok=True)
    raw_path = "C:/Users/AdminHK/SpendSense-AI/data/raw/raw_transaction_data.csv"
    df.to_csv(raw_path, index=False)
    print(f"Raw transaction dataset successfully generated and saved to {raw_path}!")
    print(f"Total Transactions generated: {len(df)}")
    
if __name__ == "__main__":
    generate_dataset(500, 2024)
