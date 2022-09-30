#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 08:53:52 2022

@author: giorgio
"""
#   Calculate the prior mean, mode, standard deviation of Beta(8,2) prior. 
#and Beta(1,20) prior.

  
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
a=8
b=2
x = np.linspace(0, 1, 100)

#show likelihood function
y = 