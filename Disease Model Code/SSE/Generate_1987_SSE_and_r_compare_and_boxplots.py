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

strandings = pd.read_csv('Normalized_Weekly_Infections_By_Patch1987.csv')

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
    j = 1
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
        
        if j == 2:
            fig, ax1 = plt.subplots()
            #ax1.set_xlabel('Week')
            ax1.set_ylabel('New Infections Standardized', fontsize = 15)
            ax1.set_ylim(0,1)
           # week_labels = ["1-Mar-13","10-May-13", "19-Jul-13", "27-Sep-13", "6-Dec-13", "14-Feb-14", "23-Apr-14", "25-Jun-14", "3-Sep-14", "12-Nov-14"]
            week_labels = ["Mar","May", "Jul", "Oct", "Dec", "Feb", "Apr"]
            ax1.set_xticks(np.arange(0, 70, step=10),labels=week_labels, rotation = 45, size= 14)
            ax1.set_title(labels[i], fontsize = 20)
            plt.yticks(fontsize = 13)
    
            ax1.plot(strandings['week'], actual1, color = 'black', alpha = 0.25, label = 'Zone 1 Stranding Data')
            ax1.plot(strandings['week'], actual2, color = 'black', alpha = 0.5,label = 'Zone 2 Stranding Data' )
            ax1.plot(strandings['week'], actual3, color = 'black', alpha = 0.75, label = 'Zone 3 Stranding Data')
            ax1.plot(strandings['week'], actual4, color = 'black', alpha = 1, label = 'Zone 4 Stranding Data')
            
            ax1.plot(strandings['week'], predicted1, color = 'blue', alpha = 0.25, label = 'Zone 1 Model Results')
            ax1.plot(strandings['week'], predicted2, color = 'blue', alpha = 0.5, label = 'Zone 2 Model Results')
            ax1.plot(strandings['week'], predicted3, color = 'blue', alpha = 0.75, label = 'Zone 3 Model Results')
            ax1.plot(strandings['week'], predicted4, color = 'blue', alpha = 1, label = 'Zone 4 Model Results')
            
           # fig.legend(loc='center right')
    
    
         #   plt.savefig("Time_Series/SS_fit" +str(labels[i])+".jpg", dpi = 300, bbox_inches = 'tight')
            plt.show()
            plt.close()
        j = j +1

    i = i +1




## look at both r and SSE for all model comparisons
Corr_DF_CI = pd.DataFrame(CI_rows, columns = ['Model', 'Zone1', 'Zone2', 'Zone3', 'Zone4', "Total"])

sseDF_CI = pd.DataFrame(SSE_rows, columns = ['Model', 'Zone1', 'Zone2', 'Zone3', 'Zone4', "Total"])


start_time_data = ['start_p1_May1-10','start_p1_May11-20','start_p1_May21-31',
              'start_p2_May1-10','start_p2_May11-20','start_p2_May21-31',
              'start_p1_June1-10','start_p1_June11-20','start_p1_June21-31',
              'start_p2_June1-10','start_p2_June11-20','start_p2_June21-31']

null_data = ['Null1', 'Null2', 'Null3', 'SocBeh',]

dynamic_data = ['Control', 'Environ', 'SocBeh']

r_start_time = Corr_DF_CI[Corr_DF_CI["Model"].isin(start_time_data)]
r_null = Corr_DF_CI[Corr_DF_CI["Model"].isin(null_data)]
r_dynamic = Corr_DF_CI[Corr_DF_CI["Model"].isin(dynamic_data)]

s_start_time = sseDF_CI[sseDF_CI["Model"].isin(start_time_data)]
s_null = sseDF_CI[sseDF_CI["Model"].isin(null_data)]
s_dynamic = sseDF_CI[sseDF_CI["Model"].isin(dynamic_data)]

dataset_labels = [start_time_data, null_data, dynamic_data, start_time_data, null_data, dynamic_data]
datasets = [r_start_time, r_null, r_dynamic, s_start_time, s_null, s_dynamic]
string_labels = ['StartTimes_r', 'Nulls_r', "Dynamic_r", 'StartTimes_SSE', 'Nulls_SSE', "Dynamic_SSE"]

r = 0
for d in datasets:
    final_CI_rows = []     
    for_stats = [] 
    figure_labels = []
    for label in dataset_labels[r]:
        
        df = d.loc[d['Model'] == label]
        total = df['Total'].tolist()
        for_stats.append(total)
        t_mean = round(np.mean(total),3)
        t_min = round(min(total),3)
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
        
    final_CI_SS_data = pd.DataFrame(final_CI_rows, columns = ["Model", "Total SS", "Min SS", "Max SS", "SD SS",
                                                     "Z1SS", "Z1Min", "Z1Max", "Z1SD",
                                                     "Z2SS", "Z2Min", "Z2Max","Z2SD",
                                                     "Z3SS", "Z3Min", "Z3Max","Z3SD",
                                                     "Z4SS", "Z4Min", "Z4Max","Z4SD"])
        
        
    
    final_CI_SS_data.to_csv("SS_for_all_models1987" +string_labels[r]+".csv")  

            

    fig, ax = plt.subplots(1, 1,)
    ax.boxplot(for_stats, showfliers = False, medianprops = dict(color = "black", linewidth = 1.5)) 
    ax.yaxis.set_tick_params(labelsize=15)
    ax.set_xticklabels(dataset_labels[r], rotation = 45, fontsize=10) 

    
    if r in range(0,3):
        ax.set_ylabel("1987 r", fontsize =25) 
        ax.set_ylim([-0.2,1])
    else:
        ax.set_ylabel("1987 SSE", fontsize =25) 
        ax.set_ylim([0,10])
    
    plt.savefig("FULL_boxplot1987" + string_labels[r]+ ".jpg", dpi = 300, bbox_inches= 'tight')
    plt.show()
    plt.close()
    
    if r == 0 or r==3:
        res = tukey_hsd(for_stats[0],for_stats[1],for_stats[2],for_stats[3], for_stats[4], for_stats[5],for_stats[6],
                        for_stats[7],for_stats[8],for_stats[9],for_stats[10],for_stats[11])
        print(res)
        
        averages = [for_stats[0],for_stats[1],for_stats[2],for_stats[3], for_stats[4], for_stats[5],for_stats[6],
                        for_stats[7],for_stats[8],for_stats[9],for_stats[10],for_stats[11]]
        for a in averages:
            mean = np.mean(a)
            print(mean)
       
    elif r ==1 or r ==4:
        res = tukey_hsd(for_stats[0],for_stats[1],for_stats[2],for_stats[3])
        print(res)
        
        averages = [for_stats[0],for_stats[1],for_stats[2],for_stats[3]]
        for a in averages:
            mean = np.mean(a)
            print(mean)
        
    elif r == 2 or r == 5:
        res = tukey_hsd(for_stats[0],for_stats[1],for_stats[2])
        print(res)
        
        averages = [for_stats[0],for_stats[1],for_stats[2]]
        for a in averages:
            mean = np.mean(a)
            print(mean)
    r = r+1






