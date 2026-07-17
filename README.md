 Capital Project Risk & Cost Overrun Dashboard
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/5872e6e8-b0b6-409d-b2ca-37b1b598174e" />


 Business Impact:
 
We created a business intelligence framework and a predictive risk-scoring model using Power BI. This tool analyzes past construction projects to identify what specifically causes budget overruns and delays. It helps construction companies move beyond guesswork, adjust safety buffers more realistically, and protect their profit margins.

 The Problem:
 
Construction management often lacks a clear view of past project performance because they rely on scattered spreadsheets. Without a central place to look at the data, it's hard to tell if cost overruns and delays come from certain project types, different scales, or specific contractors.

 The Solution:
 
Data Pipeline: A Python script using Pandas and NumPy was built to create structured data about construction projects. This includes target budgets, final costs, and planned versus actual timelines.
Data Analysis: The data was imported into Power BI for quality checks. Specific DAX formulas were written to calculate total cost variance, average schedule variance, and efficiency ratios.
Predictive AI Model: An internal AI model was used to identify and rank the factors that most increase the likelihood of a budget overrun.

How to Access Project Files:

Data Script: You can find the script for generating data in `notebooks/generate_data.py`.
Data File: The cleaned data is in `data/raw/cleaned_construction_data.csv`.
Dashboard: You can download the Power BI dashboard file here: [Power BI Dashboard File (.pbix)](https://github.com/ArseyMadeIt01/construction_delay_analysis/tree/main/dashboards)
    (To use the dashboard, click the link, download the file, and open it in Power BI Desktop.)

Core DAX Calculations:

The dashboard uses these calculations based on the data:
  Total Cost Variance: Sum of the Cost\_Variance column.
  Average Schedule Variance: Average of the Schedule\_Variance column.
  Project Overrun Rate: The number of projects that went over budget divided by the total number of projects.
  Average Cost Performance Index: Average of the CPI column.

Key Executive Insights:

Sector Spending: Big losses are concentrated in certain large sectors like COMMERCIAL and INFRASTRUCTURE. This means management needs to plan for higher contingency funds in bids for these types of projects.
Contractor Performance: We built a scorecard for lead contractors, comparing Apex Build, Vertex Infra, Summit Const, and Delta Partners. Sorting them by their average CPI and overrun rate gives procurement teams data to make better choices for future vendor selection.
Predicting Risk: The AI model identifies segments with a high chance of failure. This lets project managers flag risky bids before work even starts.

 Tech Stack:
 
  Data Modeling & Simulation: Python (Pandas, NumPy)
  
  Business Intelligence & Architecture: Power BI Desktop, DAX (Data Analysis Expressions)
