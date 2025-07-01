library(expm)
library(rstan)
library(shinystan)
library(dplyr)
library(tidyr)
library(faux)

# import necessary data
deltaE <-read.csv("delta4_Estmovers.csv", header = FALSE)
deltaC<- read.csv("delta4_Coastals.csv", header = FALSE)

deltaE[is.na(deltaE)] <- 0
deltaC[is.na(deltaC)] <- 0

deltaE<-as.matrix(deltaE)
deltaC<-as.matrix(deltaC)

mode(deltaE) <- "numeric"
mode(deltaC) <- "numeric"

stateE<- read.csv("state4_Estmovers.csv", header = FALSE)
stateC<- read.csv("state4_Coastals.csv", header = FALSE)

stateE<- as.matrix(stateE)
stateC<- as.matrix(stateC)

UE<- as.list(read.csv("U4_Estmovers.csv"), header = FALSE)
UC<- as.list(read.csv("U4_Coastals.csv"), header = FALSE)

UE<- unlist(UE[2])
UC<- unlist(UC[2])

# sample size for coastal (NC) and estuarine movers (NE)
NE = 220
NC = 29

#study length is one year
T = 365

#### set up data for the coastal and estuarine runs
stan_dataE <- list(N = NE,
                  T = T,
                  delta = deltaE,
                  state = stateE,
                  max_U = max(UE),
                  max_U_plus_one = max(UE) + 1,
                  U = UE,
                  f = matrix(c(0.1, 0.3, 0.3, 0.3), 1, 4),
                  ones = matrix(c(1,1,1,1), 4, 1))

stan_dataC <- list(N = NC,
                   T = T,
                   delta = deltaC,
                   state = stateC,
                   max_U = max(UC),
                   max_U_plus_one = max(UC) + 1,
                   U = UC,
                   f = matrix(c(0.25, 0.25, 0.25, 0.25), 1, 4),
                   ones = matrix(c(1,1,1,1), 4, 1))

# Initial values
initf1 <- function() {
  list(eta12 = 0.01,eta23 = 0.01,eta34 = 0.01, mu = runif(4, 0.1,0.1))
}

# Fit the model, uncomment for line coastal and estuarine seperately depending on run
fit <- stan(file = "stan/four_state_dot.stan",
            pars = c("eta12", "eta23","eta34", "mu"),
            data = stan_dataE,
           # data = stan_dataC,
            init = initf1,
            warmup = 200,
            iter = 500,
            chains = 4,
            cores = 1,
            thin = 1)

print(fit, digits = 4)

