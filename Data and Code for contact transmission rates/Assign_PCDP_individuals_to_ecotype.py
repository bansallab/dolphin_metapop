#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:19:36 2024

@author: melissacollier
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

new_data = pd.read_csv("Focal_Individuals_avg_distance_from_shore.csv")

X = new_data.iloc[:,2:3].values

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

new_data['cluster'] = y 

# for n = 3, which is best division
Est = new_data[new_data.cluster==2]
Coast = new_data[new_data.cluster==1]
Other = new_data[new_data.cluster == 0]

final = pd.concat([Est, Coast, Other])

from sklearn.metrics import silhouette_score
score = silhouette_score(X,y)
print(score)

degree_data = pd.read_csv("Clean_Degree_Data_PCDP.csv")

ecotype = final

Stock = []

dolphins = list(ecotype.Focal_ID.unique())

for index, row in degree_data.iterrows():
    ID = row['Dolphin_ID']
    if ID in dolphins:
        for index, row in ecotype.iterrows():
            if ID == row['Focal_ID']:
                c = row['cluster']
                dist = row["Average_distance"]
                if c == 2:
                    stock = "Est"
                elif c== 1:
                    stock = "Coast"
                else: 
                    stock = "Undetermined"   
    else: 
        stock = "Undetermined"
    
    Stock.append(stock)

degree_data["Stock"] = Stock
  
degree_data.to_csv("Clean_Degree_Data_PCDP_withStock_Assignments.csv")  

