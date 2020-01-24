#!/usr/bin/env python
# coding: utf-8

# <font face="黑体" size=4 color=#8B0000> 美林时钟周期的划分 </font>
2
# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[17]:


def Circle_Identify(D):
    #The function is to identify the circle in American Investment Clock Model
    #D is DataFrame
    eco=D['经济同比趋势']
    cpi=D['CPI同比趋势']
    eco_s=D['经济同比趋势']-D['经济同比趋势'].shift(1)
    cpi_s=D['CPI同比趋势']-D['CPI同比趋势'].shift(1)
    eco_signal=np.sign(eco_s*eco_s.shift(1))# 1: trend no change; -1: trend change
    cpi_signal=np.sign(cpi_s*cpi_s.shift(1))# 1: trend no change; -1: trend change
    eco_pos=eco_signal[eco_signal==-1].index.tolist()
    cpi_pos=cpi_signal[cpi_signal==-1].index.tolist()
    change=set(cpi_pos+eco_pos)
    change=list(change)# the index where the change happened
    change.sort()
    circle_type=[]#record the type of the circle 0: recovery, 1:overheat, 2:stagflation, 3:decline
    for pos in range(0,len(change)):
        compare=D.iloc[change[pos]][1:3]-D.iloc[change[pos]-1][1:3]
        if ((compare['经济同比趋势']<0)&(compare['CPI同比趋势']<0)): 
            circle_type.append(1) #recording the circle type of the next period
        elif((compare['经济同比趋势']<0)&(compare['CPI同比趋势']>0)):
            circle_type.append(0)
        elif((compare['经济同比趋势']>0)&(compare['CPI同比趋势']>0)):
            circle_type.append(3)
        else:
            circle_type.append(2)
    return [change,circle_type]
