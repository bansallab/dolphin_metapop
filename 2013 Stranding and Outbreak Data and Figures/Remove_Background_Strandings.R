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
library(dplyr)
library(ggsignif)



### To get from stranding data
#1. The prop of known individuals 
full_data_UME<- read.csv("2010-2013_Stranding_Data.csv")
full_data_preUME <- read.csv('2013-2015_Stranding_Data.csv')
 
##For UME (unusual mortality event, during the epidemic)
full_data_UME$Lat<- round(full_data_UME$Latitude)
UME_lat<- as.data.frame(table(full_data_UME$Lat))
colnames(UME_lat) = c("Lat", "Strandings")
lat_ume<- glm(Strandings ~Lat, family=poisson, data = UME_lat)

simulationOutput_min <- simulateResiduals(fittedModel = lat_ume)
#testDispersion(simulationOutput_min) #test fit and dispersion
plot(allEffects(lat_ume)) 
eff <- effects::effect("Lat", lat_ume)
UME_eff <- as.data.frame(eff)
UME_eff


##From before the UME
full_data_preUME$Lat<- round(full_data_preUME$Latitude)
full_data_preUME$Year<- as.Date(full_data_preUME$Observation.Date, format = "%Y-%m-%d")
full_data_preUME$Year<-lubridate::year(full_data_preUME$Year)
full_data_preUME$Year<- as.factor(full_data_preUME$Year)
preUME_lat<- as.data.frame(table(full_data_preUME$Lat, full_data_preUME$Year))
colnames(preUME_lat) = c("Lat", "Year", "Strandings")
lat_preume<- glm(Strandings ~Lat*Year, family=poisson, data = preUME_lat)

simulationOutput_min <- simulateResiduals(fittedModel = lat_preume)
#testDispersion(simulationOutput_min) #test fit and dispersion
plot(allEffects(lat_preume)) 

eff <- effects::effect("Lat*Year", lat_preume)
preUME_eff <- as.data.frame(eff)
preUME_eff

############### Now we use the model estimates and generate UME stradnings data correcting
############### for background strandings 

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

total_UME_strandings <- nrow(full_data_UME)

## Get rate of strandings for each age groups per month (based on Morris et al)
time_period = 12 # 12 months per year

lats<- c(31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41)

pre_numbers = list()

i = 1
for(lat in lats){
  sub <- subset(preUME_eff, preUME_eff$Lat== lat)
  strands = ifelse(nrow(sub) == 0, 0, mean(sub$fit))
  pre_numbers[[i]]<- strands
  i = i+1
}

pre_strandings = unlist(pre_numbers)
ume_strandings = unlist(UME_eff$fit)

##According to Morris et al, the prob that a UME stranding is disease strandings is background rate/UME rate
probs = list()

i = 1
for(lat in lats){
  excess = abs(ume_strandings[i]-pre_strandings[i])
  prob = excess/ume_strandings[i]
  probs[[i]]<- prob
  i = i+1
}



dropped_rows<- list()
for (row in 1:nrow(full_data_UME)){
    
    lat<- full_data_UME[row, "Lat"]
    chance = runif(1)
    
    if( lat == 31){
      prob = probs[1]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 32){
      prob = probs[2]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 33){
      prob = probs[3]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 34){
      prob = probs[4]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 35){
      prob = probs[5]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 36){
      prob = probs[6]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 37){
      prob = probs[7]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 38){
      prob = probs[8]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 39){
      prob = probs[9]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 40){
      prob = probs[10]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
    if( lat == 41){
      prob = probs[11]
      if(chance > prob){
        dropped_rows<-append(dropped_rows, row)
      }
    }
    
  }
  
Disease_data <-full_data_UME[-unlist(dropped_rows), ]  

write.csv(Disease_data, "2013-2015_Final_Outbreak_Data.csv")
