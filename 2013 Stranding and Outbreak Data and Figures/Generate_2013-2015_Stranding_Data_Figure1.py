#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:46:24 2019

"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
import datetime
import random as rnd
'''
Clean data to have only strandings from GA thorugh NY coasts, during the dates
of the UME, and only bottlenose dolphins.
Then delete all the columns that aren't needed.
'''
data= pd.read_csv('2013-2015_Stranding_Data.csv', encoding = "ISO-8859-1")

data_NY = data.loc[data['State'] == "NY"]
data_NJ = data.loc[data['State'] == "NJ"]
data_DE = data.loc[data['State'] == "DE"]
data_MD = data.loc[data['State'] == "MD"]
data_VA = data.loc[data['State'] == "VA"]
data_NC = data.loc[data['State'] == "NC"]
data_SC = data.loc[data['State'] == "SC"]
data_GA = data.loc[data['State'] == "GA"]

dataframes = [data_NY, data_NJ, data_DE, data_MD, data_VA, data_NC, data_SC, data_GA]


###Divide the 88 weeks up to count the number of new infections each week during the epidemic.
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
         ('2014-08-29', '2014-09-04'), ('2014-09-05', '2014-09-11')]
formatted_dates = []

weeks = range(len(dates))

##blank list to add the infections to
infections = []

##For every state we want to view strandings for 
for d in dataframes:
    ####For every date in the date list###
    for (x,y)in dates:

        week = d.loc[(d['Observation Date'] > x) & (d['Observation Date'] <= y)]
        
        r, c = week.shape
        infections.append(r) ##r is the number of rows in the data (or number of new infections)   
        if len(infections) == len(weeks)+1: #This part of the code will stop adding to the infected list when after 88 weeks and start a new infected list for the next dataframe
            infections = [r]

    
    ##Create a new dataframe and csv file for each dataframe
    final = {'week': weeks, 'cases': infections}
    #print(final)
    df = pd.DataFrame(data = final)
    
    df_id=d['State'].iloc[0]
    file_name="id_"+str(df_id)+".csv"
    df.to_csv(file_name, index = False)
    

NY = pd.read_csv("id_NY.csv")
NJ = pd.read_csv("id_NJ.csv")
DE = pd.read_csv("id_DE.csv")
MD = pd.read_csv("id_MD.csv")
VA = pd.read_csv("id_VA.csv")
NC = pd.read_csv("id_NC.csv")
SC = pd.read_csv("id_SC.csv")
GA = pd.read_csv("id_GA.csv")


##connected lines
plt.plot( NY['week'], NY['cases'],color='#0d0887')
plt.plot( NJ['week'], NJ['cases'],color='#5302a3')
plt.plot( DE['week'], DE['cases'],color='#8b0aa5')
plt.plot( MD['week'], MD['cases'],color='#b83289')
plt.plot( VA['week'], VA['cases'],color='#db5c68')
plt.plot( NC['week'], NC['cases'],color='#f48849')
plt.plot( SC['week'], SC['cases'],color='#febd2a')
plt.plot( GA['week'], GA['cases'],color='#f0f921')


### points
plt.plot( NY['week'], NY['cases'],"o", markersize = 3, label="New York", color='#0d0887')
plt.plot( NJ['week'], NJ['cases'],"o", markersize = 3, label="New Jersey", color='#5302a3')
plt.plot( DE['week'], DE['cases'],"o", markersize = 3, label="Delaware", color='#8b0aa5')
plt.plot( MD['week'], MD['cases'],"o", markersize = 3, label="Maryland", color='#b83289')
plt.plot( VA['week'], VA['cases'],"o", markersize = 3, label="Virginia", color='#db5c68')
plt.plot( NC['week'], NC['cases'],"o", markersize = 3, label="North Carolina", color='#f48849')
plt.plot( SC['week'], SC['cases'],"o", markersize = 3, label="South Carolina", color='#febd2a')
plt.plot( GA['week'], GA['cases'],"o", markersize = 3, label="Georgia", color='#f0f921')
# show legend
plt.title("2013-2014", size = 20)
plt.legend()
#plt.xlim(0, 90)
week_labels = ["Mar", "May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jun", "Sep"]
plt.xticks(np.arange(0, 90, step=10),labels=week_labels, rotation = 45, size= 10)
plt.yticks(size = 10)
#plt.xlabel('Estimated Week of Infection', size = 15)
plt.ylabel('Number of Stranded Animals', size = 15)
#plt.show()
#plt.savefig("Figures/Figure_1_Stranding_Data.jpg", dpi= 300, bbox_inches='tight')
#plt.close()






