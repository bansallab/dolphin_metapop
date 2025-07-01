
data {
int<lower = 0> N;
int<lower = 0> max_U;
int<lower = 0> max_U_plus_one;
int<lower = 0> T;
int<lower = 0> U[N];
int<lower = 0> state[N, max_U];
real<lower = 0> delta[N, max_U_plus_one];

matrix[1, 4] f;
matrix[4, 1] ones;
 }

parameters {
 real<lower=0> eta12;
 real<lower = 0> eta23;
 real<lower = 0> eta34;
 real<lower=0> mu[4];
 }

transformed parameters {
 matrix[4, 4] Q = rep_matrix(0, 4, 4);
 vector[4] lambda = rep_vector(0, 4);

 // Detection rates (live states)
 lambda[1] = mu[1];
 lambda[2] = mu[2];
 lambda[3] = mu[3];
 lambda[4] = mu[4];

 // transition rate matrix
 Q[1, 1] <- -(eta12);
 Q[1, 2] <- eta12;
 Q[2, 1] <- eta12;
 Q[2, 2] <- -(eta12 + eta23);
 Q[2, 3] <- eta23;
 Q[3, 2] <- eta23;
 Q[3, 3] <- -(eta23+eta34);
 Q[3, 4] <- eta34;
 Q[4, 3] <- eta34;
 Q[4, 4] <- -eta34;
 
 }

model {
 matrix[1, 4] acc;
 matrix[4, 4] Gamma;

 // Priors
 eta12 ~ gamma(1, 4);
 eta23 ~ gamma(1, 4);
 eta34 ~ gamma(1, 4);
 mu ~ gamma(1, 4);

 // Likelihood
 for(i in 1:N) {
  matrix[4, 4] Omega[U[i] + 1];
  if(U[i] > 0){
  for(j in 1:U[i]){
  Gamma = diag_post_multiply(matrix_exp((Q - diag_matrix(lambda)) * delta[i, j]), lambda);
  Omega[j] = rep_matrix(0, 4, 4);
  if(j == 1){
  Omega[j, 1, state[i, j]] = Gamma[1, state[i, j]];
  }else{
  Omega[j, state[i, j - 1], state[i, j]] = Gamma[state[i, j - 1], state[i, j]];
  }
  } // j

 // last det to T
 Gamma = matrix_exp((Q - diag_matrix(lambda)) * delta[i, U[i] + 1]);


 Omega[U[i] + 1] = rep_matrix(0, 4, 4);
 Omega[U[i] + 1, state[i, U[i]], state[i, U[i]]:4] = Gamma[state[i, U[i]], state[i,U[i]]:4];

 // Calculate likelihood of individual i
 acc = f * Omega[1];
 for(j in 2:(U[i] + 1)){
 acc *= Omega[j];
 }
 target += log(acc * ones);

 }else{
 // Never detected
 Gamma = matrix_exp((Q - diag_matrix(lambda)) * T);

 Omega[1] = rep_matrix(0, 4, 4);
 Omega[1, 1, 1:4] = Gamma[1, 1:4];

 target += log(f * Omega[1] * ones);
 }
 } // i
 }
 
