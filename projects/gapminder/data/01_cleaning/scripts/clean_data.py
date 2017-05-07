import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path as op

path = op.dirname(op.abspath(__file__))
path_data = path + "/../../01_cleaning/gapminderDataFiveYear_manualcleaned.txt"
print('Loading dataset: {}'.format(path_data))
gapminder = pd.read_table(path_data, sep = "\t")
gapminder_copy = gapminder.copy()

# Drop missing values
gapminder_copy = gapminder_copy.dropna()

# Convert types to int
gapminder_copy['year'] = gapminder_copy['year'].astype(int)
gapminder_copy['pop'] = gapminder_copy['pop'].astype(int)

# Drop duplicates
gapminder_copy = gapminder_copy.drop_duplicates()

# Now we'll reset the index of the dataframe since it's off by 1
gapminder_copy = gapminder_copy.reset_index(drop=True)

# Clean up the strings
gapminder_copy['region'] = gapminder_copy['region'].str.lstrip().str.rstrip().str.lower()

# Make our columns lowercase
gapminder_copy.columns = gapminder_copy.columns.str.lower()

# Rename columns so that spaces become underscores
gapminder_copy.columns = gapminder_copy.columns.str.replace(' ', '_')

# Fix string naming
gapminder_copy['region'].replace(".*congo, dem.*", "africa_dem rep congo", regex=True, inplace=True)
gapminder_copy['region'].replace(".*_democratic republic of the congo", "africa_dem rep congo", regex=True, inplace=True)

gapminder_copy['region'].replace(".*ivore.*", "africa_cote d'ivoire", regex=True, inplace=True)
gapminder_copy['region'].replace("^_canada", "americas_canada", regex=True, inplace=True)

# Tidy the data
split_regions = gapminder_copy['region'].str.split('_', 1)

# Create two new variables from the previous column
gapminder_copy['country'] = split_regions.str[1]
gapminder_copy['continent'] = split_regions.str[0]

# Now we'll drop the old region column, and look at the data
gapminder_copy = gapminder_copy.drop('region', 1) #1 stands for column

# Save the data
path_save = path + '/../../02_cleaned/gapminder_clean.csv'
print('Saving to: {}'.format(path_save))
gapminder_copy.to_csv(path_save, index=False)
print('Done!\n---\n\n')
