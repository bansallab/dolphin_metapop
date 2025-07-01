#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:20:29 2024

@author: melissacollier
"""

import Simulation_Functions_final as simf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Set parameters ############


T = 1094

day_range = range(0, T)
week_range = range(0,157)
### tau from R0 (1.8) * mu (1/8.3) / average population degree (10)
R0 = 1.8

#### Infectious period range from Morris et al ######
mu_list = [7,8,9,10]

#### patches = zones ###
patches = [0,1,2,3]

### alpha distribution from clustering and survey results
#alpha_list = [0.07, 0.08, 0.09, 0.1, 0.11]
alpha_list = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06]

max_move_coast1 = [9000, 14000, 5000, 0] #100% of individuals moving but controlling for movements of southern and northern
max_move_coast2 = [0, 9000, 14000, 5000]

max_move_est1 = [999, 999, 999, 0] #100% of individuals moving but controlling for movements of different estuarine stocks
max_move_est2 = [0, 999, 999, 999]

migratory1 = list(range(92,184)) + list(range(457,549)) +list(range(822,914)) #Oct-dec
migratory2 = list(range(275,365)) + list(range(639, 730)) + list(range(1004,1095)) #Apr-June

mig1e = list(range(92,213)) + list(range(396,578)) +list(range(761,943))
mig2e = list(range(213,396)) + list(range(578, 761)) + list(range(943,1126))

start_coastal_size = [10000, 10000, 2000, 4000] 
start_est_size = [1000,1000,1000,1000]

coastal_etas_1 = [0.02, 0.05, 0.4, 0]
coastal_etas_2 = [0, 0.02, 0.05, 0.4]
coastal_etas_1_std = [0.01, 0.01, 0.2, 0]     
coastal_etas_2_std = [0, 0.01, 0.01, 0.2]   

est_etas_1 = [0.04, 0.02, 0.01, 0]  
est_etas_2 = [0, 0.04, 0.02, 0.01 ]
est_etas_1_std = [0, 0.002, 0.0014, 0.002] 
est_etas_2_std = [0.002, 0.0014, 0.002, 0]   

change_time = list(range(289, 371)) + list(range(651, 736))
reduction = 0.8
coastal_deg_mean = 8
coastal_deg_std = 0
est_deg_std = 0
est_deg_mean = 6

num_sims = 100


###### Parameters that change depending on the model being run #####
start_time = [list(range(184,215)),list(range(215,243)), list(range(243,274)), list(range(274, 304)),
                      list(range(304,315)), list(range(315,335)), list(range(335,365)), list(range(365,396)), list(range(396,427)), 
                      list(range(427,457)), list(range(457,488)), list(range(488,518)), list(range(518,549))]

#start_time = [list(range(304,315))]


start_patch  = [[1,0,0,0],[0,1,0,0], [0,0,1,0], [0,0,0,1]]
#start_patch  = [[0,1,0,0]]

# start in each month and patch for epidemic risk scenarios
months = ['Jan', "Feb", 'Mar', "Apr", "Model", "May", "Jun", "Jul", 'Aug', "Sep", "Oct", "Nov", "Dec"]
Zones = [1, 2, 3, 4]

#months = ['Model']
#Zones = [2]


month_rows = []
patch_rows = []
err2_rows = []
err3_rows = []
err4_rows = []

frows = []
b = 0
for m in months:
    y = 0
    for p in Zones:
        
        model = 'Start '+ m + ' Patch '+ str(p)
    
    
        print(model)
    
        total_est = sum(start_est_size)
        total_coast = sum(start_coastal_size)
    
        total_size_m, epi_prob,avg_error1, avg_error2, avg_error3, avg_error4,All_I_full_epi_1, All_I_full_epi_2, All_I_full_epi_3, All_I_full_epi_4, All_RR_cum, All_RM_cum, All_N_full_epi_1,All_N_full_epi_2,All_N_full_epi_3,All_N_full_epi_4, incidence_coastline, zone1est_incidence, zone2est_incidence, zone3est_incidence, zone4est_incidence, all_err2, all_err3, all_err4= simf.metapop_model(R0, start_time[b], start_patch[y], migratory1, migratory2, coastal_etas_1, coastal_etas_1_std, coastal_etas_2, coastal_etas_2_std, 
                      est_etas_1, est_etas_1_std, est_etas_2, est_etas_2_std, change_time, max_move_coast1, max_move_coast2, max_move_est1, max_move_est2,
                      reduction, alpha_list, mu_list, T,coastal_deg_mean, coastal_deg_std, est_deg_mean, est_deg_std, patches,
                      start_est_size, start_coastal_size, num_sims,mig1e,mig2e)
        
        for i in range(0, len(all_err2)):
            month_rows.append(m)
            patch_rows.append(p)
            err2_rows.append(all_err2[i])
            err3_rows.append(all_err3[i])
            err4_rows.append(all_err4[i])
            
        
        frow = [m, p, epi_prob, total_size_m,  avg_error1, avg_error2, avg_error3, avg_error4]
        frows.append(frow)
        
        ### Get files for SSE calculation ####################
        SS_megalist = [All_I_full_epi_1, All_I_full_epi_2, All_I_full_epi_3, All_I_full_epi_4]
        rows = []
        z = 1
               
        
        for zone in SS_megalist:
            r = 0
            for sim in zone:
                max_infected = max(All_I_full_epi_1[r] + All_I_full_epi_2[r] + All_I_full_epi_3[r]+ All_I_full_epi_4[r])
                corrected_sim = [x/max_infected for x in sim]
                details = [z, r]
                row = details + corrected_sim
                rows.append(row)
                r = r+1
            z = z+1
        CIdf = pd.DataFrame(rows)
        CIdf = CIdf.rename(columns={0: 'Zone', 1: 'Simulation'}) 
        CIdf.to_csv('RiskAnalysisSSE/SS_for_CI_'+model+'.csv')
        
    
        mean_infected_1 = []      
        for w in week_range:
            infs = []
            for sim in All_I_full_epi_1:
                number = sim[w]
                infs.append(number)
            avg = round(np.mean(infs))
            mean_infected_1.append(avg)
      
    
        mean_infected_2 = []  
        for w in week_range:
            infs = []
            for sim in All_I_full_epi_2:
                number = sim[w]
                infs.append(number)
            avg = round(np.mean(infs))
            mean_infected_2.append(avg)
    
        mean_infected_3 = []  
        for w in week_range:
            infs = []
            for sim in All_I_full_epi_3:
                number = sim[w]
                infs.append(number)
            avg = round(np.mean(infs))
            mean_infected_3.append(avg)    

    
        mean_infected_4 = []  
        for w in week_range:
            infs = []
            for sim in All_I_full_epi_4:
                number = sim[w]
                infs.append(number)
            avg = round(np.mean(infs))
            mean_infected_4.append(avg)     

            
        ######## final SSE figure ############
        
        max_new = max(mean_infected_1+ mean_infected_2+ mean_infected_3+ mean_infected_4)
        Z1 = [x/max_new for x in mean_infected_1]
        Z2 = [x/max_new for x in mean_infected_2]
        Z3 = [x/max_new for x in mean_infected_3]
        Z4 = [x/max_new for x in mean_infected_4]
        average_zone_infections = [Z1, Z2, Z3, Z4]
    
        df = pd.DataFrame({'Zone1': Z1, 'Zone2': Z2, 'Zone3': Z3, 'Zone4': Z4})
        df.to_csv('RiskAnalysisSSE/Average_forSSE_' + model +'.csv')
        
        y = y +1
    b = b +1

column_names = ['Epidemic_Start_Month', 'Epidemic_Start_Zone', 'EpiProb','FullEpiSize', 'ErrorZ1', 'ErrorZ2', 'ErrorZ3','ErrorZ4']
Final_data = pd.DataFrame(frows, columns= column_names)
Final_data.to_csv("All_Data_epidemic_risk_and_survel.csv")


error_data = pd.DataFrame({'Month': month_rows, 'Patch': patch_rows, "Error2": err2_rows, "Error3": err3_rows, "Error4": err4_rows})
sub_errdf1 = error_data.loc[error_data['Patch'] == 1]
sub_errdf2 = error_data.loc[error_data['Patch'] == 2]
errdfs= [sub_errdf1, sub_errdf2]

titles = ["Start Patch 1","Start Patch 2"]

i = 0
for df in errdfs:
    mean_err_2 = []
    mean_err_3 = []
    mean_err_4 = []
    
    sd_err_2 = []
    sd_err_3 = []
    sd_err_4 = []
    

    for m in months:
        if m == 'Model':
            print("skip")
        else:
            d = df.loc[df['Month'] == m]
            e2 = np.mean(d['Error2'])
            e3 = np.mean(d['Error3'])
            e4 = np.mean(d['Error4'])
            mean_err_2.append(e2)
            mean_err_3.append(e3)
            mean_err_4.append(e4)
            
            sd_err_2.append(np.std(d['Error2']))
            sd_err_3.append(np.std(d['Error3']))
            sd_err_4.append(np.std(d['Error4']))
        
    new_months = ['Jan', "Feb", 'Mar', "Apr", "May", "Jun", "Jul", 'Aug', "Sep", "Oct", "Nov", "Dec"]    
     
    plt.plot(new_months,mean_err_2, color = '#f768a1', linewidth = 2, alpha = 1, label="Patch 2")
    plt.errorbar(new_months,mean_err_2, yerr = sd_err_2, marker = "o",capsize = 7, markersize = 7, color = '#f768a1')

    plt.plot( new_months,mean_err_3, color = '#c51b8a', linewidth = 2, alpha = 1, label="Patch 3")
    plt.errorbar( new_months,mean_err_3, yerr = sd_err_3, marker = "o", capsize = 7,markersize = 7, color = '#c51b8a')
    
    plt.plot( new_months,mean_err_4, color = '#7a0177', linewidth = 2, alpha = 1, label="Patch 4")
    plt.errorbar( new_months,mean_err_4, yerr = sd_err_4, marker = "o", capsize = 7,markersize = 7, color = '#7a0177')
    
    plt.yticks(size = 10)
    plt.xticks(size = 10, rotation = 45)
    plt.ylabel("Estuarine - Full Coastline Incidence", size = 12)
    plt.legend('')
    plt.xlabel("Start Month", size = 12 )
    plt.title(titles[i], size = 15)
    
    plt.savefig("Error_Plot"+titles[i]+".jpg", dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    i = i +1
    
 
    

"""
for i in range(0, len(error2)):
    plt.plot(week_range,error2[i], color = '#f768a1', alpha = 0.02)
    plt.plot(week_range,error3[i], color = '#c51b8a', alpha = 0.02)
    plt.plot(week_range,error4[i], color = '#7a0177', alpha = 0.02)
    
mean_error_2 = []      
for w in week_range:
    infs = []
    for sim in error2:
        number = sim[w]
        infs.append(number)
    avg = round(np.mean(infs),2)
    mean_error_2.append(avg)
plt.plot(week_range,mean_error_2, color = '#f768a1', linewidth = 2, alpha = 1, label="Estuarine Patch 2")

mean_error_3 = []      
for w in week_range:
    infs = []
    for sim in error3:
        number = sim[w]
        infs.append(number)
    avg = round(np.mean(infs),2)
    mean_error_3.append(avg)
plt.plot(week_range,mean_error_3, color = '#c51b8a', linewidth = 2, alpha = 1, label="Estuarine Patch 3")

mean_error_4 = []      
for w in week_range:
    infs = []
    for sim in error4:
        number = sim[w]
        infs.append(number)
    avg = round(np.mean(infs),2)
    mean_error_4.append(avg)
plt.plot(week_range,mean_error_4, color = '#7a0177', linewidth= 2, alpha = 1, label="Estuarine Patch 4")

plt.xlim(34, 124)
week_labels = ["Mar", "May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jul", "Sep"]
plt.xticks(np.arange(34, 124, step=10),labels=week_labels, rotation = 45, size= 14)
plt.yticks(size = 10)
plt.ylabel("Incidence Error", size = 15)
plt.legend(loc='lower left')

plt.savefig("Error_TimeSeries.jpg", dpi = 300, bbox_inches = 'tight')
plt.show()
plt.close()

 """




