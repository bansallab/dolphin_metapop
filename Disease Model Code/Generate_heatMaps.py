#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:28:36 2024

"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("All_Data_epidemic_risk_and_survel.csv")

zones = [1, 2, 3, 4]
months = ['Jan', "Feb", 'Mar', "Apr",'Model', "May", "Jun", "Jul", 'Aug', "Sep", "Oct", "Nov", "Dec"]

prob_rows = []
size_rows = []
prob_comb_rows = []
error_rows = []

for zone in zones:
    dz = df.loc[df['Epidemic_Start_Zone'] == zone]
    for month in months:
        dm = dz.loc[dz['Epidemic_Start_Month'] == month]
        epi_prob = round(dm["EpiProb"].iloc[0], 2)
        epi_size = round(dm["FullEpiSize"].iloc[0], 2)
        comb = round(epi_prob*epi_size,2)
        error1 = round(dm["ErrorZ1"].iloc[0], 2)
        error2 = round(dm["ErrorZ2"].iloc[0], 2)
        error3 = round(dm["ErrorZ3"].iloc[0], 2)
        error4 = round(dm["ErrorZ4"].iloc[0], 2)
        if month == 'Model':
            if zone == 2:
                row = [zone, month, epi_prob]
                srow = [zone, month, epi_size]
                crow = [zone, month, comb]
                erow = [zone, month, error1, error2, error3, error4]
            else:
                row = [zone, month, ]
                srow = [zone, month, ]
                crow = [zone, month, ]
                erow = [zone, month, ]
        else:
            row = [zone, month, epi_prob]
            srow = [zone, month, epi_size]
            crow = [zone, month, comb]
            erow = [zone, month, error1, error2, error3, error4]
        prob_comb_rows.append(crow)
        size_rows.append(srow)
        prob_rows.append(row)
        error_rows.append(erow)

column_names = ['Start Patch', 'Start Month', 'Epidemic Probability']
epi_prob_data = pd.DataFrame(prob_rows, columns= column_names)

column_names = ['Start Patch', 'Start Month', 'Epidemic Size']
epi_size_data = pd.DataFrame(size_rows, columns= column_names)

column_names = ['Start Patch', 'Start Month', 'Epidemic Probability * Size']
epi_probcomb_data = pd.DataFrame(prob_comb_rows, columns= column_names)

column_names_err = ['Start Patch', 'Start Month', 'Error 1', 'Error 2', 'Error 3', 'Error 4']
full_error_data = pd.DataFrame(error_rows, columns= column_names_err)



ep_result = epi_prob_data.pivot(index='Start Month',columns='Start Patch',values='Epidemic Probability')
ep_result = ep_result.reindex(months)
epiprob = ep_result.to_numpy()
print(ep_result)

# Define the plot
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "Probability of an Epidemic"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=25)
ttl = ax.title
ttl.set_position([0.5,1.05])
plt.ylabel("Start Month",fontsize =20)
plt.xlabel("Start Patch", fontsize =20)
plt.yticks(rotation=0, fontsize = 20) 
plt.xticks(fontsize = 20) 

sns.heatmap(ep_result,annot=epiprob,annot_kws={"size": 20},fmt="",cmap='Reds',linewidths=0.30,ax=ax, cbar = False)


# Display the Heatmap

plt.savefig("HeatMaps/Epi_Prob-HeatMAP.jpg", dpi = 300, bbox_inches = 'tight')
plt.show()
plt.close()

##################################################################################

es_result = epi_size_data.pivot(index='Start Month',columns='Start Patch',values='Epidemic Size')
es_result = es_result.reindex(months)
episize = es_result.to_numpy()

# Define the plot
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "Size of an Epidemic"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=25)
ttl = ax.title
ttl.set_position([0.5,1.05])
plt.ylabel("Start Month",fontsize =20)
plt.xlabel("Start Patch", fontsize =20)
plt.yticks(rotation=0, fontsize = 20) 
plt.xticks(fontsize = 20) 
sns.heatmap(es_result,annot=episize,annot_kws={"size": 20}, fmt="",cmap='Reds',linewidths=0.30,ax=ax, cbar = False)

# Display the Heatmap

plt.savefig("HeatMaps/Epi_Size-HeatMAP.jpg", dpi = 300, bbox_inches = 'tight')
plt.show()
plt.close()


##########################################################################################
comb_result = epi_probcomb_data.pivot(index='Start Month',columns='Start Patch',values='Epidemic Probability * Size')
comb_result = comb_result.reindex(months)
epicomb = comb_result.to_numpy()

# Define the plot
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "Epidemic Risk"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=25)
ttl = ax.title
ttl.set_position([0.5,1.05])
plt.ylabel("Start Month",fontsize =20)
plt.xlabel("Start Patch", fontsize =20)
plt.yticks(rotation=0, fontsize = 20) 
plt.xticks(fontsize = 20) 
sns.heatmap(comb_result,annot=epicomb,annot_kws={"size": 25, 'weight':'bold'},fmt="",cmap='Reds',linewidths=0.30,ax=ax, cbar = False)

# Display the Heatmap
plt.savefig("HeatMaps/Epi_Comb-HeatMAP.jpg", dpi = 300, bbox_inches = 'tight')
plt.show()
plt.close()

###################

r_df = pd.read_csv('2013r_epidemicRisk_scenarios.csv')
patches = ['Patch 1', 'Patch 2', 'Patch 3', 'Patch 4']
start_patch_r = [[],[],[],[]]
models = list(r_df['Model'].unique())

for m in months:
    i = 0
    for p in patches:
        for model in models:
            if model == 'Start '+m+" "+p:
                data = r_df.loc[r_df['Model'] == model]
                total = round(np.mean(data['Total']),2)
                start_patch_r[i].append(total)
        i = i +1

r = pd.DataFrame(list(zip(start_patch_r[0], start_patch_r[1], start_patch_r[2], start_patch_r[3])), columns = ['1', '2', '3', '4']) 
r.index=  months
rvals = r.to_numpy()
# Define the plot
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "2013 r values"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=25)
ttl = ax.title
ttl.set_position([0.5,1.05])

plt.yticks( rotation=0, fontsize = 20) 
plt.xticks(fontsize = 20) 
sns.heatmap(r,annot=rvals,annot_kws={"size": 25, 'weight':'bold'},fmt="",cmap='Blues',linewidths=0.30,ax=ax, cbar = False)
ax.set_ylabel("Start Month",fontsize =20)
ax.set_xlabel("Start Patch", fontsize =20)
# Display the Pharma Sector Heatmap
plt.savefig("HeatMaps/r-HeatMAP.jpg", dpi = 300, bbox_inches = 'tight')
plt.show()
plt.close()

###################

SSE_df = pd.read_csv('2013SSE_EpidemicRisk_scenarios.csv')
patches = ['Patch 1', 'Patch 2', 'Patch 3', 'Patch 4']
start_patch_SSE = [[],[],[],[]]
models = list(SSE_df['Model'].unique())

for m in months:
    i = 0
    for p in patches:
        for model in models:
            if model == 'Start '+m+" "+p:
                data = SSE_df.loc[SSE_df['Model'] == model]
                total = round(np.mean(data['Total']),2)
                start_patch_SSE[i].append(total)
        i = i +1

SSE = pd.DataFrame(list(zip(start_patch_SSE[0], start_patch_SSE[1], start_patch_SSE[2], start_patch_SSE[3])), columns = ['1', '2', '3', '4']) 
SSE.index=  months
SSEvals = SSE.to_numpy()
# Define the plot
fig, ax = plt.subplots(figsize=(13,7))

# Add title to the Heat map
title = "2013 SSE values"

# Set the font size and the distance of the title from the plot
plt.title(title,fontsize=25)
ttl = ax.title
ttl.set_position([0.5,1.05])

plt.yticks( rotation=0, fontsize = 20) 
plt.xticks(fontsize = 20) 
sns.heatmap(SSE,annot=SSEvals,annot_kws={"size": 20,'weight':'bold'},fmt="",cmap='Blues',linewidths=0.30,ax=ax, cbar = False)
ax.set_ylabel("Start Month",fontsize =20)
ax.set_xlabel("Start Patch", fontsize =20)
# Display the Pharma Sector Heatmap
plt.savefig("HeatMaps/SSE-HeatMAP.jpg", dpi = 300, bbox_inches = 'tight')
plt.show()
plt.close()




########################################################

err2 = full_error_data[["Start Patch","Start Month","Error 2"]]
err3 = full_error_data[["Start Patch","Start Month","Error 3"]]
err4 = full_error_data[["Start Patch","Start Month","Error 4"]]

err_dataframes = [err2, err3, err4]
i = 2
for ed in err_dataframes:
    error_col = ed.columns[2]
    result = ed.pivot(index='Start Month',columns='Start Patch',values=error_col)
    result = result.reindex(months)
    error = np.round(result.to_numpy(),2)

    # Define the plot
    fig, ax = plt.subplots(figsize=(13,7))

    # Add title to the Heat map
    title = "Error for Patch " + str(i)

    # Set the font size and the distance of the title from the plot
    plt.title(title,fontsize=25)
    ttl = ax.title
    ttl.set_position([0.5,1.05])
    plt.ylabel("Start Month",fontsize =20)
    plt.xlabel("Start Pactch", fontsize =20)
    plt.yticks(rotation=0, fontsize = 20) 
    plt.xticks(fontsize = 20) 

    sns.heatmap(result,annot=error,annot_kws={"size": 25, 'weight':'bold'},fmt="",cmap='PiYG',linewidths=0.30,ax=ax, vmin=-0.4, vmax=0.4, cbar = False)

    # Display the Pharma Sector Heatmap
    
    plt.savefig("HeatMaps/Erorr_HeatmAP_Zone"+str(i)+".jpg", dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    i = i+1


sp1err2 = err2.loc[err2['Start Patch'] == 1]
sp1err3 = err3.loc[err2['Start Patch'] == 1]
sp1err4 = err4.loc[err2['Start Patch'] == 1]

sp1_dfs = []



        
        