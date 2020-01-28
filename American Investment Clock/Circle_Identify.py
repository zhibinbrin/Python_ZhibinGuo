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
    eco=D['产出缺口']
    cpi=D['CPI同比']
    eco_s=D['产出缺口']-D['产出缺口'].shift(1)
    cpi_s=D['CPI同比']-D['CPI同比'].shift(1)
    eco_signal=np.sign(eco_s*eco_s.shift(1))# 1: trend no change; -1: trend change
    cpi_signal=np.sign(cpi_s*cpi_s.shift(1))# 1: trend no change; -1: trend change
    eco_pos=eco_signal[eco_signal==-1].index.tolist()  #the position where the gdp trend changes  
    cpi_pos=cpi_signal[cpi_signal==-1].index.tolist()  #the position where the cpi trend changes
    change=set(cpi_pos+eco_pos) 
    change=list(change)# the index where the change happened
    change.sort()
    circle_type=[]#record the type of the circle 0: recovery, 1:overheat, 2:stagflation, 3:decline
    for pos in range(0,len(change)):
        compare=D.iloc[change[pos]][0:3]-D.iloc[change[pos]-1][0:3] 
        if (change[pos] in eco_pos and change[pos] in cpi_pos ):#both the gdp & cpi trend change
            if ((compare['产出缺口']<0)&(compare['CPI同比']<0)): #later the gdp grows, cpi grows, overheat:1 
                circle_type.append(1) #recording the circle type of the next period
            elif((compare['产出缺口']<0)&(compare['CPI同比']>0)):#later the gdp grows, cpi decrease, recovery:0
                circle_type.append(0)
            elif((compare['产出缺口']>0)&(compare['CPI同比']>0)):#later the gdp decrease, cpi deccrease,decline:3 
                circle_type.append(3)
            else:
                circle_type.append(2) #later the gdp decrease, cpi grows, stagflation: 2
        else:#single signal trend change
            if change[pos] in eco_pos: #gdp trend change, cpi trend stays
                if ((compare['产出缺口']<0)&(compare['CPI同比']<0)): #later the gdp grows, cpi decrease, recovery:0 
                    circle_type.append(0) #recording the circle type of the next period
                elif((compare['产出缺口']<0)&(compare['CPI同比']>0)):#later the gdp grows, cpi grows, overheat:1 
                    circle_type.append(1)
                elif((compare['产出缺口']>0)&(compare['CPI同比']>0)):#later the gdp decrease, cpi grows,stagflation: 2 
                    circle_type.append(2)
                else:
                    circle_type.append(3) #later the gdp decrease, cpi grows, decline:3
            else: #cpi treend change
                if ((compare['产出缺口']<0)&(compare['CPI同比']<0)): #later the gdp decreases, cpi grows,stagflation: 2  
                    circle_type.append(2) #recording the circle type of the next period
                elif((compare['产出缺口']<0)&(compare['CPI同比']>0)):#later the gdp decreases, cpi decreases,decline:3 
                    circle_type.append(3)
                elif((compare['产出缺口']>0)&(compare['CPI同比']>0)):#later the gdp grows, cpi decreases,recovery: 0
                    circle_type.append(0)
                else:
                    circle_type.append(1) #later the gdp grows, cpi grows, overheat:1     
    return [change,circle_type]
