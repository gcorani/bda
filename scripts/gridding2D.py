#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 20:47:09 2022

@author: giorgio
"""
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.stats import halfnorm
import matplotlib.pyplot as plt
#exercise: implement the posterior of the height model, by using a 2-d gridding.
#𝜇 ∼ 𝑁(175,5)
#𝜎 ∼ half-normal(35) 
# y ∼ 𝑁(𝜇, 𝜎)
#assume that two measures are available: 168 and 178 cm.

#we consider a grid of +- 6 prior sigma, hence +-30.
#to keep the computation fast, we use only 80 points.
mu = np.linspace(145, 205, 80)

#the sigma has a broad range (see slides: 75% pctile is 40; max is 128 and we use more points)
sigma = np.linspace(0, 100, 120)

post_density = np.zeros( ( len(mu),len(sigma) ) ) 

#we could vectorize the code. But here we aim at clarity.
for row, current_mu in enumerate(mu):
  for col, current_sigma in enumerate(sigma):
    #prior: prior(current_mu) * density(current_sigma)
    # we assume the priors p(mu) and p(sigma) to be independent
    prior = norm.pdf(current_mu, loc=175, scale=5)
    prior = prior * halfnorm.pdf(current_sigma, scale=35)
    
    #assuming independence of the y_i, the lik terms multiply
    lik   = norm.pdf(168, loc=current_mu, scale=current_sigma)
    #lik   = lik * norm.pdf(178, loc=current_mu, scale=current_sigma)
    
    #unnormalized density
    post_density[row,col] = prior * lik

#numbers are small and numerically problem can arise. 
#use the log to have a more robust computation
post_density = post_density/sum(post_density)
plt.matshow(post_density)
plt.xticks(mu)
plt.yticks(sigma)
plt.show()

#posterior marginal of mu
post_mu = np.sum(post_density, axis=1)
post_sigma = np.sum(post_density, axis=0)

plt.plot(mu,post_mu)
plt.show()
