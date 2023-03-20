import pandas as pd
import numpy as np
import re

# Load the CSV file into a Pandas dataframe
df = pd.read_csv('../data/sample-data/USW00023169-temperature-degreeF.csv')

# Clean the min column
df['min'] = pd.to_numeric(df['min'], errors='coerce')
df['min'] = df['min'].replace('', None)

# Clean the max column
df['max'] = pd.to_numeric(df['max'], errors='coerce')
df['max'] = df['max'].replace('', None)

# Clean the normal_min column
df['normal_min'] = pd.to_numeric(df['normal_min'], errors='coerce')
df['normal_min'] = df['normal_min'].replace('', None)

# Clean the normal_max column
df['normal_max'] = pd.to_numeric(df['normal_max'], errors='coerce')
df['normal_max'] = df['normal_max'].replace('', None)

# Drop rows with empty values
df.dropna(inplace=True)

# calculate the mean of 'min' and 'max' rows using mean() method
df['mean'] = df[['max', 'min']].mean(axis=1)

# create a new column 'status' with values 0 or 1 depending on whether the mean is within or outside the range
df['status_temp'] = df.apply(lambda row: 1 if row['mean'] >= row['normal_min'] and row['mean'] <= row['normal_max'] else 0, axis=1)

# count = df['status'].value_counts()
# print(count)

# Save the cleaned dataframe to a new CSV file
df.to_csv('../data/output-csv/dataclean-temperature-lasvegas.csv', index=False)

print('Data cleansing success')

df.info()
