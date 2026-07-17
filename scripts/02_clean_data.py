import pandas as pd
import numpy as np
import os

# EXPLANATION: Load the raw data from our raw data folder

input_path = os.path.join('data', 'raw', 'messy_construction_data.csv')
df = pd.read_csv(input_path)

print("--- Initial Data Inspection ---")
print(df.info())
print("\nUnique Sectors before cleaning:", df['Sector'].unique())

# STEP 1: DATA CLEANING

# EXPLANATION: Standardize sector categories to avoid duplicate groupings (e.g., "res" -> "RESIDENTIAL")
df['Sector'] = df['Sector'].str.upper().str.strip()
df['Sector'] = df['Sector'].replace({'RES': 'RESIDENTIAL'})

# EXPLANATION: Clean contractor names similarly
df['Lead_Contractor'] = df['Lead_Contractor'].replace({'Apex Construction Inc': 'Apex Build'})

# EXPLANATION: Filter out ongoing projects (where Actual_End or Final_Cost is missing)
df_completed = df.dropna(subset=['Actual_End', 'Final_Cost_USD']).copy()

# EXPLANATION: Format dates properly
df_completed['Planned_Start'] = pd.to_datetime(df_completed['Planned_Start'])
df_completed['Actual_End'] = pd.to_datetime(df_completed['Actual_End'])

# STEP 2: FEATURE ENGINEERING (BUILDING METRICS)

# EXPLANATION: Calculate the actual days a project took
df_completed['Actual_Duration_Days'] = (df_completed['Actual_End'] - df_completed['Planned_Start']).dt.days

# EXPLANATION: Calculate our business-critical variances
df_completed['Cost_Variance'] = df_completed['Target_Budget_USD'] - df_completed['Final_Cost_USD']
df_completed['Schedule_Variance'] = df_completed['Planned_Duration_Days'] - df_completed['Actual_Duration_Days']

# EXPLANATION: Calculate Efficiency Indices (CPI)
df_completed['CPI'] = df_completed['Target_Budget_USD'] / df_completed['Final_Cost_USD']

# EXPLANATION: Binary indicator (1 if over budget, 0 if on/under budget)
df_completed['Is_Over_Budget'] = np.where(df_completed['Cost_Variance'] < 0, 1, 0)


# STEP 3: EXPORT THE CLEANED BASE
output_path = os.path.join('data', 'processed', 'cleaned_construction_data.csv')
df_completed.to_csv(output_path, index=False)

print("\n✅ Stage 1 Complete: Cleaned data exported to:", output_path)
print(f"Remaining completed projects to analyze: {len(df_completed)}")
