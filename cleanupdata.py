# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 10:54:22 2024

Cleaning my data 
"""

import pandas as pd

# Path to the CSV file
file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021_GL (1).csv'

# Read the entire CSV file into a DataFrame
data = pd.read_csv(file_path, low_memory=False)

# Drop rows with any missing values
filtered_data = data.dropna(axis=0, how='any')

# Save the filtered data to a new CSV file
filtered_file_path = 'C:\\Users\\patri\\OneDrive\\Desktop\\Real_Estate_Sales_2001-2021Cleaned.csv'
filtered_data.to_csv(filtered_file_path, index=False)

print("Rows with missing values removed and saved to a new CSV file.")