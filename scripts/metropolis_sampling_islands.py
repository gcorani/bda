#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 20:47:09 2022

@author: giorgio
"""
import numpy as np
import pandas as pd

# returns the next position, deciding between moving left or right
# it is necessary checking to stay within the bounds (1,7)
def get_next_position( proposal, current_position ):
    next_position = current_position
    if np.random.uniform() < np.min( np.concat([ [1], (proposal/current_position).flatten() ])) :
            next_position = proposal
    return (next_position)

samples = 50000

position = np.ones([samples,1])
start = 3
position[0] = start

for i in range(1,samples):
    # initialize the proposal to the right, remaining within the allowed bounds
    proposal = min(position[i-1]+1,7)

    #change to left with probability 50% (avoiding negative values)
    if  np.random.uniform()<0.5: 
        proposal = max(position[i-1]-1,1)
    
    position[i] = get_next_position( proposal, position[i-1])
    
    
df = pd.DataFrame(position, columns=["position"])
#frequency of each visit
freqs = pd.crosstab(index=df['position'],columns=df['position'], margins=True)["All"][0:7]

#compare sampled and actual distribution
empirical_p = freqs / sum(freqs)
true_p = pd.Series(range(1,8)/np.sum(range(1,8)), index=empirical_p.index)
results = pd.concat([true_p, empirical_p], axis=1)

#this data frame compares the sampled and the actual distribution
# if you want a better fit, increase the number of samples
results = results.rename(columns={0: 'actual_distribution', 'All': 'sampled_distribution'})
