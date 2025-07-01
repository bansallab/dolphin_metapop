#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 15:54:10 2024

@author: melissacollier
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import datetime
import random


data = pd.read_csv("Distance_from_shore_all_dolphins_all_sightings.csv")
    
X = data.iloc[:,2:3].values

wcss = []
for i in range(1,11):
    k_means = KMeans(n_clusters=i,init='k-means++', random_state=42)
    k_means.fit(X)
    wcss.append(k_means.inertia_)
#plot elbow curve
plt.plot(np.arange(1,11),wcss)
plt.xlabel('Clusters')
plt.ylabel('SSE')
plt.show()

k_means_optimum = KMeans(n_clusters = 3, init = 'k-means++',  random_state=42)
y = k_means_optimum.fit_predict(X)
print(y)

data['cluster_stock'] = y  

Est = data[data.cluster_stock==2]
Est['Stock'] = "E"
Coast = data[data.cluster_stock==1]
Coast["Stock"] = "C"
Other = data[data.cluster_stock == 0]
Other["Stock"] = "U"        

final = pd.concat([Est, Coast,Other])
#final.to_csv("All_PCdolphins_with_cluster_stocks_distance_from_shore.csv")

###############################################################################
df = pd.read_csv("All_PCDP_Sightings.csv", parse_dates=['Sighting_Date'])
sightings = list(df.Observation_ID_final.unique())

stocks = []
for index, row in df.iterrows():
    dolphin = row['Number_ID']
    stock_data = final.loc[final['dolphin']== dolphin]
    stock = stock_data["Stock"].iloc[0]
    stocks.append(stock)
    
df['Stock'] = stocks
#df = df[df.year.isin([2018])]

mixing = []

for sighting in sightings:
    sight_data = df.loc[df['Observation_ID_final']== sighting]
    date = sight_data["Sighting_Date"].iloc[0]
    month = date.month

    total_dolphins = len(sight_data.index)
    stocks_present = list(sight_data["Stock"].unique())
    if 'U' in stocks_present:
        stocks_present.remove('U')
        if len(stocks_present) ==2:
            mixing.append(1)
        else: 
            print('unknown stocks, drop')
            #mix = 0
    else: 
        if len(stocks_present) == 1:
            mixing.append(0)
        else: 
            mixing.append(1)
    

    
print(np.mean(mixing))
print(len(mixing), "is the number of surveys used")
print(len(Est.index)+len(Coast.index), "is the number of high conf est and coastal dolphins")
alphas = []
for i in range(0,999):
    boot = random.choices(mixing, k =200)
    alpha = np.mean(boot)
    alphas.append(alpha)

print("The bootstrapped alpha mean is: ", round(np.mean(alphas), 2))



    
    


