library(glmm)
library(ggplot2)
library(effects)
library(cowplot)
library(MASS)
library(bbmle)
library(effects)
library(sjPlot)
library(lme4)
library(glmmTMB)
library(DHARMa)
library(car)
library(performance)
library(dplyr)
library(interactions)

# function to draw from a distribution with a given mean, var, min and max
rgbeta <- function(n, mean, var, min = 0, max = 1)
{
  dmin <- mean - min
  dmax <- max - mean
  
  if (dmin <= 0 || dmax <= 0)
  {
    stop(paste("mean must be between min =", min, "and max =", max)) 
  }
  
  if (var >= dmin * dmax)
  {
    stop(paste("var must be less than (mean - min) * (max - mean) =", dmin * dmax))
  }
  
  # mean and variance of the standard beta distributed variable
  mx <- (mean - min) / (max - min)
  vx <- var / (max - min)^2
  
  # find the corresponding alpha-beta parameterization
  a <- ((1 - mx) / vx - 1 / mx) * mx^2
  b <- a * (1 / mx - 1)
  
  # generate standard beta observations and transform
  x <- rbeta(n, a, b)
  y <- (max - min) * x + min
  
  return(y)
}

#Import and clean the data
PCDP <- read.csv("Clean_Degree_Data_PCDP_withStock_Assignments.csv", header=T)
PCDP<- subset(PCDP, select = c(Dolphin_ID,Follow_length,Degree, Stock, Year, Number_Syncs))
PCDP$Stock <- as.factor(PCDP$Stock)
PCDP$Year_unique <- as.factor(PCDP$Year)
PCDP$duration_log <- log(PCDP$Follow_length) #scale follow duration to encourage convergence
PCDP_full<-PCDP
PCDP<- PCDP[PCDP$Stock != "Undetermined", ]

### Sync Occurrence Model
## First we get at the P(s), or the probability that individuals will sync given they are in a group
##Therefore we use a glmm with a binary response variable of Y/N sync occured in follow

PCDP<- PCDP %>%
  mutate(Occur = case_when(Number_Syncs ==0  ~ "N",
                           Number_Syncs > 0 ~ "Y"
  ))
PCDP$Occur<- as.factor(PCDP$Occur)

PCDP$Stock <- as.factor(PCDP$Stock)

# main model
occurrence_model1<- glmer(Occur ~Stock + duration_log+(1|Year)+(1|Dolphin_ID), data = PCDP, family = binomial)
simulationOutput_min <- simulateResiduals(fittedModel = occurrence_model1)
testDispersion(simulationOutput_min) #test fit and dispersion
plot(allEffects(occurrence_model1)) #check effects

#view differences among stocks
sjPlot:: tab_model(occurrence_model1, transform = NULL, digits = 4)

#save the P(s) data by exporting the model estimates for P(g) by demo/study site
eff_occ <- effects::effect("Stock", occurrence_model1)
x1_occ <- as.data.frame(eff_occ)
x1_occ

write.csv(eff_occ, "Occurrence_of_syncs.csv")

######For Number Syncs
## Next we only look at follow where a sync occurred, and we estimate the rates of syncrony when they sync
## to do this we use a glmm where # syncs ~demo*studysite +followlength and use the model estimates to get at rate

PCDP_drop<- PCDP[PCDP$Occur != "N", ]
coast<- PCDP_drop[PCDP_drop$Stock == "Coast", ]
est<- PCDP_drop[PCDP_drop$Stock == "Est", ]
write.csv(PCDP_drop, "Full_data_drop_0degree_follows.csv")

##Run the model
mod1_min<- glmer.nb(Number_Syncs ~Stock + duration_log+(1|Year)+(1|Dolphin_ID), data = PCDP_drop)

## Test to make sure not overdispersed
simulationOutput_min <- simulateResiduals(fittedModel = mod1_min)
testDispersion(simulationOutput_min)
plot(allEffects(mod1_min))
check_convergence(mod1_min)

#view significance across demo/study site
sjPlot:: tab_model(mod1_min, transform = NULL, digits = 4)

##Save the data
saveRDS(mod1_min, "Syncrony_rate_model.rds")
eff_min <- effects::effect("Stock", mod1_min)
x1_min <- as.data.frame(eff_min)
x1_min
write.csv(x1_min, "Sync_rate_results.csv")

#####################################################################################
#### Now we estimate average degree for a day ######################################

model <- readRDS(file = "Syncrony_rate_model.rds")
data<- read.csv("Full_data_drop_0degree_follows.csv")
model_results<- read.csv("Sync_rate_results.csv")
occ_model_results<- read.csv("Occurrence_of_syncs.csv")


PA_results <- read.csv("Estimated_PA.csv")
power_law_curve <- read.csv("powerlaw_curve.csv")


##### We will estimate degree 1000 times for each demo group/study site
n <- 1000
average_follow_length = mean(data$Follow_length)

m_PS <- occ_model_results$fit
sd_PS<- occ_model_results$se
min_PS <- occ_model_results$lower
max_PS<- occ_model_results$upper

m_rate <- model_results$fit
sd_rate <- model_results$se
min_rate <- model_results$lower
max_rate <- model_results$upper

alpha = power_law_curve$a[1]
lambda = power_law_curve$lambda[1]

stocks<- 1:2
samples<- 1:n
estimated_degrees<- list()

IP_range<- list(1) #range of potential infectious periods to estimate degree for
day<- 1441 #number of minutes in a day

for(d in stocks){
  
  degree_samples<- list()

  #### Next set P(s) parameters for the approriate demo/population
  m2 = m_PS[d]
  sd2 = sd_PS[d]
  min2 = min_PS[d]
  max2 = max_PS[d]
  
  ## make sure the sd makes sense for the function
  test2 <- (m2 - min2) * (max2 - m2)
  if ( sd2 >= test2){
    sd2 = test2-0.0000000001
  }
  
  #### Finally set rate parameters for the appropriate demo/pop
  m3 = m_rate[d]
  sd3 = sd_rate[d]
  min3 = min_rate[d]
  max3 = max_rate[d]
  
  ## make sure the sd makes sense for the function
  
  if (m3 < min3){
    min3 = m3-1
  }
  
  test3 <- (m3 - min3) * (max3 - m3)
  if ( sd3 >= test3){
    sd3 = test3-0.0001
  }
  
  #### Now we draw a P(a), P(s) and rate from distributions based on the above parameters
  for(i in samples){
    
    ## choose infectious period
    IP<- IP_range[[sample(1:length(IP_range), 1)]]
    
    
    #generate a random P(s)
    PS <- rgbeta(1, mean = m2, var = sd2, min = min2, max = max2)
    
    #geerate a random sync rate
    rate <-rgbeta(1, mean = m3, var = sd3, min = min3, max = max3)/average_follow_length
    
    # Now calcualte the estimated degree based on P(s), rate and the power law curve
  
    degree = round(alpha * ((IP*day*PS)*rate)^-lambda)
    degree_samples[[i]]<- degree
    
  }
  
  estimated_degrees[[d]]<- degree_samples
}

##Now write and export results as dataframe csvs
estimated_degrees_df<- as.data.frame(do.call(cbind, estimated_degrees))
colnames(estimated_degrees_df) <- c("Coastal", "Estuarine")

mean(unlist(estimated_degrees_df$Coastal))
sd(unlist(estimated_degrees_df$Coastal))
mean(unlist(estimated_degrees_df$Estuarine))
sd(unlist(estimated_degrees_df$Estuarine))

PCDP_est <- apply(estimated_degrees_df,2,as.character)

write.csv(PCDP_est, "PC_estimated_degree.csv")

PC<- read.csv('PC_estimated_degree.csv')
PC<- PC[,-c(1)]
columns<- seq(1,2, by=1)
stocks<- colnames(PC)
num_samples<- 1000
max_degree<- 30 #max the degree so we don't have issues with network generation

samples<-seq(1, num_samples, by = 1)
all_distrubutions<- list()
freq<- list()
density<- list()

for(column in columns){
  mu<- mean(unlist(PC[column]))
  var<- var(unlist(PC[column]))
  theta = var
  #theta = (mu + mu^2)/var # theta is the parameter in the neg binomial call derived from variance
  
  dist<- list()
  
  
  for( sample in samples ){
    dummy <- rnegbin(1, mu, theta = theta)
    while( dummy > max_degree){
      dummy <- rnegbin(1, mu, theta = theta)
    }
    dist[[sample]]<- dummy
  }
  
  freq[[column]]<- dist
  
  degrees <- seq(0, max_degree, by = 1)
  
  distribution <- list()
  
  for(deg in degrees){
    total <- 0
    for(d in dist) {
      if( d == deg){
        total <- total +1 
      }
    }
    distribution[[deg+1]] <- total/num_samples
  }
  all_distrubutions[[column]]<- distribution
}

##Viz  
frequency_df<- as.data.frame(do.call(cbind, freq))
colnames(frequency_df)<- stocks
df <- apply(frequency_df,2,as.character)
write.csv(df, "PC_degree_distribution.csv")

frequency_df<-lapply(frequency_df, as.numeric)
beta_df <- lapply(frequency_df,"*",0.032)

PC_freq<- frequency_df[c(1,2)]
PC_beta<- beta_df[c(1,2)]

PCCoast <- density(PC_freq$Coastal)
PCEst <- density(PC_freq$Estuarine)

PCCoast_beta <- density(PC_beta$Coastal)
PCEst_beta <- density(PC_beta$Estuarine)

plot( PCCoast, frame = FALSE, col = "#0066CC",lwd=3, main = "Chesapeake Bay Degree Distribution", xlab = "Degree", cex.axis = 1.2, cex.lab = 1.5)
lines(PCEst, col = "#006600",lwd=3,)
legend("topright", legend=c("Coastal", "Estuarine"),
       col=c("#0066CC", "#006600"),lty=1, lwd=3, cex=0.75)

mean(PC_beta$Coastal)
mean(PC_beta$Estuarine)
sd(PC_beta$Coastal)
sd(PC_beta$Estuarine)

mean(PC_freq$Coastal)
mean(PC_freq$Estuarine)
sd(PC_freq$Coastal)
sd(PC_freq$Estuarine)
