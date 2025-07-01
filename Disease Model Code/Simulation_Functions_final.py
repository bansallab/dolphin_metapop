#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:58:32 2024

"""

import random
import numpy as np

def metapop_model(R0, start_time, start_patch, migratory1, migratory2, coastal_etas_1, coastal_etas_1_std, coastal_etas_2, coastal_etas_2_std, 
                  est_etas_1, est_etas_1_std, est_etas_2, est_etas_2_std, change_time, max_move_coast1, max_move_coast2, max_move_est1, max_move_est2,
                  reduction, alpha_list, mu_list, T, coastal_deg_mean, coastal_deg_std, est_deg_mean, est_deg_std, patches,
                  start_est_size, start_coastal_size, num_sims, mig1e, mig2e):
    
    ## define empty lists for later 
    All_I_full_epi_1 = []
    All_N_full_epi_1 = []
    
    All_I_full_epi_2 = []
    All_N_full_epi_2 = []
    
    All_I_full_epi_3 = []
    All_N_full_epi_3 = []
    
    All_I_full_epi_4 = []
    All_N_full_epi_4 = []
    
    
    All_IR_full_epi_1 = []
    All_NR_full_epi_1 = []
    
    All_IR_full_epi_2 = []
    All_NR_full_epi_2 = []
    
    All_IR_full_epi_3 = []
    All_NR_full_epi_3 = []
    
    All_IR_full_epi_4 = []
    All_NR_full_epi_4 = []
    
    
    All_IM_full_epi_1 = []
    All_NM_full_epi_1 = []
    
    All_IM_full_epi_2 = []
    All_NM_full_epi_2 = []
    
    All_IM_full_epi_3 = []
    All_NM_full_epi_3 = []
    
    All_IM_full_epi_4 = []
    All_NM_full_epi_4 = []
    
    All_RR_cum = []
    All_RM_cum = []
    All_coastline_cum = []
    
    All_R0_coast_warm = []
    All_R0_est_warm = []
    
    All_R0_coast_cold = []
    All_R0_est_cold = []
    
    All_RR1 = []
    All_RR2 = []
    All_RR3 = []
    All_RR4 = []
    
    All_RM1 = []
    All_RM2 = []
    All_RM3 = []
    All_RM4 = []
    
    All_NR1_weekly = []
    All_NR2_weekly = []
    All_NR3_weekly = []
    All_NR4_weekly = []
    
    All_NM1_weekly = []
    All_NM2_weekly = []
    All_NM3_weekly = []
    All_NM4_weekly = []

    
    for n in range(num_sims):
        print("Simulation!!!!!: ", n)
        
        ##Establish initial values and lists for the migratory populations in each zone
        SM = start_coastal_size.copy() #numbers come from preUME stock reports
        IM = [0, 0, 0, 0]
        RM = [0,0,0,0]
        
        SM_change = [[] for _ in range(4)]
        IM_change = [[] for _ in range(4)]
        IM_change_new = [[] for _ in range(4)]
        IM_change_weekly = [[] for _ in range(4)]
        NM_change_weekly = [[] for _ in range(4)]
        
        RM_change = [[] for _ in range(4)]
        NM_change = [[] for _ in range(4)]
        
        Sarrivals_fall_c = [0,0,0,0,0]
        Iarrivals_fall_c = [0,0,0,0,0]
        Rarrivals_fall_c = [0,0,0,0,0]
        
        Sarrivals_spring_c= [0,0,0,0,0]
        Iarrivals_spring_c = [0,0,0,0,0]
        Rarrivals_spring_c = [0,0,0,0,0]
    
        
        ### Establish initial values for the residentital populations in each zone
        
        SR = start_est_size.copy()
        IR = [0, 0, 0, 0]
        RR = [0,0,0,0]
          
        SR_change = [[] for _ in range(4)]
        IR_change = [[] for _ in range(4)]
        IR_change_new = [[] for _ in range(4)]
        IR_change_weekly = [[] for _ in range(4)]
        NR_change_weekly = [[] for _ in range(4)]
        
        RR_change = [[] for _ in range(4)]
        NR_change = [[] for _ in range(4)]
        
        Sarrivals_fall_r = [0,0,0,0,0]
        Iarrivals_fall_r = [0,0,0,0,0]
        Rarrivals_fall_r = [0,0,0,0,0]
        
        Sarrivals_spring_r= [0,0,0,0,0]
        Iarrivals_spring_r = [0,0,0,0,0]
        Rarrivals_spring_r = [0,0,0,0,0]
        
        
        ### Establish lists for total in each patch.
        
        S_change = [[] for _ in range(4)]
        I_change = [[] for _ in range(4)]
        I_change_new = [[] for _ in range(4)]
        I_change_weekly = [[] for _ in range(4)]
        
        R_change = [[] for _ in range(4)]
        N_change = [[] for _ in range(4)]
        
        fall_moving_c = [0,0,0,0] 
        spring_moving_c = [0,0,0,0]
        
        fall_moving_r = [0,0,0,0] 
        spring_moving_r = [0,0,0,0]
        
        infection_day = random.choice(start_time) #choose random infection day from list
        
        R0_genM = [[],[],[],[]]
        R0_genR = [[],[],[],[]]
        
        pM = [0,0,0,0]
        pR = [0,0,0,0]
        
        for t in range(0,T):
            
            if t == 365 or t == 729:
                fall_moving_c = [0,0,0,0] # restart the max move list each year
                spring_moving_c = [0,0,0,0]
                
                fall_moving_r = [0,0,0,0] 
                spring_moving_r = [0,0,0,0]
            
            if t == infection_day:
                IM = start_patch.copy() 
            else: IM = IM
                        
            for patch in patches:
                
                #establish comparments for coastals
                SMt = SM[patch]
                IMt = IM[patch]
                RMt = RM[patch]
                NMt = SMt +IMt +RMt
                
                #establish compartments for estuarine
                SRt = SR[patch]
                IRt = IR[patch]
                RRt = RR[patch]
                NRt = SRt + IRt + RRt
                 
                
                mu = 1/random.choice(mu_list)  # randomly choose the recovery rate based on an IP between 6-9 days
                tau = (R0 * mu) /7 # 7 corresponds to the average degree of PCDP dolphins
                alpha = random.choice(alpha_list) #randomly choose the alpha 
                
                
                if t in change_time:
                    est_deg = 0
                    while est_deg <= 0:        
                        est_deg = np.random.normal(est_deg_mean, est_deg_std, 1)
                        est_deg = est_deg[0]
                    
                    coast_deg = 0
                    while coast_deg <= 0:
                        coast_deg = np.random.normal(coastal_deg_mean, coastal_deg_std, 1)
                        coast_deg = coast_deg[0]
                    
                    R0_C = (coast_deg * tau) / mu
                    All_R0_coast_warm.append(R0_C)
                    
                    R0_E = (est_deg * tau) / mu
                    All_R0_est_warm.append(R0_E)
    
                ## reduce degree outside of the cold season by 1/3 to match with social behavior
                else: 
                    est_deg = 0
                    while est_deg <= 0:        
                        est_deg = np.random.normal(est_deg_mean, est_deg_std, 1)
                        est_deg = est_deg[0] * reduction
                    
                    coast_deg = 0
                    while coast_deg <= 0:
                        coast_deg = np.random.normal(coastal_deg_mean, coastal_deg_std, 1)
                        coast_deg = coast_deg[0] * reduction
                    
                    R0_C = (coast_deg * tau) / mu
                    All_R0_coast_cold.append(R0_C)
                    
                    R0_E = (est_deg * tau) / mu
                    All_R0_est_cold.append(R0_E)
    
                
              ## calculate the gamma for coastal and estuarine and the gamma mixing
                if NMt == 0 and NRt != 0:
                    #gammaR = 0
                    gammaR = R0_E * mu*(IRt/NRt) #gamma for residential infection within residential
                    gammaRmix = 0 #gamma for residential infection when mixing with migratories
                    
                    gammaM = 0 #gamma for migratory infection within migratories
                    #gammaMmix = 0
                    gammaMmix = R0_C * mu *alpha* (IRt/NRt) #gamma for migratory infection when mixing with residents
                
                
                elif NMt == 0 and NRt == 0:
                    gammaR =0 #gamma for residential infection within residential
                    gammaRmix = 0 #gamma for residential infection when mixing with migratories
                    
                    gammaM = 0 #gamma for migratory infection within migratories
                    gammaMmix = 0 #gamma for migratory infection when mixing with residents
     
                elif NRt == 0 and NMt != 0:
                    #gammaR = 0
                    gammaR = 0 #gamma for residential infection within residential
                    gammaRmix = R0_E *alpha * mu * (IMt/NMt) #gamma for residential infection when mixing with migratories
                    
                    gammaM = R0_C * mu * (IMt/NMt) #gamma for migratory infection within migratories
                    #gammaMmix = 0
                    gammaMmix = 0 #gamma for migratory infection when mixing with residents
                
                else:
                
                    gammaR = R0_E * mu*(IRt/NRt) #gamma for residential infection within residential
                    gammaRmix = R0_E *alpha * mu * (IMt/NMt) #gamma for residential infection when mixing with migratories
                    
                    gammaM = R0_C * mu * (IMt/NMt) #gamma for migratory infection within migratories
                    gammaMmix = R0_C * mu *alpha* (IRt/NRt) #gamma for migratory infection when mixing with residents
               
                deltaSM = np.random.binomial(SMt, gammaM) + np.random.binomial(SMt, gammaMmix) #change in infection rates for both populations based on infection process and mixing
                deltaSR = np.random.binomial(SRt, gammaR) + np.random.binomial(SRt, gammaRmix)
                
                deltaIM = np.random.binomial(IMt, mu)
                deltaIR = np.random.binomial(IRt, mu)  
                
                ##### Getting R0 code ###############
                if IM[patch] > 1:
                    pM[patch] = pM[patch] +1
                    if pM[patch] < 9:
                        #print("coastal patch: ", patch, "infection starts on day: ",t, "with ", deltaSM, " infections")
                        
                        #print("patch: ", patch, "on gen day: ", pM[patch],"new infections: ", deltaSM, "previously infected: ", IMt)
                        R0_genM[patch].append(deltaSM)
                
                if IR[patch] > 1:
                    pR[patch] = pR[patch] +1
                    if pR[patch] < 9:
                        #print("estuarine patch: ", patch, "infection starts on day: ",t, "with ", deltaSR, " infections")
                        
                        R0_genR[patch].append(deltaSR)
                ###############################################

    
        #####migratory processes for coastals and for the moving estuarine
                
                if t in migratory1: ###leaving and going south migration
                    
                #### first for coastal/migratory animals ##############
                    mig_prob = np.random.normal(coastal_etas_1[patch], coastal_etas_1_std[patch], 1)
                    while mig_prob > 1 or mig_prob < 0:
                        mig_prob = np.random.normal(coastal_etas_1[patch], coastal_etas_1_std[patch], 1)
                    mig_prob = abs(mig_prob[0])
                    max_leave = max_move_coast1[patch]
                    current_left = fall_moving_c[patch]
                    if fall_moving_c[patch]< max_leave:
                        Nleaving = np.random.binomial(NMt, mig_prob)
                        fall_moving_c[patch] = fall_moving_c[patch] + Nleaving
                        if fall_moving_c[patch]> max_leave:
                            Nleaving = max_leave-current_left
                            fall_moving_c[patch] = max_leave
                        if NMt == 0:
                            propS = 0
                            propI = 0
                            propR = 0
                        else:
                            propS = SMt/NMt
                            propI = IMt/NMt
                            propR = RMt/NMt
                        
                        Sleaving_c = propS * Nleaving
                        Ileaving_c = propI * Nleaving
                        Rleaving_c = Nleaving -Sleaving_c-Ileaving_c
                    
                    else:
                        Sleaving_c = 0
                        Ileaving_c = 0
                        Rleaving_c = 0
                    
                    
                    Sarriving_c = Sarrivals_fall_c[patch]
                        
                    
                    Iarriving_c = Iarrivals_fall_c[patch]
                        
                    
                    Rarriving_c = Rarrivals_fall_c[patch]
                        
                        
                    Sarrivals_fall_c[patch+1] = Sleaving_c
                    Iarrivals_fall_c[patch+1] = Ileaving_c
                    Rarrivals_fall_c[patch+1] = Rleaving_c
                       
                                
        
                elif t in migratory2: ###leaving and going north migration
                 
                #### first for coastal/migratory animals ##############
                     mig_prob = np.random.normal(coastal_etas_2[patch], coastal_etas_2_std[patch], 1)
                     while mig_prob > 1 or mig_prob < 0:
                         mig_prob = np.random.normal(coastal_etas_2[patch], coastal_etas_2_std[patch], 1)
                     mig_prob = abs(mig_prob[0])
                     max_leave = max_move_coast2[patch]
                     current_left = spring_moving_c[patch]
                     
                     if spring_moving_c[patch]< max_leave:
                         Nleaving = np.random.binomial(NMt, mig_prob)
                         spring_moving_c[patch] = spring_moving_c[patch] + Nleaving
                         if spring_moving_c[patch]> max_leave:
                             Nleaving = max_leave-current_left
                             spring_moving_c[patch] = max_leave
                     
                         if NMt == 0:
                             propS = 0
                             propI = 0
                             propR = 0
                         else:
                             propS = SMt/NMt
                             propI = IMt/NMt
                             propR = RMt/NMt
                         
                         Sleaving_c = propS * Nleaving
                         Ileaving_c = propI * Nleaving
                         Rleaving_c = Nleaving -Sleaving_c-Ileaving_c
                         
                         
                     
                     else:
                         Sleaving_c = 0
                         Ileaving_c = 0
                         Rleaving_c = 0
                    
                    
                     Sarriving_c = Sarrivals_spring_c[patch+1]
                     Iarriving_c = Iarrivals_spring_c[patch+1]
                     Rarriving_c = Rarrivals_spring_c[patch+1]
                        
                        
                     Sarrivals_spring_c[patch] = Sleaving_c
                     Iarrivals_spring_c[patch] = Ileaving_c
                     Rarrivals_spring_c[patch] = Rleaving_c 
                
                else:
                    Sleaving_c = 0
                    Sarriving_c = 0
                    Ileaving_c = 0
                    Iarriving_c = 0
                    Rleaving_c = 0
                    Rarriving_c = 0
                     
                     ########## Next get the movement of estuarine in the population 
                if t in mig1e:
                     mov_prob = np.random.normal(est_etas_1[patch], est_etas_1_std[patch], 1)
                     mov_prob = abs(mov_prob[0])
                    
                     max_leave = max_move_est1[patch]
                     current_left = fall_moving_r[patch]
                    
                     if fall_moving_r[patch]< max_leave:
                         Nleaving = np.random.binomial(NRt, mov_prob)
                         fall_moving_r[patch] = fall_moving_r[patch] + Nleaving
                         if fall_moving_r[patch]> max_leave:
                             Nleaving = max_leave-current_left
                             fall_moving_r[patch] = max_leave
                         if NRt == 0:
                             propS = 0
                             propI = 0
                             propR = 0
                         else:
                             propS = SRt/NRt
                             propI = IRt/NRt
                             propR = RRt/NRt
                        
                         Sleaving_r = propS * Nleaving
                         Ileaving_r = propI * Nleaving
                         Rleaving_r = Nleaving -Sleaving_r-Ileaving_r
                    
                     else:
                         Sleaving_r = 0
                         Ileaving_r = 0
                         Rleaving_r = 0
                    
                    
                     Sarriving_r = Sarrivals_fall_r[patch]
                        
                    
                     Iarriving_r = Iarrivals_fall_r[patch]
                        
                    
                     Rarriving_r = Rarrivals_fall_r[patch]
                        
                        
                     Sarrivals_fall_r[patch+1] = Sleaving_r
                     Iarrivals_fall_r[patch+1] = Ileaving_r
                     Rarrivals_fall_r[patch+1] = Rleaving_r
                 
                    ########## Next get the movement of estuarine in the population 
                elif t in mig2e:
                     mov_prob = np.random.normal(est_etas_2[patch], est_etas_2_std[patch], 1)
                     mov_prob = abs(mov_prob[0])
                     max_leave = max_move_est2[patch]
                     current_left = spring_moving_r[patch]
                     
                     if spring_moving_r[patch]< max_leave:
                         Nleaving = np.random.binomial(NRt, mov_prob)
                         spring_moving_r[patch] = spring_moving_r[patch] + Nleaving
                         if spring_moving_r[patch]> max_leave:
                             Nleaving = max_leave-current_left
                             spring_moving_r[patch] = max_leave
                     
                         if NRt == 0:
                             propS = 0
                             propI = 0
                             propR = 0
                         else:
                             propS = SRt/NRt
                             propI = IRt/NRt
                             propR = RRt/NRt
                         
                         Sleaving_r = propS * Nleaving
                         Ileaving_r = propI * Nleaving
                         Rleaving_r = Nleaving -Sleaving_r-Ileaving_r
                         
                         
                     
                     else:
                         Sleaving_r = 0
                         Ileaving_r = 0
                         Rleaving_r = 0
                    
                    
                     Sarriving_r = Sarrivals_spring_r[patch+1]
                     Iarriving_r = Iarrivals_spring_r[patch+1]
                     Rarriving_r = Rarrivals_spring_r[patch+1]
                        
                        
                     Sarrivals_spring_r[patch] = Sleaving_r
                     Iarrivals_spring_r[patch] = Ileaving_r
                     Rarrivals_spring_r[patch] = Rleaving_r 
          
                    
        
                else:
                    Sleaving_r = 0
                    Sarriving_r = 0
                    Ileaving_r = 0
                    Iarriving_r = 0
                    Rleaving_r = 0
                    Rarriving_r = 0
    
                                
    
                ### Now put it all together with migration, infection and interpopulation mixing 
                
                ### For the migratory individuals     
                SMt1 = SMt - deltaSM - Sleaving_c + Sarriving_c 
                IMt1 = IMt +deltaSM -deltaIM -Ileaving_c +Iarriving_c 
                RMt1 = RMt +deltaIM - Rleaving_c +Rarriving_c 
        
                
                if SMt1 < 0:
                    SMt1 = 0
                if IMt1 < 0:
                    IMt1 = 0
                if RMt1 < 0:
                    RMt1 = 0   
                
                
                SM[patch] = SMt1
                IM[patch] = IMt1
                RM[patch] = RMt1
                NMt1 = SMt1+ IMt1 +RMt1
                                    
                SM_change[patch].append(SMt1)
                IM_change[patch].append(IMt1)
                IM_change_new[patch].append(deltaSM)
                RM_change[patch].append(RMt1)
                NM_change[patch].append(NMt1)
                
                ## For the residential individuals
                SRt1 = SRt - deltaSR - Sleaving_r + Sarriving_r 
                IRt1 = IRt +deltaSR -deltaIR -Ileaving_r +Iarriving_r 
                RRt1 = RRt +deltaIR - Rleaving_r +Rarriving_r
        
                
                if SRt1 < 0:
                    SRt1 = 0
                if IRt1 < 0:
                    IRt1 = 0
                if RRt1 < 0:
                    RRt1 = 0   
                
                
                SR[patch] = SRt1
                IR[patch] = IRt1
                RR[patch] = RRt1
                NRt1 = SRt1+ IRt1 +RRt1
                                    
                SR_change[patch].append(SRt1)
                IR_change[patch].append(IRt1)
                IR_change_new[patch].append(deltaSR)
                RR_change[patch].append(RRt1)
                NR_change[patch].append(NRt1)
                
                
                ### Also get total patch change
                
                                    
                S_change[patch].append(SMt1+SRt1)
                I_change[patch].append(IMt1+ IRt1)
                I_change_new[patch].append(deltaSM + deltaSR)
                R_change[patch].append(RMt1+RRt1)
                N_change[patch].append(NMt1+ NRt1)
           
    
        for patch in patches:
            
            I_weekly = np.add.reduceat(I_change_new[patch], np.arange(0, len(I_change_new[patch]), 7))
            I_weekly = list(I_weekly)
            I_change_weekly[patch].append(I_weekly)
            
            IM_weekly = np.add.reduceat(IM_change_new[patch], np.arange(0, len(IM_change_new[patch]), 7))
            IM_weekly = list(IM_weekly)
            IM_change_weekly[patch].append(IM_weekly)
            
            IR_weekly = np.add.reduceat(IR_change_new[patch], np.arange(0, len(IR_change_new[patch]), 7))
            IR_weekly = list(IR_weekly)
            IR_change_weekly[patch].append(IR_weekly)
            
            NR_weekly = NR_change[patch][0::7]
            NR_weekly = list(NR_weekly)
            NR_change_weekly[patch].append(NR_weekly)
            
            NM_weekly = NM_change[patch][0::7]
            NM_weekly = list(NM_weekly)
            NM_change_weekly[patch].append(NM_weekly)
        
        
        RR_Cum = []
        RM_Cum = []
        
        RR_1_Cum = []
        RR_2_Cum = []
        RR_3_Cum = []
        RR_4_Cum = []
        
        RM_1_Cum = []
        RM_2_Cum = []
        RM_3_Cum = []
        RM_4_Cum = []
        
        for i in range(0, T):
    
            RR1 = RR_change[0][i]
            RR_1_Cum.append(RR1)
            RR2 = RR_change[1][i]
            RR_2_Cum.append(RR2)
            RR3 = RR_change[2][i]
            RR_3_Cum.append(RR3)
            RR4 = RR_change[3][i]
            RR_4_Cum.append(RR4)
    
            RM1 = RM_change[0][i]
            RM_1_Cum.append(RM1)
            RM2 = RM_change[1][i]
            RM_2_Cum.append(RM2)
            RM3 = RM_change[2][i]
            RM_3_Cum.append(RM3)
            RM4 = RM_change[3][i]
            RM_4_Cum.append(RM4)
            
            totalRR = RR1+ RR2 + RR3 + RR4
            totalRM = RM1+ RM2 + RM3 + RM4
            RR_Cum.append(totalRR)
            RM_Cum.append(totalRM)
        
        RR_weekly = RR_Cum[0::7]
        RM_weekly = RM_Cum[0::7]
        
        RR1_weekly = RR_1_Cum[0::7]
        RR2_weekly = RR_2_Cum[0::7]
        RR3_weekly = RR_3_Cum[0::7]
        RR4_weekly = RR_4_Cum[0::7]
        
        RM1_weekly = RM_1_Cum[0::7]
        RM2_weekly = RM_2_Cum[0::7]
        RM3_weekly = RM_3_Cum[0::7]
        RM4_weekly = RM_4_Cum[0::7]
            
    
                
        if max(R_change[0]) + max(R_change[1]) + max(R_change[2]) + max(R_change[3]) > round((sum(start_coastal_size)+sum(start_est_size))*0.1): # 10% of the population
        
            All_RR_cum.append(RR_weekly)
            All_RM_cum.append(RM_weekly)
            All_coastline_cum.append([e + s for e,s in zip(RR_weekly,RM_weekly)])
            
            
            All_RR1.append(RR1_weekly)
            All_RR2.append(RR2_weekly)
            All_RR3.append(RR3_weekly)
            All_RR4.append(RR4_weekly)
            
            All_RM1.append(RM1_weekly)
            All_RM2.append(RM2_weekly)
            All_RM3.append(RM3_weekly)
            All_RM4.append(RM4_weekly)
            
            All_I_full_epi_1.append(I_change_weekly[0][0])
            All_I_full_epi_2.append(I_change_weekly[1][0])
            All_I_full_epi_3.append(I_change_weekly[2][0])
            All_I_full_epi_4.append(I_change_weekly[3][0])
            
            All_N_full_epi_1.append(N_change[0])
            All_N_full_epi_2.append(N_change[1])
            All_N_full_epi_3.append(N_change[2])
            All_N_full_epi_4.append(N_change[3])
            
            
            All_IR_full_epi_1.append(IR_change_weekly[0][0])
            All_IR_full_epi_2.append(IR_change_weekly[1][0])
            All_IR_full_epi_3.append(IR_change_weekly[2][0])
            All_IR_full_epi_4.append(IR_change_weekly[3][0])
            
            All_NR_full_epi_1.append(NR_change[0])
            All_NR_full_epi_2.append(NR_change[1])
            All_NR_full_epi_3.append(NR_change[2])
            All_NR_full_epi_4.append(NR_change[3])
            
            All_IM_full_epi_1.append(IM_change_weekly[0][0])
            All_IM_full_epi_2.append(IM_change_weekly[1][0])
            All_IM_full_epi_3.append(IM_change_weekly[2][0])
            All_IM_full_epi_4.append(IM_change_weekly[3][0])
            
            All_NM_full_epi_1.append(NM_change[0])
            All_NM_full_epi_2.append(NM_change[1])
            All_NM_full_epi_3.append(NM_change[2])
            All_NM_full_epi_4.append(NM_change[3])
            
            All_NM1_weekly.append(NM_change_weekly[0][0])
            All_NM2_weekly.append(NM_change_weekly[1][0])
            All_NM3_weekly.append(NM_change_weekly[2][0])
            All_NM4_weekly.append(NM_change_weekly[3][0])
            
            All_NR1_weekly.append(NR_change_weekly[0][0])
            All_NR2_weekly.append(NR_change_weekly[1][0])
            All_NR3_weekly.append(NR_change_weekly[2][0])
            All_NR4_weekly.append(NR_change_weekly[3][0])
        

    total_size = [max(n)/ (sum(start_coastal_size)+sum(start_est_size)) for n in All_coastline_cum]
    total_size_m = round(np.mean(total_size),2)
    #print(All_RR1)
    #print(len(All_NR1_weekly))

    epi_prob = round(len(total_size)/num_sims,2)
    
    
    incidence_coastline = []
    for ltotal in All_coastline_cum:
        incidence = [i/ (sum(start_coastal_size)+sum(start_est_size)) for i in ltotal]
        incidence_coastline.append(incidence)

    o = 0 
    zone1est_incidence = []
    for l in All_RR1:
        
        z1_size = [e / s for e,s in zip(l,All_NR1_weekly[o])]
        zone1est_incidence.append(z1_size)
        o = o+1
    
    o = 0 
    zone2est_incidence = []
    for l in All_RR2:
        
        z2_size = [e / s for e,s in zip(l,All_NR2_weekly[o])]
        zone2est_incidence.append(z2_size)
        o = o+1
    
    o = 0 
    zone3est_incidence = []
    for l in All_RR3:
        
        z3_size = [e / s for e,s in zip(l,All_NR3_weekly[o])]
        zone3est_incidence.append(z3_size)
        o = o+1
        
    o = 0 
    zone4est_incidence = []
    for l in All_RR4:
        
        z4_size = [e / s for e,s in zip(l,All_NR4_weekly[o])]
        zone4est_incidence.append(z4_size)
        o = o+1

    
    incidence_error1 = []
    incidence_error2 = []
    incidence_error3 = []
    incidence_error4 = []
    for s in range(0, len(incidence_coastline)):
        error1 = [e - t for t,e in zip(incidence_coastline[s], zone1est_incidence[s])]
        avg_err1 = np.mean(error1)
        incidence_error1.append(avg_err1)
        
        error2 = [e - t for t,e in zip(incidence_coastline[s], zone2est_incidence[s])]
        avg_err2 = np.mean(error2)
        incidence_error2.append(avg_err2)
        
        error3 = [e - t for t,e in zip(incidence_coastline[s], zone3est_incidence[s])]
        avg_err3 = np.mean(error3)
        incidence_error3.append(avg_err3)
        
        error4 = [e - t for t,e in zip(incidence_coastline[s], zone4est_incidence[s])]
        avg_err4 = np.mean(error4)
        incidence_error4.append(avg_err4)
    
    avg_error1 = np.mean(incidence_error1)
    avg_error2 = np.mean(incidence_error2)
    avg_error3 = np.mean(incidence_error3)
    avg_error4 = np.mean(incidence_error4)

            
    return(total_size_m, epi_prob,avg_error1, avg_error2, avg_error3, avg_error4,
           All_I_full_epi_1, All_I_full_epi_2, All_I_full_epi_3, All_I_full_epi_4, All_RR_cum, All_RM_cum,
           All_N_full_epi_1, All_N_full_epi_2, All_N_full_epi_3, All_N_full_epi_4, incidence_coastline, zone1est_incidence,
           zone2est_incidence, zone3est_incidence, zone4est_incidence, incidence_error2, incidence_error3, incidence_error4)

def calc_correlation(actual, predic):
    a_diff = actual - np.mean(actual)
    p_diff = predic - np.mean(predic)
    numerator = np.sum(a_diff * p_diff)
    denominator = np.sqrt(np.sum(a_diff ** 2)) * np.sqrt(np.sum(p_diff ** 2))
    return numerator / denominator
            