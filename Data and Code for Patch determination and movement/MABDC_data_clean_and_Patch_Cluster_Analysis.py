#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:07:36 2022

@author: melissacollier
"""

import scipy.cluster.hierarchy as hac
from scipy import cluster
from scipy.cluster.hierarchy import fcluster
import pandas as pd
import datetime
from datetime import datetime, date, time, timedelta, timezone
import random
import numpy as np

df = pd.read_csv('MABDC_sighting_data.csv', parse_dates = ['sight_date'] )


summer= [7,8,9]
winter = [1,2,3]
transition = [4,5,6,10,11,12]

season = []
months = []

## assign a season to each sighting
for value in df["sight_date"]:
    
    month = datetime.date(value).month
    months.append(month)
    if month in summer:   
        s = 1
    elif month in winter:
        s =2
    else: s = 3
    
    season.append(s)



df['Season'] = season
df['month'] = months

## only get dolphins with at least 5 sighitngs seen in each of the 3 main seasons
warm_and_cold_dolphins = []
all_dolphins = list(df['dolphin_id'].unique())

for dolphin in all_dolphins:
    sightings = df.loc[df['dolphin_id'] == dolphin]
    seasons = list(sightings['Season'].unique())
    if sightings.shape[0] >=5:
        if len(seasons) == 3: 
             warm_and_cold_dolphins.append(dolphin)
        else: print("only seen one season")
    else: print("Less than 5 sighitngs")

print("The number of dolphins seen in each season at least 5 times is: ", len(warm_and_cold_dolphins))    

wcdf = df.copy()

for index, row in wcdf.iterrows():
    
    if row['dolphin_id'] not in warm_and_cold_dolphins:
        wcdf.drop(index, inplace=True)


##### Cluster dolphins by similar seasonal sighting histories 

df_indiv_loc = wcdf # get data from file where columns are time, indiv, latitude
df_indiv_loc = df_indiv_loc.pivot_table(index = 'dolphin_id', columns='Season', values='lat', aggfunc='mean').reset_index(drop=True)

# clean up dataframe by making all Nans and negative values 0    
df_indiv_loc = df_indiv_loc.fillna(0)
df_indiv_loc = df_indiv_loc.clip(lower=0)

num_clusters =[2,3,4,5,6,7] # loop over 2-7 cluster values

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# set up the time series linkage matrix for clustering
Z = hac.linkage(df_indiv_loc, method='ward')
cutree = cluster.hierarchy.cut_tree(Z, n_clusters=[4])

num_clusters = [2, 3, 4, 5, 6, 7]
X = df_indiv_loc

fig, ax = plt.subplots(3, 2, figsize=(15, 12))
fig.suptitle("Silhouette Plots for KMeans Clustering", fontsize=18)

highlight_ax = None

for idx, n in enumerate(num_clusters):
    kmeans = KMeans(n_clusters=n, random_state=42)
    labels = kmeans.fit_predict(X)

    silhouette_avg = silhouette_score(X, labels)
    sample_silhouette_values = silhouette_samples(X, labels)

    row = idx // 2
    col = idx % 2
    ax_i = ax[row][col]

    if n == 4:
        highlight_ax = ax_i

    y_lower = 10
    for i in range(n):
        ith_cluster_silhouette_values = sample_silhouette_values[labels == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        ax_i.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ith_cluster_silhouette_values,
            alpha=0.7
        )

        ax_i.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10

    ax_i.set_title(f"P = {n}, avg silhouette = {silhouette_avg:.2f}", fontsize=14)
    ax_i.set_xlabel("Silhouette coefficient")
    ax_i.set_ylabel("Cluster label")
    ax_i.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax_i.set_xlim([-0.1, 1])

# Do layout first to get correct subplot positions
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Add red rectangle *after* layout
if highlight_ax:
    bbox = highlight_ax.get_position()
    rect = patches.Rectangle(
        (bbox.x0, bbox.y0),
        bbox.width,
        bbox.height,
        linewidth=3,
        edgecolor='red',
        facecolor='none',
        transform=fig.transFigure,
        zorder=10
    )
    fig.add_artist(rect)

# Save figure with rectangle visible
plt.savefig("silhouette_plots.png", dpi=300)
plt.show()

for n in num_clusters:
# do time series clustering
    results = fcluster(Z, t=n, criterion='maxclust')
    
    model = KMeans(n, random_state=42) #seed 42 for reproducable results
    q, mod = divmod(n, 2)
    # the results just tell you which partition each node (animal) is in, so this attaches the node ids to the cluster ids
    partition = dict(zip(warm_and_cold_dolphins, results))
    clusterdf = pd.DataFrame(partition.items(), columns=['Dolphin', 'Cluster'])
    clusters = []
    
    for index, row in wcdf.iterrows():
        ID = int(row['dolphin_id'])
        cluster = partition[ID]
        clusters.append(cluster)  
    
    wcdf['Cluster'] = clusters
    summer_df = wcdf[wcdf["Season"] == 1]
    if n == 4: #only save 4 cluster results since we know this is best division
        wcdf.to_csv("cluster_results"+ str(n) +".csv")
        summer_df.to_csv("warm_water_cluster_results" + str(n) +".csv")



#### Figure and cluster results say 4 clusters is best, so we will divide the coastline
#### into 4 patches based on the warm water season sightings of each cluster

dfsummer4 = pd.read_csv('warm_water_cluster_results4.csv')
dolphins = dfsummer4.dolphin_id.unique()
columns =[ "Dolphin", "lat", "lon", "Cluster"]
rows = []
for d in dolphins:
    subdf = dfsummer4[(dfsummer4["dolphin_id"] == d)]
    lat = np.mean(subdf['lat'])
    long= np.mean(subdf['lon'])
    clust = subdf['Cluster'].iloc[0]
    row = [d, lat, long, clust]
    rows.append(row)

dfsummer4_avg = pd.DataFrame(rows, columns= columns) 

clusters = list(dfsummer4_avg['Cluster'].unique())
#clusters.sort()

ranges = []
maxes = []
mins = []

## look for the min and max latitude of dolphin sightings in each cluster
for c in clusters:
    
    cdf = dfsummer4_avg.loc[dfsummer4_avg["Cluster"] == c]
        
    maxlat = max(cdf['lat'])
    minlat = min(cdf['lat'])
        
    mins.append(minlat)
    maxes.append(maxlat)
    
maxes.sort()
mins.sort()
ranges = list(zip(maxes, mins))

i = 0
lines = []
for m in maxes:
    
    if m < maxes[3] :
        
        range1max, range1min = ranges[i]
        range2max, range2min = ranges[i+1]

        
        if range2min < range1max:
            overlap = range2min- range1max # get the amount that they overlap
            line = range1max + (overlap/2) # draw line in the middle of the overlap
            lines.append(line)
        else: 

            line = (range2min +range1max)/2
            lines.append(line)
        
    i = i+1

print("Draw patch boundaries between patch 1 and 2 at latitude: ", lines[0])      
    
print("Draw patch boundaries between patch 2 and 3 at latitude: ", lines[1])      
    
print("Draw patch boundaries between patch 3 and 4 at latitude: ", lines[2])      
    







