# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:12:35 2024

@author: bg2226
"""
# %% Importing Libraries
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
##ctrl shft e to script and i to console
########################################################################################################################
# %% Reading Data 

# Load the stream gauge CSV file into a DataFrame
d_test = pd.read_csv('S:\\FOR\\Fule-Lab\\Other\\bgonzalez\\thesis\\LANL_streamGageData\\Daria_C\\E050 2001-2010.csv', header=None)

print(d_test.head(10)) # Display the first 10 rows

# Method chaining using pipe()
temp = (d_test
 .dropna(axis=1, how='all')  # Remove columns with all NaN values
 #.head(10)                   # Select the first 10 rows
 #.pipe(print)                # Print the result in the console, unnecessary 
)

# Load MET data 
folder_path = 'S:/FOR/Fule-Lab/Other/bgonzalez/forest-hydro/BANDELIER_weatherstation'

# Get all CSV files in the folder
csv_files = [files for files in os.listdir(folder_path) if files.endswith('.csv')]

# Merge CSV files
df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
met_df = pd.concat(df_list)

# Load SNOTEL data 
file_path = "S:/FOR/Fule-Lab/Other/bgonzalez/thesis/snotel_quemazon_708_dataonly.csv" # File path

# Load the CSV file into a DataFrame
snotel = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
print(snotel.head())
########################################################################################################################

# %% Cleaning Stream Data 

# Create new column names by concatenating the first three rows for each column [ take 3 top rows for each col]
# [expression for item in iterable]
new_col_names = [ # brackets generate a list to store the column names 
    '_'.join(temp[col].head(3).fillna('').astype(str))  # Concatenate first 3 rows of each column
    for col in temp.columns  # Iterate over each column
]

temp.columns = new_col_names # Assign new column names to the DataFrame

# Drop the first three rows and reset the DataFrame
temp = temp.drop([0, 1, 2]).reset_index(drop=True) # Drop the first three rows

#keep only first four 
temp2 = temp.iloc[:,:4].copy() # beg of rows : end of rows all, beg of cols to : end of rows (4 here)


temp2 = temp2.rename(columns={
    temp2.columns[1]: 'E050_232_stage_ft',
    temp2.columns[2]: 'QualCode',
    temp2.columns[3]: 'E050_262_discharge_CFS'  # Add more renaming as needed
}).astype({
    'Time_and_Date':'datetime64[ns]',
    'E050_232_stage_ft': 'float64',
    'QualCode': 'str',
    'E050_262_discharge_CFS': 'float64'  # Add more type conversions as needed
})
  
# Clean up any duplicate Categories by first converting to str above and now category for memory efficiency 
temp2['QualCode'] = temp2['QualCode'].astype('category')

# replace ice values and other NAN values (as noted in category) with NA values
temp2.loc[temp2['QualCode'].isin(['151', '152', '255']), 'Discharge'] = np.nan #.loc[BOOLEAN condition] will change the TRUE values in the boolean to the specified value, here NA. to inverse use ~ 
# print(temp2['E050_262_discharge_CFS'].isna().sum()) # to make sure this worked we should see an increase in NAN values 

# set datetime column as index in dataframe 
temp2.set_index('Time_and_Date', inplace=True)

## let's create a column with daily average and weekly rolling discharge average 
temp2['E050_262_discharge_CFS'] = temp2['E050_262_discharge_CFS'].rolling(window=)
temp2['Weekly_Avg_Discharge'] = temp2['E050_262_discharge_CFS'].rolling(window='7D').mean()
    
## print(temp2.loc['2007-04-01':'2007-04-01', ['E050_262_discharge_CFS', 'Weekly_Avg_Discharge']])## print(temp2.loc['2007-04-01':'2007-04-01', ['E050_262_discharge_CFS']].agg(['max', 'min']))
# Save new file after cleaning

#print(cd_test.info()) # Display information about the DataFrame
#print(cd_test.describe()) # Display summary statistics
    
# Convert Cols to Proper Type
#temp2["Time_and_Date"]= pd.to_datetime(temp2["Time_and_Date"], errors='coerce') #method1: use col name
########################################################################################################################
# %% Cleaning Met Data 


########################################################################################################################

# %% Cleaning Snotel Data 


########################################################################################################################
# Merge all predictor data by daily and weekly averages 

# %% Babys' 1st LSTM model 

### Predictors (4) 
# Snotel 
# met data frijoles - precip, penman, temp 

temp2.sort_values('Time_and_Date', inplace=True)

# Create a mask for missing values
missing_mask = temp2.isna()

# Feature Scaling (only on non-missing data)
# Scaling changes your data from values to 0 to 1 
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = temp2.copy()

# 


# okay let's fix columns 


# %% Visualizing Pre-cleaned data 



