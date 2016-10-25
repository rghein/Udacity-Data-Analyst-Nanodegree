import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

################################################################################################
##
##  Udacity Data Analyst Nanodegree "Investigate A Dataset" Project


##  Read in data files and convert to pandas dataframes:

players = pd.read_csv('Master.csv')
batters = pd.read_csv('Batting.csv')

##  Limit dataframes to the data used in analysis:

players = players[['playerID', 'height', 'weight']]
batters = batters[['playerID', 'yearID', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'HBP', 'SF']]

##  Limit data to players with a minimum number of 100 At Bats per season, in an attempt
##  to minimize outliers using a conservative representation of MLB's requirements for batting title
##  (https://en.wikipedia.org/wiki/Batting_average#Qualifications_for_the_batting_title):

batters = batters[batters['AB'] >= 100.0]

##  Merge batters dataframe with players dataframe.
##  Using dropna() to eliminate rows with missing data:

data = batters.merge(players, on = 'playerID', how = 'left').dropna(how = 'any')

##  Add Batting Average, On Base Percentage, Slugging Percentage,
##  and On Base Percentage Plus Slugging Percentage to Dataframe:

##  Batting Average:
data['BA'] = data['H'] / data['AB']

##  On Base Percentage:
data['OBP'] = (data['H'] + data['BB'] + data['HBP']) / (data['AB'] + data['BB'] + data['HBP'] + data['SF'])

##  Slugging Percentage:
data['SLG'] = (data['H'] + data['2B'] + (2 * data['3B']) + (3 * data['HR'])) / data['AB']

##  On Base Percentage plus Slugging Percentage:
data['OPS'] = data['OBP'] + data['SLG']

##  The variables being considered:

player_characteristics = ['height', 'weight']
batting_metrics = ['BA', 'OBP', 'SLG', 'OPS']
all_variables = player_characteristics + batting_metrics

##  The number of data points (Player years):

print 'The number of data points: ', len(data['height'])
print ''

##  The Mean & Standard Deviation of each variable being analyzed:

print 'Mean & Standard Deviation of each variable:'
print ''
for variable in all_variables:
    print variable, data[variable].mean(), '&', data[variable].std()
print ''

##  Histograms of the variables being analyzed:

def display_histogram(variable, bar_color, num_bins):
    plt.hist(data[variable].dropna().values, bins = num_bins, color = bar_color)
    plt.xlabel('Player ' + variable + ' (mean is: ' + str(round(data[variable].mean(), 2)) + ')')
    plt.ylabel('Number of Player Years')
    plt.title('Histogram of Player ' + variable)
    plt.show()
    return

number_of_bins = [17, 18, 21, 21, 21, 21]
colors = ['yellow', 'green', 'red', 'blue', 'orange', 'brown']

for i in range(len(all_variables)):
    display_histogram(all_variables[i], colors[i], number_of_bins[i])

##  Scatter Plots:

def show_scatter_plot(characteristic, metric, data_color):
    plt.scatter(data[characteristic], data[metric], color = data_color)
    plt.xlabel('Player ' + characteristic)
    plt.ylabel('Batter ' + metric)
    plt.title('Player ' + characteristic + '/' + 'Batter ' + metric)
    plt.show()
    return

for i in range(len(player_characteristics)):
    for j in range(len(batting_metrics)):
        char, metric = player_characteristics[i], batting_metrics[j]
        show_scatter_plot(char, metric, colors[j])

##  Pearson's r and p-values for all comparisons:

print 'Pearson Correlation Coefficients & p-values:'
print ''
for i in range(len(player_characteristics)):
    for j in range(len(batting_metrics)):
        char, metric = player_characteristics[i], batting_metrics[j]
        print  char + '/' + metric, pearsonr(data[char], data[metric])
