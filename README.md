# Seasonal contact and migration structure mass epidemics and inform outbreak preparedness in bottlenose dolphins

Dataset DOI: 10.5281/zenodo.15784437

## Description of the data and file structure

## **Directories**

### "Data and Code for Patch determination and movement".&#x20;

This directory contains data and code used to 1) estimate metapopulation patches and 2) determine movement rates.

The "MABDC_sighting_data.csv" file is used in "MABDC_data_clean_and_Patch_Cluster_Analysis.py" to determine the metapopulation patches and again in "Get_data_for_MSCRM.py" to generate the data inputs necessary to perform the continuous time multistate capture recapture models on coastal and estuarine individuals. This CTMSCRM can be found in the "stan" directory, and is carried out using the associated datasheets in "dolphin_HMM_four_states.R".



### "Data and Code for contact transmission rates"

This directory contains data and code used to determine the contact driven transmission rates for coastal and estuarine ecotypes and to generate the the ecotype mixing parameter "alpha".

"Assign_PCDP_individuals_to_ecotype.py" uses "Clean_Degree_Data_PCDP.csv" and "Focal_Individuals_avg_distance_from_shore.csv" to assign ecotype designations to focal individuals from the PCDP based on their average distance sighted from shore. "Get_alpha.py" uses "Distance_from_shore_all_dolphins_all_sightings.csv" and "All_PCDP_Sightings.csv" to generate the mixing parameter alpha.

In the "Estimating Degree" directory, the code "Estimate_degree_and_Beta_over_day_for_ecotype.R" uses "Clean_Degree_Data_PCDP_withStock_Assignments.csv" and the associated data to estimate average synchrony degree for coastal and estuarine individuals over the course of a day.

### "Disease Model Code"

"Run_Disease_Model_main.py" applies the metapopulation model desribed in "Simulation_Functions_final.py" to 1) determine the most likely start time and patch location for past epidemics, test seasonal changes in beta, and understand the impact of metapopulation structure using different control senarios. In the "SSE" directory, "Generate_1987/2013_SSE_and_r_compare_and_boxplots.py" will generate the sum squared error (SSE) and Pearson's correlation (r) scores for each of these model runs to asses their projected infection time series fits to the 1987 and 2013 outbreak data respectively.

"Run_Disease_Model_to_assess_EpidemicRisk_and_Surveillance.py" will run our best fitting metapopulation model for 48 different start time and location scenarios to assess epidemic risk values and questiosn related to surveillance. the "RiskAnalysisSSE" directory will generate the SSE and r values for these model runs.

### "1987/2013 Stranding and Outbreak Data and Figures"

These directories contain the stranding data and code used to generate the outbreak data used to assess disease model fit.



## Code/software

All data are in csv file format. All code is written in R or Python 3.
## Access information

**Data was derived from the following sources:**

* National Marine Fisheries Service
* Mid-Atlantic Bottlenose Dolphin Catalog
* Potomac-Chesapeake Dolphin Project
* Smithsonian Institution
