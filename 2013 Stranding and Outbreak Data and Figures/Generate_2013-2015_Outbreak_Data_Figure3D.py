#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:00:33 2024

"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

data = pd.read_csv('2013-2015_Final_Outbreak_Data.csv', encoding = "ISO-8859-1")
'''
Produce new csvs for each state that shows the epidemic size for each week
of the UME. We will use four patches to divide the strandings
'''
#########data for each patch###############

data_patch1 = data.loc[data['Latitude'].ge(37.4) & data['Latitude'].lt(40.5)]
data_patch1['Patch'] = 1
data_patch2 = data.loc[data['Latitude'].ge(35) & data['Latitude'].lt(37.4)]
data_patch2['Patch'] = 2
data_patch3 = data.loc[data['Latitude'].ge(33.7) & data['Latitude'].lt(35)]
data_patch3['Patch'] = 3
data_patch4 = data.loc[data['Latitude'].ge(31) & data['Latitude'].lt(33.7)]
data_patch4['Patch'] = 4

dataframes = [data_patch1, data_patch2, data_patch3, data_patch4, data]

###Divide the weeks up to count the number of new infections each week during the epidemic.
dates = [('2013-03-01', '2013-03-07'), ('2013-03-08', '2013-03-14'), ('2013-03-15', '2013-03-21'), ('2013-03-22', '2013-03-28'),
        ('2013-03-29', '2013-04-04'), ('2013-04-05', '2013-04-11'), ('2013-04-12', '2013-04-18'), ('2013-04-19', '2013-04-25'),
        ('2013-04-26', '2013-05-02'), ('2013-05-03', '2013-05-09'), ('2013-05-10', '2013-05-16'), ('2013-05-17', '2013-05-23'),
        ('2013-05-24', '2013-05-30'),
        ('2013-05-31', '2013-06-06'), ('2013-06-07', '2013-06-13'), ('2013-06-14', '2013-06-20'), ('2013-06-21', '2013-06-27'),
         ('2013-06-28', '2013-07-04'), ('2013-07-05', '2013-07-11'), ('2013-07-12', '2013-07-18'),
         ('2013-07-19', '2013-07-25'), ('2013-07-26', '2013-08-01'), ('2013-08-02', '2013-08-08'),
         ('2013-08-09', '2013-08-15'),
         ('2013-08-16', '2013-08-22'), ('2013-08-23', '2013-08-29'), ('2013-08-30', '2013-09-05'),
         ('2013-09-06', '2013-09-12'), ('2013-09-13', '2013-09-19'), ('2013-09-20', '2013-09-26'),
         ('2013-09-27', '2013-10-03'), ('2013-10-04', '2013-10-10'), ('2013-10-11', '2013-10-17'),
         ('2013-10-18', '2013-10-24'), ('2013-10-25', '2013-10-31'), ('2013-11-01', '2013-11-07'),
         ('2013-11-08', '2013-11-14'), ('2013-11-15', '2013-11-21'), ('2013-11-22', '2013-11-28'),
         ('2013-11-29', '2013-12-05'), ('2013-12-06', '2013-12-12'), ('2013-12-13', '2013-12-19'),
         ('2013-12-20', '2013-12-26'), ('2013-12-27', '2014-01-02'), ('2014-01-03', '2014-01-09'),
         ('2014-01-10', '2014-01-16'), ('2014-01-17', '2014-01-23'), ('2014-01-24', '2014-01-30'),
         ('2014-01-31', '2014-02-06'), ('2014-02-07', '2014-02-13'), ('2014-02-14', '2014-02-20'),
         ('2014-02-21', '2014-02-27'), ('2014-02-28', '2014-03-06'), ('2014-03-07', '2014-03-13'), 
         ('2014-03-14', '2014-03-20'), ('2014-03-21', '2014-03-27'), ('2014-03-28', '2014-04-03'),
         ('2014-04-04', '2014-04-10'), ('2014-04-11', '2014-04-17'), ('2014-04-18', '2014-04-24'),
         ('2014-04-25', '2014-05-01'), ('2014-05-02', '2014-05-08'), ('2014-05-09', '2014-05-15'), 
         ('2014-05-16', '2014-05-22'), ('2014-05-23', '2014-05-29'), ('2014-05-30', '2014-06-05'),
         ('2014-06-06', '2014-06-12'), ('2014-06-13', '2014-06-19'), ('2014-06-20', '2014-06-26'), 
         ('2014-06-27', '2014-07-03'), ('2014-07-04', '2014-07-10'), ('2014-07-11', '2014-07-17'),
         ('2014-07-18', '2014-07-24'), ('2014-07-25', '2014-07-31'), ('2014-08-01', '2014-08-07'),
         ('2014-08-08', '2014-08-14'), ('2014-08-15', '2014-08-21'), ('2014-08-22', '2014-08-28'),
         ('2014-08-29', '2014-09-04'), ('2014-09-05', '2014-09-11')
         ]

formatted_dates = []

weeks = range(len(dates))

##blank list to add the infections to
infections = []

##For every dataframe we want to generate data for
for d in dataframes:
    ####For every date in the date list###
    for (x,y)in dates:
        week = d.loc[(d['Estimated_Infection_Date'] > x) & (d['Estimated_Infection_Date'] <= y)]
        
        r, c = week.shape
        infections.append(r) ##r is the number of rows in the data (or number of new infections)   
        if len(infections) == len(weeks)+1: 
            infections = [r]
    
    ##Create a new dataframe and csv file for each dataframe
    final = {'week': weeks, 'cases': infections}
    #print(final)
    df = pd.DataFrame(data = final)
    
    df_id=d['Patch'].iloc[0]
    file_name="id_"+str(df_id)+".csv"
    df.to_csv(file_name, index = False)
    
Patch1 = pd.read_csv("id_1.csv")
Patch2 = pd.read_csv("id_2.csv")
Patch3 = pd.read_csv("id_3.csv")
Patch4 = pd.read_csv("id_4.csv")

# Combine into one DataFrame
combined_df = pd.DataFrame({
    'week': Patch1['week'],
    'patch_1': Patch1['cases'],
    'patch_2': Patch2['cases'],
    'patch_3': Patch3['cases'],
    'patch_4': Patch4['cases'],
})

# Normalize by the max value across all patches and weeks
max_val = combined_df[['patch_1', 'patch_2', 'patch_3', 'patch_4']].values.max()
normalized_df = combined_df.copy()
normalized_df[['patch_1', 'patch_2', 'patch_3', 'patch_4']] = normalized_df[['patch_1', 'patch_2', 'patch_3', 'patch_4']] / max_val

# Save to CSV
normalized_df.to_csv("Normalized_Weekly_Infections_By_Patch2013.csv", index=False)

##connected lines
plt.plot( Patch1['week'], Patch1['cases'],color='#fbb4b9')
plt.plot( Patch2['week'], Patch2['cases'],color='#f768a1')
plt.plot( Patch3['week'], Patch3['cases'], color='#c51b8a')
plt.plot( Patch4['week'], Patch4['cases'], color='#7a0177')


### points
plt.plot( Patch1['week'], Patch1['cases'],"o", markersize = 3, label="Patch 1", color='#fbb4b9')
plt.plot( Patch2['week'], Patch2['cases'],"o", markersize = 3,label="Patch 2", color='#f768a1')
plt.plot( Patch3['week'], Patch3['cases'],"o", markersize = 3,label="Patch 3", color='#c51b8a')
plt.plot( Patch4['week'], Patch4['cases'],"o", markersize = 3,label="Patch 4", color='#7a0177')
# show legend
week_labels = ["Mar", "May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jun", "Sep"]

plt.xticks(np.arange(0, 90, step=10),labels=week_labels, rotation = 45, size= 10)
plt.yticks(size = 10)
plt.ylabel('Observed Infections', size = 15)
#plt.show()
plt.savefig("Patches_Combined_points2013.jpg", dpi= 300, bbox_inches='tight')
#plt.close()

