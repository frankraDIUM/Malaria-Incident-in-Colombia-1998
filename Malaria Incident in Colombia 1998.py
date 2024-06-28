# Import the pandas and numpy packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Load the data
colmunic = pd.read_csv('data/colmunic.csv')
coldept  = pd.read_csv('data/coldept.csv')

# Display the first few rows of each DataFrame to understand their structure
print("Department Data (first 5 rows):")
print(coldept.head())

print("\nMunicipal Data (first 5 rows):")
print(colmunic.head())

# Checking for missing values in both datasets
missing_values_dept = coldept.isnull().sum()
missing_values_munic = colmunic.isnull().sum()

# Print the number of missing values for each column
print("\nMissing Values in Department Data:")
print(missing_values_dept)

print("\nMissing Values in Municipal Data:")
print(missing_values_munic)

# Checking for consistency in department codes
consistent_dept_codes = coldept['CODDEPT'].isin(colmunic['CODDEPT']).all()

# Display the result of consistency check
print("\nAre all department codes in `coldept.csv` present in `colmunic.csv`?")
print(consistent_dept_codes)

# Optional: Additional data cleaning (e.g., removing duplicates)
# Removing duplicates if any
df_dept_clean = coldept.drop_duplicates()
df_munic_clean = colmunic.drop_duplicates()

# Verify the shape of the dataframes after cleaning
print("\nShape of Department Data after removing duplicates:", df_dept_clean.shape)
print("Shape of Municipal Data after removing duplicates:", df_munic_clean.shape)

# Checking for any anomalies in population data (e.g., negative values)
# Ensure no negative values in population columns
population_columns_dept = coldept.columns[coldept.columns.str.startswith('TP') | coldept.columns.str.startswith('UP') | coldept.columns.str.startswith('RP')]
population_columns_munic = colmunic.columns[colmunic.columns.str.startswith('TP') | colmunic.columns.str.startswith('UP') | colmunic.columns.str.startswith('RP')]

negative_values_dept = coldept[population_columns_dept].lt(0).sum()
negative_values_munic = colmunic[population_columns_munic].lt(0).sum()

print("\nNegative Values in Population Columns (Department Data):")
print(negative_values_dept)

print("\nNegative Values in Population Columns (Municipal Data):")
print(negative_values_munic)

# Display first few rows of cleaned data
from IPython.display import display

print("\nCleaned Department Data:")
display(df_dept_clean.head())

print("\nCleaned Municipal Data:")
display(df_munic_clean.head())