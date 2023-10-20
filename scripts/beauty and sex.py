import numpy as np
import pandas as pd
import scipy.stats as stats
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns



# number of couples in the first four categories and in the fifth ("very attractive")
n_normal, n_attract = 2700, 300

# proportion of girls in the first four categories and in the fifth ("very attractive")
p_normal, p_attract = 0.48, 0.56
girl_group_normal =  int (np.round(n_normal * p_normal))
girl_group_attract = int (np.round(n_attract * p_attract))

p_pooled = ( girl_group_normal + girl_group_attract ) / (n_normal + n_attract)
se = np.sqrt( p_pooled * (1 - p_pooled) * (1/n_normal + 1/n_attract) )
z = (p_normal - p_attract) / se #-2.62

# The test declares significance even using significance as little as 0.01
z_crit = stats.norm.ppf(q=0.01) #-2.32


# Bayesian analysis
# The variation in the human sex ratio occurs in a very narrow range.
# On average the female ratio is  (49.5%).
# For example, in United States report 48.7% girls among whites and 49.2% among blacks. 
# In general, similar differences of half of a percentage point or less have been found in different studies.
# Differences larger than 0.5% are not reported in literature.
# We model the proportion of girls in the two groups as two independent beta-binomial model and eventually we
# check the posterior of the difference.
# We treat the 0.48 - 51 as a 95% interval
# the expected value is (48 + 51)/2 = 49.5
#We get a/(a+b) = 0.495, hence b = 0.495/0.505  * a = 0.98 * a
# Approximately we represent this informations using a =3000, b =3000 * 1.02.
# Our prior knowledge is equivalent to 6000 observations.
alpha = 3000
beta= alpha * 1.02
lower_0025 = stats.beta.ppf(0.025,  a=alpha, b= beta)
upper_0975 =  stats.beta.ppf(0.975, a=alpha, b= beta)

#posterior distribution of the difference of the the theta parameters
with pm.Model() as binomial_diff:
    #same prior for both groups. a priori we have no idea how the theta could
    #vary among the two groups
    theta_normal  =  pm.Beta('theta_normal',  alpha=alpha, beta=beta)
    theta_attract =  pm.Beta('theta_attract', alpha=alpha, beta=beta)
    
    #we need to write the model using the binomial likelihood
    y_normal   = pm.Binomial ('y_normal',  p=theta_normal,  observed=girl_from_normal, n=n_normal)
    y_attract  = pm.Binomial ('y_attract', p=theta_attract, observed=girl_from_attract, n=n_attract)
    
    #Difference between the two mortality rates is a deterministic variable.
    diff_theta  = pm.Deterministic('diff_theta', theta_attract - theta_normal)
    trace  = pm.sample(return_inferencedata=True)

a= az.summary(trace)
 



