import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import logsumexp
from matplotlib import cm
import arviz as az
import pymc as pm
import scipy.stats as stats
import matplotlib as plt


# computes the log-posterior for a specific parameter value and given the data set
def log_posterior (alpha, beta, sigma, x, y):
    #log prior
    log_beta =  stats.norm.logpdf(beta, loc=0, scale=0.5)
    log_sigma = stats.halfnorm.logpdf(sigma, scale=1)
    log_prior = log_beta + log_sigma
    log_lik=0
    for i in (range(len(y))):
        log_lik = log_lik + stats.norm.logpdf(y[i], loc = alpha + beta * x[i], scale = sigma)
    return (log_beta + log_sigma + log_lik)


#draws the proposal, clipping the proposed std to 0.01
def proposal(current_beta, current_sigma):
    # we keep the variance of the proposal fixed
    s_proposal_beta =  0.1
    s_proposal_sigma = 0.1
    proposed_beta  = current_beta  + stats.norm.rvs(loc=0, scale= s_proposal_beta, size=1)[0]
    proposed_sigma = current_sigma + stats.norm.rvs(loc=0, scale= s_proposal_sigma, size=1)[0]
    while (proposed_sigma < 0):
        proposed_sigma = current_sigma + stats.norm.rvs(loc=0, scale= s_proposal_sigma, size=1)[0]
    return([proposed_beta, proposed_sigma])




babies = pd.read_csv('/Users/giorgio/bda/assignments/penguins/babies_month_length.csv')
month_obs = babies["Month"].values # x variable
length_obs = babies["Length"].values # y variable

#bivariate metropolis sampling
warmup = 1000
samples= 2000
trace = np.zeros([warmup+samples,2])
logp_trace = np.zeros([warmup+samples])



#draw initial value
alpha = 55
current_sigma = 1.5
current_beta = 0
trace[0] = [current_beta, current_sigma]
logp_trace[0] = log_posterior(alpha, current_beta, current_sigma, x=month_obs, y=length_obs) 
logp_current = logp_trace[0]
accepted = 0



#posterior pymc3 : beta	mean 1.450,	HDI:1.383	1.519
#sigma	mean:1.548	HDI:0.995	2.131

for i in range(1, warmup+samples):
    
    if i % 100 == 0:
        print(i)
    #draw proposal
    proposed_beta, proposed_sigma = proposal(current_beta, current_sigma)

    #compute  log-posterior and probability of change
    logp_proposed = log_posterior (alpha, proposed_beta,  proposed_sigma, x=month_obs, y=length_obs)
    p_change = np.min([1, np.exp(logp_proposed - logp_current)])

    if (stats.uniform.rvs() < p_change):
        accepted = accepted + 1
        trace[i] = [proposed_beta, proposed_sigma]
        logp_trace[i] = logp_proposed
        current_beta, current_sigma = proposed_beta, proposed_sigma
        logp_current = logp_proposed
    else:
        trace[i] = trace[i-1]
        logp_trace[i] = logp_trace[i-1]
        
print("proportion accepted: ", np.round(accepted/(warmup+samples),2))

#cut warmup samples
trace=trace[warmup:warmup+samples,:]
print("post mean: ", np.round(np.mean(trace, axis=0),2))

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(9, 4.5))
ax1.plot(np.arange(samples), trace[:,0])
ax1.grid()
ax1.set_ylabel('beta')

ax2.plot(np.arange(samples), trace[:,1])
ax2.grid()
ax2.set_ylabel('sigma')

fig.savefig("trace.png")
fig.show()
