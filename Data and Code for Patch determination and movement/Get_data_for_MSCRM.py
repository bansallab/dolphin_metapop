#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:17:28 2023

@author: mcollier
"""


import pandas as pd
import datetime
from datetime import datetime, date, time, timedelta, timezone
import random
import numpy as np
import csv

#df= pd.read_csv("qry_match_ids_sightings_to Melissa_20231009.csv", parse_dates = ['sight_date'])
df = pd.read_csv("cluster_results4.csv", parse_dates = ['sight_date'])

### add in a patch assignment for each sighting based on patch assignments
lat_gradients = []
for index, row in df.iterrows():
        if row['lat'] < 31:
            df.drop(index, inplace=True)
        elif row['lat'] >=37.5:
            latgrad = 1
        elif 37.5 > row['lat'] >=35.4:
            latgrad = 2
        elif 35.4 > row['lat'] >=33.9:
            latgrad = 3
        else: latgrad = 4
        
        lat_gradients.append(latgrad)

df["lat_gradient"] = lat_gradients

months = []
days = []
seasons = []

summer= [7,8,9]
winter = [1,2,3]
transition = [4,5,6,10,11,12]

for value in df["sight_date"]:
    
    month = datetime.date(value).month
    day = datetime.date(value).day
    months.append(month)
    days.append(day)
    
    if month in summer:   
        s = 'S'
    elif month in winter:
        s ='W'
    else: s = 'T'
    
    seasons.append(s)
 
df['month'] = months 
df['day'] = days  
df['season'] =seasons
df['year'] = 1901 ## assigning a standard year to all sightings, since ifnoring year in the analysis
#df.loc[df['month'] == 12, 'year'] = 1900
df['date'] = df["day"].astype(str) + " " + df["month"].astype(str) + " " + df["year"].astype(str)
df['date']= pd.to_datetime(df['date'], format='%d %m %Y', errors= 'coerce')


all_dolphins = list(df['dolphin_id'].unique())

wcdf = df.copy()

wcdf = wcdf.sort_values(['dolphin_id','month', 'day'],
              ascending = [True,True, True])
wcdf['state_delta'] = wcdf.groupby('dolphin_id')['lat_gradient'].diff() 
wcdf['state_delta'] = wcdf['state_delta'].fillna(0)
wcdf['state_delta'] = np.abs(wcdf['state_delta'])

U = []

#if dolphin seen in non consectutive patches (e.g. seen in patch 1, then next sighting in patch 3)
#we simulate a sighitng in the patch between between the sighting dates of the non consectutive patch sightings

for dolphin in all_dolphins:
    data = wcdf.loc[wcdf['dolphin_id'] == dolphin]
    state1 = data['lat_gradient'].iloc[0]
    date1 = data['date'].iloc[0]
    u = len(data)
    
    for index, row in data.iterrows():
        state_change = row['state_delta']
        state2 = row['lat_gradient']
        date2 = row['date']
        if state_change == 2:
           # wcdf= wcdf.append(row)
            wcdf = pd.concat([wcdf, pd.DataFrame([row])])
            wcdf=wcdf.reset_index()
            wcdf= wcdf.drop('index', axis=1)
            state = round(np.mean([state1, state2]))
            new_date = date1 + (date2 - date1) * random.random()
            wcdf.loc[wcdf.index[-1], 'date'] = new_date
            wcdf.loc[wcdf.index[-1], 'lat_gradient'] = state
            
            u = u+1
            
        elif state_change == 3:
           # wcdf= wcdf.append(row)
            wcdf = pd.concat([wcdf, pd.DataFrame([row])])
            wcdf=wcdf.reset_index()
            wcdf= wcdf.drop('index', axis=1)
            first_state = round(np.mean([state1, state2-1]))
            first_new_date = date1 + (date2 - date1) * random.random()
            wcdf.loc[wcdf.index[-1], 'date'] = first_new_date
            wcdf.loc[wcdf.index[-1], 'lat_gradient'] = first_state
            
           # wcdf= wcdf.append(row)
            wcdf = pd.concat([wcdf, pd.DataFrame([row])])
            wcdf=wcdf.reset_index()
            wcdf= wcdf.drop('index', axis=1)
            second_state = round(np.mean([state1+1, state2]))
            second_new_date = first_new_date + (date2 - first_new_date) * random.random()
            wcdf.loc[wcdf.index[-1], 'date'] = second_new_date
            wcdf.loc[wcdf.index[-1], 'lat_gradient'] = second_state
            
            u = u+2
            
            
        
        state1 = state2
        date1 = date2
    U.append(u)
        
wcdf = wcdf.sort_values(['dolphin_id','date'],
              ascending = [True,True])            
            
# get the time between sightings (delta) and the state (patch) change (state delta)            
wcdf['delta'] = wcdf.groupby('dolphin_id')['date'].diff()
wcdf['delta'] = wcdf['delta'].fillna(wcdf['date']- min(wcdf['date']))
wcdf['delta'] = wcdf['delta'] /np.timedelta64(1, 'D')
wcdf['delta'] = wcdf['delta'].replace(0,0.5)   
wcdf['state_delta'] = wcdf.groupby('dolphin_id')['lat_gradient'].diff()
wcdf['state_delta'] = wcdf['state_delta'].fillna(0)
wcdf['state_delta'] = np.abs(wcdf['state_delta'])

################################ ASSIGNING COASTAL ESTUARINE STOCKS TO INDIVIDUALS ################################

Coastal_dolphins = [] # MOVE INTO TWO OR MORE PATCHES
Estuarine_dolphins = [] #STAY IN THE SAME PATCH OR MOVE INTO ONE PATCH MAX
Est_dont_move = [] #STAY IN THE SAME PATCH
Est_that_move =[] #MOVE INTO ONE PATCH MAX

for d in all_dolphins:
    df = wcdf.loc[wcdf["dolphin_id"] == d]
    nps = len(df['lat_gradient'].unique())
    #print(nps)
    if nps > 2:
        Coastal_dolphins.append(d)
    else:
        Estuarine_dolphins.append(d)
        if nps == 1:
            Est_dont_move.append(d)
        else: Est_that_move.append(d)
            

stocks_i = []        
for index, row in wcdf.iterrows():
    dolphin = row["dolphin_id"]
    if dolphin in Coastal_dolphins:
        stocks_i.append("C")
    else:
        stocks_i.append("E")

dolphins_that_move = Coastal_dolphins + Est_that_move

wcdf["Stock_ind"] = stocks_i
#wcdf.to_csv("final_cleaned_data4patches_with_stocks.csv")
dfC = wcdf.loc[wcdf['Stock_ind'] == 'C']
#dfC.to_csv("final_cleaned_data4patch_Coastal.csv")

estuarinedf = wcdf.loc[wcdf["Stock_ind"] == 'E']
#estuarinedf.to_csv("final_cleaned_data4patch_with_stocks_Estonly.csv")

dfEM = estuarinedf.copy()

for index, row in dfEM.iterrows():
    dolphin = row['dolphin_id']
    if dolphin not in dolphins_that_move:
        dfEM.drop(index, inplace = True)

#dfEM.to_csv("final_cleaned_data4patch_with_stocks_Estmovers.csv")

############### NOW GET DATA INTO FORMAT FOR MSCR MODELING ############################# 

df_list = [dfEM, dfC]

strings = ["Estmovers", "Coastals"]

i = 0

for df in df_list:
    
    dolphins = list(df['dolphin_id'].unique())
    
    U = []
    
    for d in dolphins:
        data = df.loc[df['dolphin_id'] == d]
        num_obs = len(data)
        if num_obs < 250:
            u = len(data)
            #if u <250:
            U.append(u)
            
    
    print("The max number of obs (U) is: ", max(U))
    
    delta_rows = []
    state_rows = []
    end_of_study = datetime(1904, 12, 31, 0, 0, 0)
    
    
    for d in dolphins:
        data = df.loc[df['dolphin_id'] == d]
        num_obs = len(data)
        if num_obs < 250:
            dates = data['sight_date'].to_list()
            last_sighting = dates[-1]
            last_sighting_fix = last_sighting.replace(year=1904) 
            final_d = (end_of_study-last_sighting_fix).days
            if final_d ==0:
                final_d = 0.5
            
            
            delta = data['delta'].tolist()
            delta.append(final_d)
            add_zeros = max(U)- num_obs
            zeros = [0] * add_zeros
            final_delta = delta+zeros
            final_delta = [0.5 if pd.isna(x) else x for x in final_delta]
            delta_rows.append(final_delta)
            
            state = data['lat_gradient'].tolist()
            add_states = max(U) - num_obs
            last_state = state[-1:]
            new_states = last_state * add_states
            final_state = state+new_states
            state_rows.append(final_state)
            
    
    with open('delta4_'+strings[i]+'.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(delta_rows) 
        
    with open('state4_'+strings[i]+'.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(state_rows) 
        
    U_df = pd.DataFrame(U)
    
    U_df.to_csv("U4_" +strings[i]+".csv")
    
    i = i+1
    
        
        
    # Filter only Estuarine dolphins (E)
e_df = wcdf[wcdf['Stock_ind'] == 'E']

# Get a dictionary of all patches visited by each E dolphin
dolphin_patch_map = e_df.groupby('dolphin_id')['lat_gradient'].apply(set).to_dict()

# Initialize result dictionary
patch_proportions = {}

# Loop through patches 1 to 4
for patch in sorted(e_df['lat_gradient'].unique()):
    # All E dolphins seen in this patch
    seen_in_patch = e_df[e_df['lat_gradient'] == patch]['dolphin_id'].unique()
    
    # Of those, how many were also seen in at least one other patch
    also_seen_elsewhere = [d for d in seen_in_patch if len(dolphin_patch_map[d]) > 1]
    
    # Proportion calculation
    proportion = len(also_seen_elsewhere) / len(seen_in_patch) if len(seen_in_patch) > 0 else 0
    
    patch_proportions[patch] = {
        'total_E_seen_in_patch': len(seen_in_patch),
        'E_seen_in_patch_and_elsewhere': len(also_seen_elsewhere),
        'proportion': proportion
    }

# Print results
for patch, result in patch_proportions.items():
    print(f"Patch {patch}:")
    print(f"  Total E dolphins seen: {result['total_E_seen_in_patch']}")
    print(f"  E dolphins also seen elsewhere: {result['E_seen_in_patch_and_elsewhere']}")
    print(f"  Proportion: {result['proportion']:.2f}")
    print()    
    







    
    