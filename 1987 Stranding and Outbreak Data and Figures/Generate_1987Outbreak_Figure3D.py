#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 17:00:33 2024

"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
import random as rnd
import datetime

data = pd.read_csv('1987-1988_Outbreak_Data.csv')
data_full= data[data['Centroid.Latitude'].notna()]

#########data for all the patches###############

data_patch1 = data.loc[data['Centroid.Latitude'].ge(37.4) & data['Centroid.Latitude'].lt(40.5)]
data_patch1['Patch'] = 1
data_patch2 = data.loc[data['Centroid.Latitude'].ge(35) & data['Centroid.Latitude'].lt(37.4)]
data_patch2['Patch'] = 2
data_patch3 = data.loc[data['Centroid.Latitude'].ge(33.7) & data['Centroid.Latitude'].lt(35)]
data_patch3['Patch'] = 3
data_patch4 = data.loc[data['Centroid.Latitude'].ge(31) & data['Centroid.Latitude'].lt(33.7)]
data_patch4['Patch'] = 4

########N, S, and M patches

###A list of dataframes to generate data for POMP
dataframes = [data_patch1, data_patch2, data_patch3, data_patch4]

dates = [('1987-03-01', '1987-03-07'), ('1987-03-08', '1987-03-14'), ('1987-03-15', '1987-03-21'), ('1987-03-22', '1987-03-28'),
        ('1987-03-29', '1987-04-04'), ('1987-04-05', '1987-04-11'), ('1987-04-12', '1987-04-18'), ('1987-04-19', '1987-04-25'),
        ('1987-04-26', '1987-05-02'), ('1987-05-03', '1987-05-09'), ('1987-05-10', '1987-05-16'), ('1987-05-17', '1987-05-23'),
        ('1987-05-24', '1987-05-30'),
        ('1987-05-31', '1987-06-06'), ('1987-06-07', '1987-06-13'), ('1987-06-14', '1987-06-20'), ('1987-06-21', '1987-06-27'),
         ('1987-06-28', '1987-07-04'), ('1987-07-05', '1987-07-11'), ('1987-07-12', '1987-07-18'),
         ('1987-07-19', '1987-07-25'), ('1987-07-26', '1987-08-01'), ('1987-08-02', '1987-08-08'),
         ('1987-08-09', '1987-08-15'),
         ('1987-08-16', '1987-08-22'), ('1987-08-23', '1987-08-29'), ('1987-08-30', '1987-09-05'),
         ('1987-09-06', '1987-09-12'), ('1987-09-13', '1987-09-19'), ('1987-09-20', '1987-09-26'),
         ('1987-09-27', '1987-10-03'), ('1987-10-04', '1987-10-10'), ('1987-10-11', '1987-10-17'),
         ('1987-10-18', '1987-10-24'), ('1987-10-25', '1987-10-31'), ('1987-11-01', '1987-11-07'),
         ('1987-11-08', '1987-11-14'), ('1987-11-15', '1987-11-21'), ('1987-11-22', '1987-11-28'),
         ('1987-11-29', '1987-12-05'), ('1987-12-06', '1987-12-12'), ('1987-12-13', '1987-12-19'),
         ('1987-12-20', '1987-12-26'), ('1987-12-27', '1988-01-02'), ('1988-01-03', '1988-01-09'),
         ('1988-01-10', '1988-01-16'), ('1988-01-17', '1988-01-23'), ('1988-01-24', '1988-01-30'),
         ('1988-01-31', '1988-02-06'), ('1988-02-07', '1988-02-13'), ('1988-02-14', '1988-02-20'),
         ('1988-02-21', '1988-02-27'), ('1988-02-28', '1988-03-06'), ('1988-03-07', '1988-03-13'), 
         ('1988-03-14', '1988-03-20'), ('1988-03-21', '1988-03-27'), ('1988-03-28', '1988-04-03'),
         ('1988-04-04', '1988-04-10'), ('1988-04-11', '1988-04-17'), ('1988-04-18', '1988-04-24'),
         ('1988-04-25', '1988-05-01'), ('1988-05-02', '1988-05-08'), ('1988-05-09', '1988-05-15'), 
         ('1988-05-16', '1988-05-22'), ('1988-05-23', '1988-05-29'), ('1988-05-30', '1988-06-05'),
         ('2014-06-06', '2014-06-12'), ('2014-06-13', '2014-06-19'), ('2014-06-20', '2014-06-26'), 
         ('2014-06-27', '2014-07-03'), ('2014-07-04', '2014-07-10'), ('2014-07-11', '2014-07-17'),
         ('2014-07-18', '2014-07-24'), ('2014-07-25', '2014-07-31'), ('2014-08-01', '2014-08-07'),
         ('2014-08-08', '2014-08-14'), ('2014-08-15', '2014-08-21'), ('2014-08-22', '2014-08-28'),
         ('2014-08-29', '2014-09-04'), ('2014-09-05', '2014-09-11')]

formatted_dates = []

weeks = range(len(dates))

##blank list to add the infections to
infections = []

for d in dataframes:
    ####For every date in the date list###
    for (x,y)in dates:

       # week = d.loc[(d['Observation.Date'] > x) & (d['Observation.Date'] <= y)]
        week = d.loc[(d['Estimated_Infection_Date'] > x) & (d['Estimated_Infection_Date'] <= y)]
        
        r, c = week.shape
        infections.append(r) ##r is the number of rows in the data (or number of new infections)   
        if len(infections) == len(weeks)+1: #This part of the code will stop adding to the infected list when after 88 weeks and start a new infected list for the next dataframe
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
normalized_df.to_csv("Normalized_Weekly_Infections_By_Patch1987.csv", index=False)

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
week_labels = ["Mar", "May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jun", "Sep"]
plt.xticks(np.arange(0, 90, step=10),labels=week_labels, rotation = 45, size= 10)
plt.yticks(size = 10)
#plt.xlabel('Estimated Week of Infection', size = 15)
plt.ylabel('Observed Infections', size = 15)
#plt.show()
plt.savefig("Patches_Combined_points_1987.jpg", dpi= 300, bbox_inches='tight')
#plt.close()

