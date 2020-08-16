# import packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.seasonal import seasonal_decompose


def make_plot(y_train, y_test, columns):
    """
    This function plots predictions and compares them to the actual test data
    Parameters:
    y_train = df of training data
    y_test = df of test data
    columns = List of strings
    """
    y_train.resample('w').mean()['2010':'2019']['temp'].plot(label = 'Training Data')
    y_test.resample('w').mean()['temp'].plot(label='Test data')
    for column in columns:
        y_test.resample('w').mean()[column].plot(label=column)
    plt.title = 'Temperature prediction for Berlin Tempelhof'
    plt.xlabel = 'time'
    plt.ylabel = 'temperature'
    plt.legend()


# Set standard plotting size
plt.rcParams['figure.figsize'] = (16, 9)

# Read in the data
df = pd.read_csv('_RES/TG_STAID002759.txt', sep=',', skiprows=19)

# Check column names
df.columns
df.rename(columns={' SOUID': 'souid', '    DATE': 'date', '   TG': 'temp',
    ' Q_TG': 'quality'}, inplace=True)

# DateTime features
df['DateTime'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
df['year'] = df['DateTime'].dt.year
df['month'] = df['DateTime'].dt.month
df['week'] = df['DateTime'].dt.week
df['day'] = df['DateTime'].dt.day
df.drop('date', axis=1, inplace=True)
df.set_index('DateTime', inplace=True)

# convert temperature to degrees in Celsius
df['temp'] = df['temp'] * 0.1

# Imputation
s_1945_new = pd.Series((df['1946-04-25':'1946-11-05']['temp'].values + df['1944-04-25':'1944-11-05']['temp'].values)*0.5)
s_1945_new.index = df['1945-04-25':'1945-11-05'].index
df.loc['1945-04-25':'1945-11-05','temp'] = s_1945_new

# Shift temperature values
df['temp'].min()
df['temp_shifted'] = df['temp'] + 25

# Delete souid column
df['souid'].unique()
df.drop('souid', axis=1, inplace=True)

# Split into train and test data sets
y_train = df[:'2019'].copy()
y_test = df['2020'].copy()


# Last 365 days
ax = y_train.tail(365)['temp'].plot(title='Temperature in Berlin, Tempelhof, 2019 in °C')
ax.set_xlabel='2019'
ax.set_ylabel='Temperature in °C'
plt.show()

# Group by daily average
y_train.groupby(['day']).mean()

# Resample by month
y_train.resample('M').mean()
y_train.resample('y').mean()['temp'].plot()

# Remove The Trend
y_train['temp_diff'] = y_train['temp'].diff()
y_train.resample('y').mean()['temp_diff'].plot()

# Second Order Differencing
y_train['temp_diff_second'] = y_train['temp_diff'].diff()
y_train.resample('2y')['temp_diff'].mean().plot()
y_train.resample('2y')['temp_diff_second'].mean().plot()
plt.legend()
plt.show()

# Calculate percentage change with shifted temperature data
y_train['pct_change'] = y_train['temp_shifted'].pct_change()
y_train['2019']['pct_change'].describe()
y_train['2000':'2020']['pct_change'].resample('m').mean().plot()

# Deseasonalize by subtracting the monthly mean
y_train['monthly_means'] = y_train.groupby('month')['temp_diff'].transform('mean')
y_train['deseasonalized'] = y_train['temp_diff'] - y_train['monthly_means']
y_train['deseasonalized'].mean()
y_train['1920':'2020'].resample('6m').mean()['deseasonalized'].plot()

# Add the mean value of temperature as prediction for y_test
y_test['y_pred_mean'] = y_train['temp'].mean()

make_plot(y_train, y_test, ['y_pred_mean'])
# This doesn't look like anything to me

# Plot mean of detrended df
y_test['y_pred_pct_change_mean'] = y_train['2000':'2019']['pct_change'].mean()
y_test['y_pred_pct_change_mean'] += 1

# Calculate the culmulative product of the mean percentage change
y_test['y_pred_pct_change_mean'] = np.cumprod(y_test['y_pred_pct_change_mean'])

# Define the intercept aka last starting point
intercept = y_train['temp'][-1]
y_test['y_pred_pct_change_mean'] *= intercept
make_plot(y_train, y_test, ['y_pred_pct_change_mean'])

# Let's see if we can take the seasonal patterns into account
y_train['monthly_means'].unique()
y_train['monthly_means'][:182]
y_test['y_pred_monthly_pct_mean'] = y_train['monthly_means'][:182].values
y_test['y_pred_monthly_pct_mean'] += 1
y_test['y_pred_monthly_pct_mean'] = np.cumprod(y_test['y_pred_monthly_pct_mean'])

make_plot(y_train, y_test, ['y_pred_monthly_pct_mean'])

# Persistance Forecast
y_test['y_pred_persistence'] = y_test['temp'].shift()
y_test.loc['2020-01-01','y_pred_persistence'] = intercept

make_plot(y_train, y_test, ['y_pred_persistence'])

# Plot all of them together
predictions = ['y_pred_mean', 'y_pred_pct_change_mean', 'y_pred_persistence']

make_plot(y_train, y_test, predictions)

# Compare all of them together
for prediction in predictions:
    print(f'{prediction} : {mean_absolute_error(y_test["temp"], y_test[prediction])}')
seasonal = seasonal_decompose(df['2010':'2020']['temp'])

seasonal.plot()
