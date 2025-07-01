#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 12:57:09 2024

"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statannot import add_stat_annotation
import os
from scipy.stats import tukey_hsd

def calc_euclidean(actual, predic):
    return np.sqrt(np.sum((actual - predic) ** 2))

def calc_correlation(actual, predic):
    a_diff = actual - np.mean(actual)
    p_diff = predic - np.mean(predic)
    numerator = np.sum(a_diff * p_diff)
    denominator = np.sqrt(np.sum(a_diff ** 2)) * np.sqrt(np.sum(p_diff ** 2))
    if denominator == 0:
        denominator = 0.00001
    return numerator / denominator

strandings = pd.read_csv('Normalized_Weekly_Infections_By_Patch2013.csv')

models = []

directory = os.getcwd()

labels =[]
for filename in os.listdir(directory):
    if filename.startswith("SS_for_CI"):
        df = pd.read_csv(filename)
        filename = filename.replace('SS_for_CI_', "")
        filename = filename.replace('.csv','')
        labels.append(filename.replace('SS_for_CI_', ""))
        models.append(df)
    
models_reformat = []

for df in models:
    sims = list(df['Simulation'].unique())
    zone_reformats = []
    for sim in sims:
        sim_data = df.loc[df['Simulation'] == sim]
        z1 = sim_data.iloc[0].tolist()
        z1 = z1[37:117]
        z2 = sim_data.iloc[1].tolist()
        z2 = z2[37:117]
        z3 = sim_data.iloc[2].tolist()
        z3 = z3[37:117]
        z4 = sim_data.iloc[3].tolist()
        z4 = z4[37:117]
        
        rdf = pd.DataFrame({'Zone1': z1, 'Zone2': z2, 'Zone3': z3, 'Zone4': z4})
        zone_reformats.append(rdf)
    models_reformat.append(zone_reformats)

        
CI_rows = []
SSE_rows = []

i = 0
for sims in models_reformat:

    for df in sims:
        
        predicted1 = df['Zone1']
        predicted2 = df['Zone2']
        predicted3 = df['Zone3']
        predicted4 = df['Zone4']
        
        actual1 = strandings['patch_1']
        actual2 = strandings['patch_2']
        actual3 = strandings['patch_3']
        actual4 = strandings['patch_4']
    
        sse1 = calc_euclidean(actual1, predicted1)
        sse2 = calc_euclidean(actual2, predicted2)
        sse3 = calc_euclidean(actual3, predicted3)
        sse4 = calc_euclidean(actual4, predicted4)
        
        cor1 = calc_correlation(actual1, predicted1)
        cor2 = calc_correlation(actual2, predicted2)
        cor3 = calc_correlation(actual3, predicted3)
        cor4 = calc_correlation(actual4, predicted4)
        
        
        
        totalsse = sse1+sse2+sse3+sse4
        total = np.mean([cor1,cor2,cor3,cor4])
    
        row = [labels[i], cor1, cor2, cor3, cor4, total]
        CI_rows.append(row)
        
        sserow = [labels[i], sse1, sse2, sse3, sse4, totalsse]
        SSE_rows.append(sserow)
        

    i = i +1

Corr_DF_CI = pd.DataFrame(CI_rows, columns = ['Model', 'Zone1', 'Zone2', 'Zone3', 'Zone4', "Total"])
sseDF_CI = pd.DataFrame(SSE_rows, columns = ['Model', 'Zone1', 'Zone2', 'Zone3', 'Zone4', "Total"])
sseDF_CI.to_csv('2013SSE_Data_scenarios.csv') 
Corr_DF_CI.to_csv('2013r_Data_scenarios.csv') 


datasets = [Corr_DF_CI, sseDF_CI]
string_label = ["r", "SSE"]

q = 0
for d in datasets:
    final_CI_rows = []     
    for_stats = [] 
    r = 0
    for label in labels:
        
        df = d.loc[d['Model'] == label]
        total = df['Total'].tolist()
        for_stats.append(total)
        t_mean = round(np.mean(total),3)
        t_min = round(min(df['Total']),3)
        t_max = round(max(df['Total']),3)
        t_sd = round(np.std(df['Total']), 3)
        
        z1_mean = round(np.mean(df['Zone1']),3)
        z1_min = round(min(df['Zone1']),3)
        z1_max = round(max(df['Zone1']),3)
        z1_sd = round(np.std(df['Zone1']), 3)
        
        z2_mean = round(np.mean(df['Zone2']),3)
        z2_min = round(min(df['Zone2']),3)
        z2_max = round(max(df['Zone2']),3)
        z2_sd = round(np.std(df['Zone2']), 3)
        
        z3_mean = round(np.mean(df['Zone3']),3)
        z3_min = round(min(df['Zone3']),3)
        z3_max = round(max(df['Zone3']),3)
        z3_sd = round(np.std(df['Zone3']), 3)
        
        z4_mean = round(np.mean(df['Zone4']),3)
        z4_min = round(min(df['Zone4']),3)
        z4_max = round(max(df['Zone4']),3)
        z4_sd = round(np.std(df['Zone4']), 3)
        
        row = [label, t_mean, t_min, t_max, t_sd, z1_mean, z1_min, z1_max,z1_sd, z2_mean, z2_min, z2_max, z2_sd,
               z3_mean, z3_min, z3_max, z3_sd, z4_mean, z4_min, z4_max, z4_sd]
        final_CI_rows.append(row)
        r = r+1
        
    final_CI_SS_data = pd.DataFrame(final_CI_rows, columns = ["Model", "Total SS", "Min SS", "Max SS", "SD SS",
                                                     "Z1SS", "Z1Min", "Z1Max", "Z1SD",
                                                     "Z2SS", "Z2Min", "Z2Max","Z2SD",
                                                     "Z3SS", "Z3Min", "Z3Max","Z3SD",
                                                     "Z4SS", "Z4Min", "Z4Max","Z4SD"])
        
        
    
    final_CI_SS_data.to_csv("Scenarios2013_" +string_label[q]+".csv")  
    q = q+1
    
  
      
    
tests = []

directory = os.getcwd()
labels =[]
for filename in os.listdir(directory):
    if filename.startswith("Average_forSSE_"):
        df = pd.read_csv(filename)
        filename = filename.replace('Average_forSSE_,', "")
        filename = filename.replace('.csv','')
        labels.append(filename.replace('Average_forSSE_', ""))
        tests.append(df)
       
tests_reformat = []

for df in tests:
    
   # new = df.iloc[40:]
    final = df.iloc[37:117]
    #final['week'] = list(range(0,98))
    final['week'] = list(range(0,80))
    tests_reformat.append(final)
    final.to_csv('test.csv')
    
   
rows = []

i = 0
for df in tests_reformat:
    
    
    fig, ax1 = plt.subplots()
    #ax1.set_xlabel('Week')
    ax1.set_ylabel('New Infections Standardized', fontsize = 15)
    ax1.set_ylim(0,1)
   # week_labels = ["1-Mar-13","10-May-13", "19-Jul-13", "27-Sep-13", "6-Dec-13", "14-Feb-14", "23-Apr-14", "25-Jun-14", "3-Sep-14", "12-Nov-14"]
    week_labels = ["Mar","May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jun", "Sep", "Nov"]
    ax1.set_xticks(np.arange(0, 100, step=10),labels=week_labels, rotation = 45, size= 14)
    ax1.set_title(labels[i], fontsize = 20)
    plt.yticks(fontsize = 13)

    #ax1.plot(strandings['week'], strandings['Zone1'], color = '#fbb4b9',  label = 'Zone 1 Stranding Data')
    #ax1.plot(strandings['week'], strandings['Zone2'], color = '#f768a1', label = 'Zone 2 Stranding Data' )
    #ax1.plot(strandings['week'], strandings['Zone3'], color = '#c51b8a', label = 'Zone 3 Stranding Data')
    #ax1.plot(strandings['week'], strandings['Zone4'], color = '#7a0177',  label = 'Zone 4 Stranding Data')
    
    ax1.plot(df['week'], df['Zone1'], color = '#fbb4b9',  label = 'Patch 1')
    ax1.plot(df['week'], df['Zone2'], color = '#f768a1',  label = 'Patch 2')
    ax1.plot(df['week'], df['Zone3'], color = '#c51b8a',  label = 'Patch 3')
    ax1.plot(df['week'], df['Zone4'], color = '#7a0177', label = 'Patch 4')
    
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.85))
    plt.savefig("Figures/" + labels[i] +"Scenario_Infection_Plot_Standardized.jpg", dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    i = i+1
