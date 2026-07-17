import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 1. Set seed for reproducibility
np.random.seed(42)
n_projects = 1000

# 2. Generate Raw Synthetic Construction Data
start_dates = [datetime(2022, 1, 1) + timedelta(days=int(np.random.randint(0, 1000))) for _ in range(n_projects)]
planned_durations = np.random.randint(90, 540, n_projects) # 3 to 18 months

# Introduce realistic construction delays (skewed right)
delay_factors = np.random.exponential(scale=45, size=n_projects) + np.random.normal(loc=10, scale=5, size=n_projects)
actual_durations = planned_durations + np.where(delay_factors > 0, delay_factors.astype(int), 0)

planned_budgets = planned_durations * np.random.randint(5000, 15000, n_projects)
# Overruns usually correlate with delays
overrun_factors = (actual_durations / planned_durations) * np.random.uniform(0.9, 1.4, n_projects)
actual_costs = planned_budgets * overrun_factors

# Inconsistent text data (simulation of human data entry errors)
project_types = np.random.choice(['Commercial', 'Residential', 'Infrastructure', 'res', 'COMMERCIAL'], n_projects)
contractors = np.random.choice(['Apex Build', 'Vertex Infra', 'Summit Const', 'Delta Partners', 'Apex Construction Inc'], n_projects)

raw_data = pd.DataFrame({
    'Project_ID': [f'PROJ-{i+1000}' for i in range(n_projects)],
    'Project_Name': [f'Site Phase {np.random.randint(1, 10)} Development' for _ in range(n_projects)],
    'Sector': project_types,
    'Lead_Contractor': contractors,
    'Target_Budget_USD': planned_budgets,
    'Final_Cost_USD': actual_costs,
    'Planned_Start': start_dates,
    'Planned_Duration_Days': planned_durations
})

# Add actual end dates, but leave 5% missing to simulate active/incomplete projects
raw_data['Actual_End'] = [raw_data['Planned_Start'][i] + timedelta(days=int(actual_durations[i])) for i in range(n_projects)]
missing_mask = np.random.rand(n_projects) < 0.05
raw_data.loc[missing_mask, 'Actual_End'] = np.nan
raw_data.loc[missing_mask, 'Final_Cost_USD'] = np.nan

# EXPLANATION: Save the messy raw data to the data/raw/ folder we created
output_path = os.path.join('data', 'raw', 'messy_construction_data.csv')
raw_data.to_csv(output_path, index=False)
print(f"✅ Messy raw dataset successfully created at: {output_path}")