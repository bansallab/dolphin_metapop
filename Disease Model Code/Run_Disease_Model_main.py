#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:20:29 2024

"""

import Simulation_Functions_final as simf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Set parameters ############


T = 1099 #number of days to run the simulation 

day_range = range(0, T)
week_range = range(0,T//7)

R0 = 1.8

#### Infectious period range from Morris et al ######
mu_list = [7,8,9,10]

#### list of patches (four patches) ###
patches = [0,1,2,3]

### alpha distribution from clustering and survey results (mixing between 0-6%)
alpha_list = [ 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06]

max_move_coast1 = [10000, 14000, 5000, 0] #100% of individuals moving but controlling for movement of different coastal stocks
max_move_coast2 = [0, 10000, 14000, 5000]

max_move_est1 = [999, 999, 500, 0] #100% of individuals moving but controlling for movements of different estuarine stocks
max_move_est2 = [0, 999, 999, 500]

migratory1 = list(range(92,184)) + list(range(457,549)) +list(range(822,914)) #Oct-dec days
migratory2 = list(range(275,365)) + list(range(639, 730)) + list(range(1004,1095)) #Apr-June days

mig1e = list(range(92,213)) + list(range(396,578)) +list(range(761,943)) #estuarine move south in the first half of the year, Jan-June
mig2e = list(range(213,396)) + list(range(578, 761)) + list(range(943,1126)) #estuarine move north in second half of the year July-Dec

start_coastal_size = [10000, 10000, 2000, 4000]  #the number of coastal dolphins in each patch initially
start_est_size = [1000,1000,1000,1000] #the number of estuarine dolphins in each patch initally


###### Parameters that change depending on the model being run #####
num_sims = 100

model_runs = ['start_p1_May1-10','start_p1_May11-20','start_p1_May21-31',
              'start_p2_May1-10','start_p2_May11-20','start_p2_May21-31',
              'start_p1_June1-10','start_p1_June11-20','start_p1_June21-31',
              'start_p2_June1-10','start_p2_June11-20','start_p2_June21-31',
              'Null1', 'Null2', 'Null3', 
              'Control', 'SocBeh', 'Environ']


## range of what day the infection starts 
start_time = [list(range(304,315)),list(range(315,325)), list(range(325,335)),
              list(range(304,315)),list(range(315,325)), list(range(325,335)),
              list(range(335,345)), list(range(345,355)), list(range(355,365)),
              list(range(335,345)), list(range(345,355)), list(range(355,365)),
              list(range(304,315)),list(range(304,315)), list(range(304,315)),
              list(range(304,315)), list(range(304,315)), list(range(304,315))]

## which patch infection starts in
start_patch = [[1,0,0,0],[1,0,0,0],[1,0,0,0],
               [0,1,0,0],[0,1,0,0],[0,1,0,0],
               [1,0,0,0],[1,0,0,0],[1,0,0,0],
               [0,1,0,0],[0,1,0,0],[0,1,0,0],
               [0,1,0,0],[0,1,0,0],[0,1,0,0],
               [0,1,0,0],[0,1,0,0],[0,1,0,0]]

#########the eta pq, s for patches 1,2 2,3, 3,4, 4,5

coastal_etas_1 = [[0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0],
                  [0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0],
                 [0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0],
                  [0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0], [0.02, 0.05, 0.4, 0], 
                  [0.02, 0.05, 0.4, 0],[0.15, 0.15, 0.15, 0],[0.096, 0.096, 0.096, 0],
                  [0.02, 0.05, 0.4, 0],[0.02, 0.05, 0.4, 0],[0.02, 0.05, 0.4, 0]]

coastal_etas_2 = [[0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4],
                  [0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4],
                  [0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4],
                  [0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4], [0, 0.02, 0.05, 0.4], 
                  [0, 0.02, 0.05, 0.4], [0, 0.15, 0.15, 0.15],[0, 0.096, 0.096, 0.096],
                  [0, 0.02, 0.05, 0.4],[0, 0.02, 0.05, 0.4],[0, 0.02, 0.05, 0.4]]

                #standard deviations for the associated etas 
coastal_etas_1_std = [[0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],
                      [0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],
                      [0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],
                      [0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],
                      [0.01, 0.01, 0.2, 0],[0.1, 0.1, 0.1, 0],[0.1, 0.1, 0.1, 0],
                      [0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0],[0.01, 0.01, 0.2, 0]]


coastal_etas_2_std = [[0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2],
                      [0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2],
                      [0, 0.01, 0.01, 0.2], [0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2],
                      [0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2],
                      [0, 0.01, 0.01, 0.2], [0, 0.1, 0.1, 0.1], [0, 0.1, 0.1, 0.1],
                      [0, 0.01, 0.01, 0.2], [0, 0.01, 0.01, 0.2],[0, 0.01, 0.01, 0.2]]

est_etas_1 = [[0.04, 0.02, 0.01, 0],  [0.04,0.02, 0.01, 0],[0.04, 0.02, 0.01, 0],
              [0.04, 0.02, 0.01, 0], [0.04, 0.02, 0.01, 0], [0.04, 0.02, 0.01, 0],
              [0.04, 0.02, 0.01, 0], [0.04, 0.02, 0.01, 0], [0.04,0.02, 0.01, 0],
              [0.04, 0.02, 0.01, 0], [0.04, 0.02, 0.01, 0], [0.04, 0.02, 0.01, 0],
              [0.04, 0.02, 0.01, 0], [0.023, 0.023, 0.023, 0], [0.1, 0.1, 0.1, 0], 
             [0.04, 0.02, 0.01, 0], [0.04, 0.02, 0.01, 0], [0.04, 0.02, 0.01, 0]]

est_etas_2 = [[0, 0.04, 0.02, 0.01,],  [0, 0.04, 0.02, 0.01,],[0, 0.04,0.02, 0.01,],
             [0, 0.04, 0.02, 0.01,],[0, 0.04, 0.02, 0.01,],[0, 0.04, 0.02, 0.01,],
             [0, 0.04, 0.02, 0.01,],[0, 0.04, 0.02, 0.01,],[0, 0.04, 0.02, 0.01,],
             [0, 0.04, 0.02, 0.01,],[0, 0.04, 0.02, 0.01,],[0, 0.04, 0.02, 0.01,],
              [0, 0.04, 0.02, 0.01,],  [0, 0.023, 0.023, 0.023], [0, 0.1, 0.1, 0.1], 
              [0, 0.04, 0.02, 0.01,],  [0, 0.04, 0.02, 0.01,],[0, 0.04,0.02, 0.01,]]

est_etas_1_std = [[0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], 
                  [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], 
                  [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], 
                  [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], 
                  [0, 0.002, 0.0014, 0.002], [0.002, 0.002, 0.002, 0], [0, 0.1, 0.1, 0.1],
                  [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002], [0, 0.002, 0.0014, 0.002]]

est_etas_2_std = [[0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0],
                  [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0],
                  [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0],
                  [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0],
                  [0.002, 0.0014, 0.002, 0], [0.002, 0.002, 0.002, 0], [0.1, 0.1, 0.1, 0], 
                  [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0], [0.002, 0.0014, 0.002, 0]]

### The time of year we change beta ss for the seasonal hypotheses
change_time = [[], [], [], 
               [], [], [], 
               [], [], [], 
               [], [], [],
               list(range(289, 371)) + list(range(651, 736)), list(range(289, 371)) + list(range(651, 736)), list(range(289, 371)) + list(range(651, 736)),
               [], list(range(289, 371)) + list(range(651, 736)), list(range(184, 274))+ list(range(549, 639)) + list(range(914, 1004))]

# how much to reduce beta 
reduction = [1, 1, 1,
             1, 1, 1, 
             1, 1, 1, 
             1, 1, 1,
             0.8, 0.8, 0.8,
             1, 0.8, 0.8]

## mean degree for coastal dolphins
coastal_deg_mean = [8,8,8,
                    8,8,8,
                    8,8,8,
                    8,8,8,
                    7,8,8,
                    8,8,8,]
## mean degree for estuarine dolphins
est_deg_mean = [6,6,6,
                6,6,6,
                6,6,6,
                6,6,6,
                7,6,6,
                6,6,6,]

coastal_deg_std = [0,0,0,
                   0,0,0,
                   0,0,0,
                   0,0,0,
                   0,0,0,
                   0,0,0]

est_deg_std = [0,0,0,
                   0,0,0,
                   0,0,0,
                   0,0,0,
                   0,0,0,
                   0,0,0]

b = 0

est_coast_data_cm = []
est_coast_data_sm = []
est_coast_data_stm = []
control_model_runs = ['SocBeh','Null1', "Null2", "Null3" ]
seasonal_model_runs = ['Control', 'SocBeh', 'Environ']
starttime_model_runs = ['start_p1_May1-10','start_p1_May11-20','start_p1_May21-31',
              'start_p2_May1-10','start_p2_May11-20','start_p2_May21-31',
              'start_p1_June1-10','start_p1_June11-20','start_p1_June21-31',
              'start_p2_June1-10','start_p2_June11-20','start_p2_June21-31']


for model in model_runs:
    print(model)
    
    total_est = sum(start_est_size)
    total_coast = sum(start_coastal_size)
    
    total_size_m, epi_prob,avg_error1, avg_error2, avg_error3, avg_error4,All_I_full_epi_1, All_I_full_epi_2, All_I_full_epi_3, All_I_full_epi_4, All_RR_cum, All_RM_cum, All_N_full_epi_1,All_N_full_epi_2,All_N_full_epi_3,All_N_full_epi_4, incidence_coastline, zone1est_incidence, zone2est_incidence, zone3est_incidence, zone4est_incidence, all_err2, all_err3, all_err4= simf.metapop_model(R0, start_time[b], start_patch[b], migratory1, migratory2, coastal_etas_1[b], coastal_etas_1_std[b], coastal_etas_2[b], coastal_etas_2_std[b], 
                  est_etas_1[b], est_etas_1_std[b], est_etas_2[b], est_etas_2_std[b], change_time[b], max_move_coast1, max_move_coast2, max_move_est1, max_move_est2,
                  reduction[b], alpha_list, mu_list, T,coastal_deg_mean[b], coastal_deg_std[b], est_deg_mean[b], est_deg_std[b], patches,
                  start_est_size, start_coastal_size, num_sims,mig1e,mig2e)
    
    
    ### Get files for SSE and r calculations to assess fit ####################
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
  #  CIdf.to_csv('SSE/SS_for_CI_'+model+'.csv')
    


    
    #### Generate Figures #######
    
    # Just one figure for the population size change by patch
    if b == 15:
        mean_pop_1 = []    
        for w in day_range:
            Ns = []
            for sim in All_N_full_epi_1:
                number = sim[w]
                Ns.append(number)
            avg = round(np.mean(Ns))
            mean_pop_1.append(avg)
        plt.plot(day_range,mean_pop_1, color = '#fbb4b9', alpha = 1, label="Patch 1")

        mean_pop_2 = []    
        for w in day_range:
            Ns = []
            for sim in All_N_full_epi_2:
                number = sim[w]
                Ns.append(number)
            avg = round(np.mean(Ns))
            mean_pop_2.append(avg)    
        plt.plot(day_range,mean_pop_2, color = '#f768a1', alpha = 1, label="Patch 2")

        mean_pop_3 = []    
        for w in day_range:
            Ns = []
            for sim in All_N_full_epi_3:
                number = sim[w]
                Ns.append(number)
            avg = round(np.mean(Ns))
            mean_pop_3.append(avg)              
        plt.plot(day_range,mean_pop_3, color = '#c51b8a', alpha = 1, label="Patch 3")

        mean_pop_4 = []    
        for w in day_range:
            Ns = []
            for sim in All_N_full_epi_4:
                number = sim[w]
                Ns.append(number)
            avg = round(np.mean(Ns))
            mean_pop_4.append(avg)
         
        plt.plot(day_range,mean_pop_4, color = '#7a0177', alpha = 1, label="Patch 4")
        plt.xlabel("Days")
        plt.ylabel("Number of Dolphins Present")
        plt.legend()

      #  plt.savefig("Figures/Patch_TotPop_Change.jpg", dpi = 300, bbox_inches = 'tight')
        plt.show()
        plt.close()
    
    #### Gow generate time series of infecitons ##############
    
    for i in range(0, len(All_I_full_epi_1)):
        
        plt.plot(week_range,All_I_full_epi_1[i], color = '#fbb4b9', alpha = 0.025)
        plt.plot(week_range,All_I_full_epi_2[i],  color = '#f768a1', alpha = 0.025) 
        plt.plot(week_range, All_I_full_epi_3[i],  color = '#c51b8a', alpha = 0.025) 
        plt.plot(week_range, All_I_full_epi_4[i],  color = '#7a0177', alpha = 0.025)
    
    mean_infected_1 = []      
    for w in week_range:
        infs = []
        for sim in All_I_full_epi_1:
            number = sim[w]
            infs.append(number)
        avg = round(np.mean(infs))
        mean_infected_1.append(avg)
    plt.plot(week_range,mean_infected_1, color = '#fbb4b9', alpha = 1, label="Patch 1")

    mean_infected_2 = []  
    for w in week_range:
        infs = []
        for sim in All_I_full_epi_2:
            number = sim[w]
            infs.append(number)
        avg = round(np.mean(infs))
        mean_infected_2.append(avg)
    plt.plot(week_range,mean_infected_2, color = '#f768a1', alpha = 1, label="Patch 2")

    mean_infected_3 = []  
    for w in week_range:
        infs = []
        for sim in All_I_full_epi_3:
            number = sim[w]
            infs.append(number)
        avg = round(np.mean(infs))
        mean_infected_3.append(avg)    
    plt.plot(week_range,mean_infected_3, color = '#c51b8a', alpha = 1, label="Patch 3")

    mean_infected_4 = []  
    for w in week_range:
        infs = []
        for sim in All_I_full_epi_4:
            number = sim[w]
            infs.append(number)
        avg = round(np.mean(infs))
        mean_infected_4.append(avg)     
    plt.plot(week_range,mean_infected_4, color = '#7a0177', alpha = 1, label="Patch 4")
    
    plt.ylim(0,2000)
    plt.xlim(34, 124)
    #week_labels = ["1-Mar-13", "10-May-13", "19-Jul-13", "27-Sep-13", "6-Dec-13", "14-Feb-14", "23-Apr-14", "25-Jun-14", "3-Sep-14", "12-Nov-14"]
    week_labels = ["Mar", "May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jul", "Sep"]
    plt.xticks(np.arange(34, 124, step=10),labels=week_labels, rotation = 45, size= 14)
    plt.yticks(size = 10)
    plt.ylabel("Number of New Infections", size = 15)
    #plt.legend(loc='lower right')

   # plt.savefig("Figures/Time_Series_Plot_"+model+".jpg", dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    
    ####### Coast Est Time Series Cumulative ##############
    for i in range(0,len(All_RR_cum)):
        prop1 = [x/total_est for x in All_RR_cum[i]]
        plt.plot(week_range,prop1, color = '#006600', alpha = 0.05)

    for i in range(0,len(All_RM_cum)):
        prop1 = [x/total_coast for x in All_RM_cum[i]]
        plt.plot(week_range,prop1, color = '#0066CC', alpha = 0.05)

    meanR_infected_1 = []  
    totalR1 =[]   
    for w in week_range:
        infs = []
        for sim in All_RR_cum:
            number = sim[w]
            final = round(sim[-1]/total_est, 2)
            if w == 1:
                totalR1.append(final)
            prop = number/total_est
            infs.append(prop)
        avg = round(np.mean(infs),2)
        meanR_infected_1.append(avg)   
    plt.plot(week_range,meanR_infected_1, color = '#006600', alpha = 1, label = "Estuarine")

    meanM_infected_1 = []   
    totalM1 = []    
    for w in week_range:
        infs = []
        for sim in All_RM_cum:
            number = sim[w]
            final = round(sim[-1]/total_coast,2)
            if w == 1:
                totalM1.append(final)
            prop = number/total_coast
            infs.append(prop)
        avg = round(np.mean(infs),2)
        meanM_infected_1.append(avg)
    plt.plot(week_range,meanM_infected_1, color = '#0066CC', alpha = 1, label = "Coastal")

    plt.ylim(0,1)
    plt.xlim(34, 134)
    week_labels = ["Mar", "May", "Jul", "Oct", "Dec", "Feb", "Apr", "Jul", "Sep", "Nov"]
    plt.xticks(np.arange(34, 134, step=10),labels=week_labels, rotation = 45, size= 10)
    plt.yticks(size = 10)
    plt.ylabel("Cumulative Proportion Infected", size = 15)
    plt.legend(loc='lower right', fontsize =20)
  #  plt.savefig("Figures/Coast_Est_Cum_TimeSeries_Plots_" +model+".jpg", dpi = 300, bbox_inches = 'tight')
    plt.show()
    plt.close()
    
    #### Coastal EStuarine Boxplot ##############
    coastal_stringlist = ["Coastal"]*len(totalM1)
    est_stringlist = ['Estuarine']*len(totalR1)
    stringlist = coastal_stringlist + est_stringlist
    total_size_list = totalM1 +totalR1
    boxplotdf = [totalM1, totalR1]
    if model in control_model_runs:
        est_coast_data_cm.append(boxplotdf)
    if model in seasonal_model_runs:
        est_coast_data_sm.append(boxplotdf)
    if model in starttime_model_runs:
        est_coast_data_stm.append(boxplotdf)
    labels = ['Coastal', 'Estuarine']
    colors = [ '#0066CC','#006600']

    fig, ax = plt.subplots()
    ax.set_ylabel('Total Proportion Infected', fontsize = 20)

    bplot = ax.boxplot(boxplotdf,
                       patch_artist=True,  # fill with color
                       labels=labels, medianprops = dict(color = "black", linewidth = 1.5))  # will be used to label x-ticks

    # fill with colors
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    plt.yticks(fontsize=15)
    plt.xticks(fontsize=20)
    plt.ylim([0.25,0.9])

     
  #  plt.savefig("Figures/CoastEst_BPs_"+model+".jpg", dpi = 300, bbox_inches= 'tight')
    plt.show()
    plt.close()
    
    
    ######## dataframe for assessing fit ############
    
    max_new = max(mean_infected_1+ mean_infected_2+ mean_infected_3+ mean_infected_4)
    Z1 = [x/max_new for x in mean_infected_1]
    Z2 = [x/max_new for x in mean_infected_2]
    Z3 = [x/max_new for x in mean_infected_3]
    Z4 = [x/max_new for x in mean_infected_4]
    average_zone_infections = [Z1, Z2, Z3, Z4]

    df = pd.DataFrame({'Zone1': Z1, 'Zone2': Z2, 'Zone3': Z3, 'Zone4': Z4})
   # df.to_csv('SSE/Average_forSSE_' + model +'.csv')
    
    b = b +1


### Examone coastal vs estuarine burden bias
i = 0
rb_boxplot_data = []
for model in control_model_runs:
    
    data = est_coast_data_cm[i]
    #print(data)
    relative_burden = [c/e for c,e in zip(data[0], data[1])]
    rb_boxplot_data.append(relative_burden)
    i = i +1

target_row = 3
# Move target row to first element of list.
idx = [target_row] + [i for i in range(len(rb_boxplot_data)) if i != target_row]
rb_boxplot_data = [rb_boxplot_data[i] for i in idx]

labels = [ 'Fully \n Empirical','Control: \n Ecotype \n Contact', 'Control: \n Movement', 'Control: \n Ecotype \n Movement']
fig, ax = plt.subplots()

bplot = ax.boxplot(rb_boxplot_data,
                  # patch_artist=True,  # fill with color
                   labels=labels, medianprops = dict(color = "black", linewidth = 1.5))  # will be used to label x-ticks

colors = [ '#0066CC', '#006600','#0066CC','#0066CC']

plt.yticks(fontsize=10)
plt.xticks(fontsize=10, rotation = 45)
plt.ylim (0.5,2.1)
plt.xlabel("Model", size = 15)
plt.ylabel("Relative Burden", size = 15)
#plt.ylim([0.25,0.9])

 
#plt.savefig("Figures/Burden_Bias_controls.jpg", dpi = 300, bbox_inches= 'tight')
plt.show()
plt.close()

########### For seasonality ############################

i = 0
rb_boxplot_data = []
for model in seasonal_model_runs:
    
    data = est_coast_data_sm[i]
    #print(data)
    relative_burden = [c/e for c,e in zip(data[0], data[1]) if e != 0]
    rb_boxplot_data.append(relative_burden)
    i = i +1

labels = ['Fully \n Empirical', 'Seasonal \n Behavior', 'Seasonal \n Environment']
fig, ax = plt.subplots()

bplot = ax.boxplot(rb_boxplot_data,
                #   patch_artist=True,  # fill with color
                   labels=labels, medianprops = dict(color = "black", linewidth = 1.5))  # will be used to label x-ticks

plt.yticks(fontsize=10)
plt.xticks(fontsize=10, rotation = 45)
plt.ylim (0.5,2.1)
plt.xlabel("Seasonality Applied", size = 15)
plt.ylabel("Relative Burden", size = 15)
#plt.ylim([0.25,0.9])

 
#plt.savefig("Figures/Burden_Bias_seasonal.jpg", dpi = 300, bbox_inches= 'tight')
plt.show()
plt.close()
 
    
########## For Start Times #####################################

i = 0
rb_boxplot_data = []
for model in starttime_model_runs:
    
    data = est_coast_data_stm[i]
    #print(data)
    relative_burden = [c/e for c,e in zip(data[0], data[1])]
    rb_boxplot_data.append(relative_burden)
    i = i +1

labels = ['patch 1 \n May1-10','patch 1 \n May11-20','patch 1 \n May21-31',
              'patch 2 \n May1-10','patch 2 \n May11-20','patch 2 \n May21-31',
              'patch 1 \n Mune1-10','patch 1 \n June11-20','patch 1 \n June21-31',
              'patch 2 \n June1-10','patch 2 \n June11-20','patch 2 \n June21-31']
fig, ax = plt.subplots()

bplot = ax.boxplot(rb_boxplot_data,
                  # patch_artist=True,  # fill with color
                   labels=labels, medianprops = dict(color = "black", linewidth = 1.5))  # will be used to label x-ticks

colors = [ '#0066CC', '#0066CC','#0066CC','#0066CC','#0066CC','#0066CC','#0066CC','#0066CC','#0066CC','#0066CC','#0066CC','#0066CC']

import matplotlib.patches as mpatches

plt.yticks(fontsize=10)
plt.xticks(fontsize=10, rotation = 90)
plt.ylim (0.5,1.5)
plt.xlabel("Start Patch and Time", size = 15)
plt.ylabel("Relative Burden", size = 15)
#plt.ylim([0.25,0.9])

 
#plt.savefig("Figures/Burden_Bias_starttimes.jpg", dpi = 300, bbox_inches= 'tight')
plt.show()
plt.close()

