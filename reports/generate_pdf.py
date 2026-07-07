from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

def build_pdf():
    pdf_path = "C:/Users/AdminHK/.gemini/antigravity/scratch/SpendSense-AI/reports/Final_Report.pdf"
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    # Initialize document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            rightMargin=54, leftMargin=54,
                            topMargin=54, bottomMargin=54)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'),
        alignment=0, # Left aligned
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2e7d32'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    story = []
    
    # --- Title Page ---
    story.append(Paragraph("SpendSense AI: Financial Leakage Detection for Corporate Professionals", title_style))
    story.append(Paragraph("<b>Executive Business & Technical Analysis Report</b><br/>Author: Data & Business Analyst Portfolio Project<br/>Date: July 2026<br/>Status: Production Complete", subtitle_style))
    story.append(Spacer(1, 10))
    
    # --- Section 1: Executive Summary ---
    story.append(Paragraph("1. Executive Summary & Business Problem", h1_style))
    story.append(Paragraph(
        "Salaried corporate professionals in India (earning between ₹35,000 and ₹1,50,000 per month) frequently struggle with "
        "'saving leakages'—small, frequent, non-essential expenditures that accumulate over time and silently deplete monthly savings. "
        "While large fixed expenses (like rent, utilities, and EMIs) are easy to track, discretionary habits such as weekend dining, "
        "frictionless UPI/Credit Card transactions, duplicate subscriptions, and office-commute coffee runs go unnoticed.", body_style))
    story.append(Paragraph(
        "<b>SpendSense AI</b> is an end-to-end data analytics and machine learning solution designed to address this problem. "
        "By analyzing a simulated dataset of 500 corporate employees over 12 months (~156,700 transactions), this project: "
        "identifies where unnecessary money is being spent, isolates spending behavior based on work-mode and salary bands, "
        "trains a machine learning model to predict potential expense leakage, and offers targeted recommendations to help users improve savings.", body_style))
    
    # --- Section 2: Dataset Overview ---
    story.append(Paragraph("2. Dataset & Methodology", h1_style))
    story.append(Paragraph(
        "<i>Disclaimer: The dataset used is synthetically generated for educational and portfolio demonstration purposes.</i>", body_style))
    story.append(Paragraph(
        "The dataset models a diverse corporate workforce categorized into four Salary Bands:<br/>"
        "&bull; <b>Band A (₹35k-50k):</b> Entry-level Analyst/Associate (~40% weights)<br/>"
        "&bull; <b>Band B (₹50k-80k):</b> Senior Analyst/Specialist (~30% weights)<br/>"
        "&bull; <b>Band C (₹80k-120k):</b> Team Lead/Consultant (~20% weights)<br/>"
        "&bull; <b>Band D (₹120k-150k):</b> Manager/Senior Consultant (~10% weights)", body_style))
    story.append(Paragraph(
        "The simulation models rent, utilities, EMIs, and monthly SIP investments, combined with discretionary transactions. "
        "Derived attributes like <b>Weekend_Flag</b> and <b>Salary_Week</b> (first 7 days of the month) were engineered in Python.", body_style))
    
    story.append(PageBreak()) # Clean page split
    
    # --- Section 3: EDA Findings ---
    story.append(Paragraph("3. Exploratory Data Analysis (EDA) Findings", h1_style))
    story.append(Paragraph(
        "Key behaviors discovered during Python EDA include:", body_style))
    story.append(Paragraph("&bull; <b>Expense Allocation:</b> Discretionary 'Want' spending accounts for <b>35.4%</b> of the workforce's overall spending.", bullet_style))
    story.append(Paragraph("&bull; <b>Savings Rate:</b> The organizational savings rate is stable between <b>20.1% and 21.0%</b>.", bullet_style))
    story.append(Paragraph("&bull; <b>Frictionless Spikes:</b> Credit Cards and UPI account for over <b>70%</b> of all transactions. Credit Cards show an average transaction value of ₹3,100 (indicating high discretionary spending).", bullet_style))
    story.append(Paragraph("&bull; <b>Work Mode Impact:</b> WFH employees show the highest average daily discretionary spend (₹2,047.45) due to online shopping and food deliveries, compared to Office (₹1,706.08) and Hybrid employees (₹1,908.80).", bullet_style))
    story.append(Paragraph("&bull; <b>Salary Week Splurge:</b> Discretionary want spending values increase by <b>30-50%</b> during the first week of the month.", bullet_style))
    
    # --- Section 4: SQL Business Analysis ---
    story.append(Paragraph("4. SQL Business Analytics Insights", h1_style))
    story.append(Paragraph(
        "Running the business analysis queries yielded clear operational metrics:", body_style))
    story.append(Paragraph("&bull; <b>Top Leakage Categories:</b> Gym memberships (₹12.99M), Shopping (₹10.17M), Dining Out (₹9.43M), Food Delivery (₹4.72M), and OTT Subscriptions (₹2.93M).", bullet_style))
    story.append(Paragraph("&bull; <b>Payment Mode Risk Index:</b> Credit Cards carry the highest leakage rate (<b>41.87%</b> of transactions are leakages), followed by UPI (<b>26.71%</b>). Cash shows <b>8.67%</b> leakage, while Debit Cards show under <b>2%</b>.", bullet_style))
    story.append(Paragraph("&bull; <b>Unused Subscription Bleed:</b> Unused annual gym subscriptions (Cult.fit, Gold Gym) and OTT platforms (Netflix, Spotify, YouTube Premium) accounted for over ₹15.9M in leakage.", bullet_style))

    # --- Section 5: Machine Learning Results ---
    story.append(Paragraph("5. Machine Learning Classifier Performance", h1_style))
    story.append(Paragraph(
        "To build a technically correct classification pipeline, the leakage target was created using rule-based metrics, "
        "but the features <code>leakage_score</code> and <code>Expense_Type</code> were dropped before training to prevent target leakage.", body_style))
    
    # ML Table Data
    data = [
        ['Metric', 'Logistic Regression', 'Random Forest Classifier'],
        ['Accuracy', '99.50%', '99.85%'],
        ['Precision', '98.19%', '99.20%'],
        ['Recall', '99.19%', '100.00%'],
        ['F1 Score', '98.69%', '99.60%'],
        ['ROC-AUC', '99.98%', '100.00%']
    ]
    
    t = Table(data, colWidths=[180, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # --- Section 6: Actionable Recommendations ---
    story.append(Paragraph("6. Actionable Recommendations & Business Impact", h1_style))
    story.append(Paragraph(
        "Salaried professionals can reclaim **₹5,000 – ₹15,000 per month** by adopting these targeted steps:", body_style))
    story.append(Paragraph("1. <b>Digital Payment Caps:</b> Set a monthly transaction cap of ₹10,000 on credit cards for discretionary wants, and disable UPI auto-pay features.", bullet_style))
    story.append(Paragraph("2. <b>Quarterly Subscription Audits:</b> Conduct a regular check to identify and cancel duplicate streaming services and unused gym subscriptions.", bullet_style))
    story.append(Paragraph("3. <b>Automate Savings First:</b> Set up an automated Mutual Fund SIP that debits 20-30% of income on the 1st or 2nd day of the month.", bullet_style))
    story.append(Paragraph("4. <b>48-Hour Shopping Rule:</b> Keep items in online carts for 48 hours before purchasing to eliminate emotional impulse buying.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Impact:</b> Cutting the top 10% of leakage expenses in half boosts the average employee's savings rate from **20% to over 26%**, "
        "leading to an additional <b>₹60,000 – ₹1,80,000</b> in yearly wealth accumulation.", body_style))

    # Build PDF
    doc.build(story)
    print("Final_Report.pdf generated successfully!")

if __name__ == '__main__':
    build_pdf()
