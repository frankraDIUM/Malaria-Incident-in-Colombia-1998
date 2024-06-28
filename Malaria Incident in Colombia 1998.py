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

# merge data files
merged_data = colmunic.merge(coldept, on= ['ADM0', 'ADM1', 'MALARI98'], how='left')

# Read the two shapefiles
colmunic_shapefile = gpd.read_file('data/colmunic.shp')
coldept_shapefile = gpd.read_file('data/coldept.shp')

# Merge the shapefiles
merged_shapefile = gpd.GeoDataFrame(pd.concat([colmunic_shapefile, coldept_shapefile], ignore_index=True))

# Save the merged shapefile
merged_shapefile.to_file("data/merged_shapefile.shp")

# Get the number of null values present in the data
merged_shapefile.isnull().sum()

# drop duplicates
merged_shapefile.drop_duplicates(inplace=True)

# Preview the dataframe
merged_shapefile.head(10)

# Create a Folium map centered around Colombia
colombia_map = folium.Map(location=[4.5709, -74.2973], zoom_start=6)

# Add malaria incidence data to the map
for _, row in merged_shapefile.iterrows():
    if row.geometry.geom_type == 'Point':
        location = [row.geometry.y, row.geometry.x]
    else:
        location = [row.geometry.centroid.y, row.geometry.centroid.x]
    
    folium.CircleMarker(
        location=location,  # Use geometry to get coordinates
        radius=5,
        popup=f"Municipality: {row['ADM2']}<br>Malaria Incidence: {row['MALARI98']}",
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(colombia_map)

# Save the map as an HTML file
colombia_map.save('data/malaria_incidence_map.html')

# Display the map
colombia_map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged_shapefile.plot(column='MALARI98', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Add titles and labels
ax.set_title('Malaria Incidence in Colombia (1998)', fontdict={'fontsize': '15', 'fontweight': '3'})
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Save the plot
plt.savefig('data/malaria_incidence_plot.png')

# Display the plot
plt.show()

# Select columns
dist_columns = ['ADM2', 'MALARI98', 'TP1998', 'UP1998', 'RP1998']
df_selected = merged_shapefile[dist_columns]

# Drop rows with missing values
df_selected = df_selected.dropna()

# Display the first few rows of the cleaned DataFrame
df_selected.head()

# Create a bar chart for malaria incidence
plt.figure(figsize=(12, 6))
sns.barplot(x='ADM2', y='MALARI98', data=df_selected.sort_values('MALARI98', ascending=False).head(10))
plt.title('Top 10 Counties with Highest Malaria Incidence in 1998')
plt.xlabel('County')
plt.ylabel('Malaria Incidence')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Create a bar chart for total population
plt.figure(figsize=(12, 6))
sns.barplot(x='ADM2', y='TP1998', data=df_selected.sort_values('TP1998', ascending=False).head(10))
plt.title('Top 10 Counties with Highest Total Population in 1998')
plt.xlabel('County')
plt.ylabel('Total Population')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Create a bar chart for urban population
plt.figure(figsize=(12, 6))
sns.barplot(x='ADM2', y='UP1998', data=df_selected.sort_values('UP1998', ascending=False).head(10))
plt.title('Top 10 Counties with Highest Urban Population in 1998')
plt.xlabel('County')
plt.ylabel('Urban Population')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Create a bar chart for rural population
plt.figure(figsize=(12, 6))
sns.barplot(x='ADM2', y='RP1998', data=df_selected.sort_values('RP1998', ascending=False).head(10))
plt.title('Top 10 Counties with Highest Rural Population in 1998')
plt.xlabel('County')
plt.ylabel('Rural Population')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Aggregate data by states (departments)
state_aggregated = merged_data.groupby('ADM1')['MALARI98'].sum().reset_index()

# Aggregate data by counties (municipalities)
county_aggregated = merged_data.groupby('ADM2')['MALARI98'].sum().reset_index()

# Sort states by malaria incidence
state_aggregated_sorted = state_aggregated.sort_values(by='MALARI98', ascending=False)

# Sort counties by malaria incidence
county_aggregated_sorted = county_aggregated.sort_values(by='MALARI98', ascending=False)

# Find the state with the highest and lowest malaria incidence
highest_incidence_state = state_aggregated_sorted.iloc[0]['ADM1']
lowest_incidence_state = state_aggregated_sorted.iloc[-1]['ADM1']

# Find the county with the highest and lowest malaria incidence
highest_incidence_county = county_aggregated_sorted.iloc[0]['ADM2']
lowest_incidence_county = county_aggregated_sorted.iloc[-1]['ADM2']

# Display results
print(str(highest_incidence_state) + " is the state with the highest malaria incident.")
print(str(lowest_incidence_state) + " is the state with the lowest malaria incident.")
print(str(highest_incidence_county) + " is the county with the highest malaria incident.")
print(str(lowest_incidence_county) + " is the county with the lowest malaria incident.")