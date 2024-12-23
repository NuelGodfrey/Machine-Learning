# -*- coding: utf-8 -*-
"""Energy Data Metrics-Nuel Godfrey

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_JRQctds2GSAuFb_t4jnepQxF2p7U9fD
"""

# importation of neccessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# loading of the data
hist_data = pd.read_csv('historical_energy_data.csv')
market_data = pd.read_csv('market_data.csv')
infrastructure_data = pd.read_csv('infrastructure_data.csv')
regulatory_data = pd.read_csv('regulatory_data.csv')

hist_data.head()

infrastructure_data.head()

regulatory_data.head()

market_data.head()

"""Understanding the Structure of the Datasets

"""

hist_data.info()
hist_data.describe()

infrastructure_data.info()
infrastructure_data.describe()

market_data.info()
market_data.describe()

regulatory_data.info()
regulatory_data.describe()

"""Data Cleaning

"""

hist_data.head()

infrastructure_data.head()

market_data.head()

regulatory_data.head()

"""Converting the dormat of the data"""

date_format = "%d/%m/%Y"
hist_data['Date/Time'] = pd.to_datetime(hist_data['Date/Time'], format=date_format)

new_date_format = "%Y-%m-%d"
hist_data['Date/Time'] = pd.to_datetime(hist_data['Date/Time'], format = new_date_format)

hist_data.head(1)

date_format = "%d/%m/%Y"
infrastructure_data['Date/Time'] = pd.to_datetime(infrastructure_data['Date/Time'], format=date_format)

new_date_format = "%Y-%m-%d"
infrastructure_data['Date/Time'] = pd.to_datetime(infrastructure_data['Date/Time'], format = new_date_format)

infrastructure_data.head(1)

new_date_format = "%Y-%m-%d"
market_data['Date/Time'] = pd.to_datetime(market_data['Date/Time'], format = new_date_format)

market_data.info(1)

new_date_format = "%Y-%m-%d"
regulatory_data['Date/Time'] = pd.to_datetime(regulatory_data['Date/Time'], format = new_date_format)

regulatory_data.info()

"""EXPLORATORY DATA ANALYSIS"""

# specifically, to examine:
# location/region and energy source from historical_energy_data
# infrastructure status, maintenance Activities, and technology limitations from infrastructure_data
# competitor data and market trends from market_data
# Regulatory changes and compliance status from regulatory_data

# grouping all datasets as dataset
datasets = {'hist_data': hist_data, 'infrastructure_data': infrastructure_data, 'market_data': market_data, 'regulatory_data': regulatory_data}

# extracting unique values and thier counts for categorical columns
categorical_columns = {'hist_data': ['Location/Region', 'Energy Source'],"infrastructure_data":['Infrastructure Status','Maintenance Activities', 'Technology Limitations'],'market_data':['Competitor Data', 'Market Trends'], 'regulatory_data': ['Regulatory Changes', 'Compliance Status']}

categorical_values_counts = {}
for dataset, columns in categorical_columns.items():
  for column in columns:
    categorical_values_counts[(dataset, column)] = datasets[dataset][column].value_counts()

# visualizing
# calculate the number of rows and columns for the sublots
num_rows = (len(categorical_values_counts) + 1) // 2
num_cols = 2

#create a grid of the subplots and ensuring that the figure is tall enough to accomodate all subplots without them overlapping each other or being too cramped.
fig, axes = plt.subplots(num_rows, num_cols, figsize= (12, 6 * num_rows))

#flatten the axes array for easier indexing
axes = axes .flatten()


# iterate through categorical columns and plot them in subplots
for i,  ((dataset, column), counts) in enumerate(categorical_values_counts.items()):
  ax = axes[i]
  sns.barplot(x=counts.values, y= counts.index, ax = ax)
  ax.set_title(f'Value Counts for {dataset} -{column}')
  ax.set_xlabel('Count')
  ax.set_ylabel(column)

# hide any remaining empty subplots
for i in range(len(categorical_values_counts), num_rows * num_cols):
  fig.delaxes(axes[i])


# adjust the layout
plt.tight_layout
plt.show()

"""EDA-Energy Demand, Production and consumption over time"""

#Extract the month and year from the date time column.
hist_data['Year'] = hist_data['Date/Time'].dt.year
hist_data['Month'] = hist_data['Date/Time'].dt.month

#Create a new column year month for easy plotting.
hist_data['Year-Month'] = hist_data['Date/Time'].dt.to_period('M')

# Aggregating Data on a monthly basis
monthly_data = hist_data.groupby('Year-Month')[['Energy Production (kWh)', 'Energy Consumption (kWh)', 'Energy Demand']].mean()


# setting figsize
plt.figure(figsize=(15, 6))

# plotting
sns.lineplot(data = monthly_data, x = monthly_data.index.astype(str), y='Energy Production (kWh)', label='Energy Production', color='blue', linestyle= '-', linewidth=1.5, ci = None)
sns.lineplot(data = monthly_data, x = monthly_data.index.astype(str), y='Energy Consumption (kWh)', label='Energy Consumption', color='red', linestyle= '-', linewidth=1.5, ci = None)
sns.lineplot(data = monthly_data, x = monthly_data.index.astype(str), y='Energy Demand', label='Energy Demand', color='green', linestyle= '-', linewidth=1.5, ci = None)


# setting the tile and labels
plt.title('Monthly Aggregate of Energy Production, Consumption, and Demand Over time')
plt.xlabel('Date')
plt.ylabel('KWh')
plt.legend(loc = 'upper left', bbox_to_anchor=(1, 1))
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# setting our labels
labels = monthly_data.index.astype(str).tolist()
n = 6
plt.xticks(labels[::n], rotation = 360)

plt.tight_layout()
plt.subplots_adjust(hspace=0.5)
plt.show()

"""EDA- Energy Price and Market Price
Market Price and Energy Price overtime

*To understand the pricing dynam,ics and its relation to market trends.

*Visualization of the Market Price from the market_data datset alongside the energy price from the historical_energy_data dataset over time.
"""

# merging historical_energy_data on Date/Time for combined analysis
merged_data = pd.merge(hist_data, market_data, on = 'Date/Time', how= 'inner')

# setting 'Date/Time' as the index of the Dataframe for aggregation
merged_data['Year'] = merged_data['Date/Time'].dt.year
merged_data['Month'] = merged_data['Date/Time'].dt.month

#Aggregating data on a monthly basis
monthly_merged_data = merged_data.groupby(['Year','Month'])[['Energy Production (kWh)', 'Energy Consumption (kWh)', 'Energy Demand', 'Market Price', 'Energy Price']].mean()

# create a new 'Year-Month' column for plotting
monthly_merged_data['Year-Month'] = monthly_merged_data.index.get_level_values(0).astype(str)+ '-'+ monthly_merged_data.index.get_level_values(1).astype(str)

plt.figure(figsize=(15, 8))

sns.lineplot(data=monthly_merged_data, x = 'Year-Month', y = 'Market Price', label = 'Market Price', color ='blue', linestyle= '-', linewidth=1.5, ci = None)
sns.lineplot(data=monthly_merged_data, x = 'Year-Month', y = 'Energy Price', label = 'Energy Price', color ='yellow', linestyle= '-', linewidth=1.5, ci = None)

plt.title('Monthly Aggregate of Market Price and Energy Price over Time')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.legend(loc='upper left', bbox_to_anchor = (1, 1))

plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# setting our labels
labels = monthly_merged_data['Year-Month'].tolist()
n = 6
plt.xticks(labels[::n], rotation = 360)

plt.tight_layout()
# plt.subplots_adjust(hspace=0.5)
plt.show()

"""Energy Demand and Energy Price Correlation.
*Let's check if the energy demand is influenced by the current energy price.
"""

# merge historical_energy_data and market_data on Date/Time
merged_data = pd.merge(hist_data, market_data, on='Date/Time', how = 'inner')

correlation_energy_price = merged_data['Energy Demand'].corr(merged_data['Energy Price'])
correlation_market_price = merged_data['Market Demand'].corr(merged_data['Market Price'])

correlation_energy_price

correlation_market_price

"""Infrastructure and Technological limitations

*To understand the state of infrastructure and technology overtime

*We'll visualize the frequency of various infrsatructure status values and the distribution of Technology limitations from the infrastructure_data dataset

"""

# settin g up the figure and axis
fig, axes = plt.subplots(1, 2, figsize=(15, 8))

#plotting the frequency of infrstructure status
sns.countplot(data=infrastructure_data, x='Infrastructure Status', ax=axes[0],order=['Good', 'Fair', 'Poor'],palette='viridis')
axes[0].set_title('Frequency of Infrastructure Status')
axes[0].set_xlabel('Infrastructure Status')
axes[0].set_ylabel('count')

# plotting the frequency of technology limitation
sns.countplot(data=infrastructure_data, x='Technology Limitations', order=['High', 'Moderate', 'Low', 'None'], ax=axes[1],palette='viridis')
axes[1].set_title('Frequency of Technology Limitations')
axes[1].set_xlabel('Technology Limitations')
axes[1].set_ylabel('count')

plt.tight_layout()
plt.show()

"""Let's see the relationship with infrastructure status and technology limitation.

"""

# cross tabulation of two categorical columns

ct = pd.crosstab(infrastructure_data['Infrastructure Status'], infrastructure_data['Technology Limitations'])
plt.figure(figsize=(10, 6))

sns.heatmap(ct, annot = True, cmap = 'viridis')
plt.title('Infrastructure Status vs Technology Limitations')
plt.xlabel('Technology Limitations')
plt.ylabel('Infrastructure Status')

plt.tight_layout()

plt.show()

"""Correlation Between poor infrastructure status and high technology limitation and the energy production.

"""

# convert the infrastructure status and technological limitations to binary columns

infrastructure_data['Poor_Infrastructure'] = infrastructure_data['Infrastructure Status'].apply(lambda x: 1 if x == 'Poor' else 0)
infrastructure_data['High_Tech_Limitations'] = infrastructure_data['Technology Limitations'].apply(lambda x:1 if x == 'High' else 0)

infrastructure_data['Combined']= infrastructure_data['Poor_Infrastructure'] + infrastructure_data['High_Tech_Limitations']

merged_infra_data = pd.merge(hist_data, infrastructure_data, on='Date/Time', how = 'inner')

correlation_coefficient = merged_infra_data['Energy Production (kWh)'].corr(merged_infra_data['Combined'])

correlation_coefficient

"""Regulatory Changes and Compliance Costs.

-To understand the impact of regulatory changes.

-We'll visualize the frequency of various Regulatory Changes and the distribution of Compliance Costs associated with these changes from the regulatory_data dataset.
"""

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

sns.countplot(data=regulatory_data, x ='Regulatory Changes', ax=ax1, palette='viridis')
ax1.set_title('Frequency of Regulatory Changes')
ax1.set_xlabel('Regulatory Changes')
ax1.set_ylabel('count')

sns.histplot(data=regulatory_data,x='Compliance Costs',ax=ax2,bins=30, kde=True,color='skyblue')
ax2.set_title('Distribution of Compliance Costs')
ax2.set_xlabel('Compliance Costs')
ax2.set_ylabel('Freq')

plt.tight_layout()
plt.show()

hist_data.head()

"""Impact of Regulatory Changes and Operational Costs on Revenue


-We'll visualize the relationship between regulatory changes and the associated compliance costs, as well as the operational costs to the revenue generated from the company.

-Revenue = Energy Consumption* Energy Price

-This will provide insights into the financial implications of regulatory changes cost and operational cost for energix enterprise.




"""

# Calculating the revenue

hist_data['Revenue'] = hist_data['Energy Consumption (kWh)'] * hist_data['Energy Price']

merged_reg_data = pd.merge(hist_data, regulatory_data, on= 'Date/Time', how = 'inner')

# extract year and month from Date Time column
merged_reg_data['Year'] = merged_reg_data['Date/Time'].dt.year
merged_reg_data['Month'] = merged_reg_data['Date/Time'].dt.month

# Aggregating data on a monthly basis
numeric_columns = merged_reg_data.select_dtypes(include=np.number).columns
# Removing 'Month' and 'Year' if they are present in numeric_columns
numeric_columns = numeric_columns.drop(['Month', 'Year'])
monthly_aggregated_data = merged_reg_data.groupby(['Year', 'Month'])[numeric_columns].mean().reset_index()

monthly_aggregated_data['Year-Month']= monthly_aggregated_data['Year'].astype(str)+'-'+ monthly_aggregated_data['Month'].astype(str)

plt.figure(figsize=(15, 6))

plt.fill_between(monthly_aggregated_data['Year-Month'], monthly_aggregated_data['Operational Costs'], color = 'blue', label= 'Operational Costs', alpha=0.5)
plt.fill_between(monthly_aggregated_data['Year-Month'], monthly_aggregated_data['Operational Costs'], monthly_aggregated_data['Operational Costs'] + monthly_aggregated_data['Compliance Costs'] )

sns.lineplot(data = monthly_aggregated_data, x = 'Year-Month', y = 'Revenue', label = 'Revenue', color = 'red', linestyle= '-', linewidth=2, ci = None)
plt.xlabel('Date')
plt.ylabel('Amount ($)')
plt.legend(loc = 'upper left')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# setting our labels
labels = monthly_aggregated_data['Year-Month'].tolist()
n = 6
plt.xticks(labels[::n], rotation = 360)

plt.tight_layout()
plt.show()

"""Analyzing Competition from Renewable Energy Providers.

-To understand the competition from renewable energy providers and its impact on Energix Enterprise. We'll analyze the Energy Source Column from the historical_energy_data data set.

-We'll visualize the trends in energy production based on the energy source(Fossil Fuels vs. Renewables)over time. This will give us insights

"""

hist_data['Year'] = hist_data['Date/Time'].dt.year
hist_data['Year'] = hist_data['Date/Time'].dt.year
hist_data['Month'] = hist_data['Date/Time'].dt.month

monthly_aggregated_data = hist_data.groupby(['Year', 'Month', 'Energy Source'])['Energy Production (kWh)'].sum().reset_index()

monthly_aggregated_data['Year-Month'] = monthly_aggregated_data['Year'].astype(str) + '-' + monthly_aggregated_data['Month'].astype(str)


plt.figure(figsize=(12, 4))

sns.lineplot(data=monthly_aggregated_data, x='Year-Month', y='Energy Production (kWh)', hue='Energy Source', palette='viridis')
plt.title('Monthly Aggregated Energy Production by Energy Source')
plt.xlabel('Date')
plt.ylabel('Energy Production (kWh)')

plt.grid(True, which ='both', linestyle='--', linewidth=0.5)
labels = monthly_aggregated_data['Year-Month'].tolist()
n = 4
plt.xticks(labels[::n], rotation=360)
plt.tight_layout()

plt.show()

"""General Insights:

1.Dynamic Energy Landcsape: Energix Enterprise experiences marked variances in energy production, consumption and demand patterns.
2.Pricing Volatility: Energix's energy pricing exhibits variabbility with broader market price trends.
3.Infrastructure and Technology Concerns:A significamt portion of the comapny's infrastructure is categorized as 'poor'.
4.Regulatory & financial Implications: Energiz is continually navigating a changing regulatory landscape, with new madates and modifications to existing ones.
5.Emergence of Renewables: The energy market is witnessing a paradigm shift with renewables gaianing prominence.

Resilience pla
"""