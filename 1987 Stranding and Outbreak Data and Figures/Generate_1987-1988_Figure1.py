#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 14:01:02 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
import datetime
import random as rnd
'''
Generate Figure 1 for 1987 and 1988 strandings
'''
data = pd.read_csv('1987-1988_Stranding_Data.csv')

######################################################################################3

data_NJ = data.loc[data['Province/State'] == "New Jersey"]
data_DE = data.loc[data['Province/State'] == "Delaware"]
data_MD = data.loc[data['Province/State'] == "Maryland"]
data_VA = data.loc[data['Province/State'] == "Virginia"]
data_NC = data.loc[data['Province/State'] == "North Carolina"]
data_SC = data.loc[data['Province/State'] == "South Carolina"]
data_GA = data.loc[data['Province/State'] == "Georgia"]

dataframes = [data, data_NJ, data_DE, data_MD, data_VA, data_NC, data_SC, data_GA]


###Divide the 88 weeks up to count the number of new infections each week during the epidemic.
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
         ('1988-06-06', '1988-06-12'),('1988-06-13', '1988-06-19'),('1988-06-20', '1988-06-26'),
         ('1988-06-27', '1988-07-02'),('1988-07-03', '1988-07-09'),('1988-07-10', '1988-07-16'),
         ('1988-07-17', '1988-07-23'), ('1988-07-24', '1988-07-30'), ('1988-07-31', '1988-08-06'),
         ('1988-08-07', '1988-08-13'), ('1988-08-14', '1988-08-20'), ('1988-08-21', '1988-08-27'),
         ('1988-08-28', '1988-09-3'),('1988-09-04', '1988-09-10')]
formatted_dates = []

weeks = range(len(dates))

##blank list to add the infections to
infections = []

i =0
for d in dataframes:
    ####For every date in the date list###
    for (x,y)in dates:

       # week = d.loc[(d['Observation.Date'] > x) & (d['Observation.Date'] <= y)]
        week = d.loc[(d['Date Collected'] > x) & (d['Date Collected'] <= y)]
        
        r, c = week.shape
        infections.append(r) ##r is the number of rows in the data (or number of new infections)   
        if len(infections) == len(weeks)+1: #This part of the code will stop adding to the infected list when after 88 weeks and start a new infected list for the next dataframe
            infections = [r]
    
    ##Create a new dataframe and csv file for each dataframe
    final = {'week': weeks, 'cases': infections}
    #print(final)
    df = pd.DataFrame(data = final)
    if i ==0:
        df_id = 'full'
    else:
        df_id=d['Province/State'].iloc[0]
    file_name="id_"+str(df_id)+".csv"
    df.to_csv(file_name, index = False)
    i =i +1
    
NJ = pd.read_csv("id_New Jersey.csv")
DE = pd.read_csv("id_Delaware.csv")
MD = pd.read_csv("id_Maryland.csv")
VA = pd.read_csv("id_Virginia.csv")
NC = pd.read_csv("id_North Carolina.csv")
SC = pd.read_csv("id_South Carolina.csv")
GA = pd.read_csv("id_Georgia.csv")


##connected lines
plt.plot( NJ['week'], NJ['cases'],color='#5302a3')
plt.plot( DE['week'], DE['cases'],color='#8b0aa5')
plt.plot( MD['week'], MD['cases'],color='#b83289')
plt.plot( VA['week'], VA['cases'],color='#db5c68')
plt.plot( NC['week'], NC['cases'],color='#f48849')
plt.plot( SC['week'], SC['cases'],color='#febd2a')
plt.plot( GA['week'], GA['cases'],color='#f0f921')


### points
plt.plot( NJ['week'], NJ['cases'],"o", markersize = 3, label="New Jersey", color='#5302a3')
plt.plot( DE['week'], DE['cases'],"o", markersize = 3, label="Delaware", color='#8b0aa5')
plt.plot( MD['week'], MD['cases'],"o", markersize = 3, label="Maryland", color='#b83289')
plt.plot( VA['week'], VA['cases'],"o", markersize = 3, label="Virginia", color='#db5c68')
plt.plot( NC['week'], NC['cases'],"o", markersize = 3, label="North Carolina", color='#f48849')
plt.plot( SC['week'], SC['cases'],"o", markersize = 3, label="South Carolina", color='#febd2a')
plt.plot( GA['week'], GA['cases'],"o", markersize = 3, label="Georgia", color='#f0f921')
# show legend
plt.title("1987-1988", size = 20)
plt.legend()
#plt.xlim(0, 90)
week_labels = ["Mar", "May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jun", "Sep"]
plt.xticks(np.arange(0, 90, step=10),labels=week_labels, rotation = 45, size= 10)
plt.yticks(size = 10)
#plt.xlabel('Estimated Week of Infection', size = 15)
plt.ylabel('Number of Stranded Animals', size = 15)
#plt.show()
#plt.savefig("1987_Stranding_Data.jpg", dpi= 300, bbox_inches='tight')
#plt.close()




