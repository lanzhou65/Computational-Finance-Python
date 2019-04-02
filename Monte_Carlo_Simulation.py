# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 12:57:58 2019

@author: hulan
"""
import time
import random
import statistics
import numpy as np
from scipy.stats import norm 
from math import sqrt, pi, log, exp
import bs_options as bs

random.seed(100)

S, tau, vol, r, d = 100, 0.5, 0.5, 0, 0
mu, sigma, disc = (r-d-0.5*vol*vol)*tau, vol*sqrt(tau), exp(-r*tau)
#monte-carlo simulation 
stock_prices = [S*random.lognormvariate(mu, sigma) for i in range(100000)]

#print(stock_prices[:30])
def call_payoff(S, K):
    return lambda S: (S-K) if S > K else 0

def put_payoff(S, K):
    return lambda S: (K-S) if S < K else 0

print('call price is', statistics.mean(map(call_payoff(S,100), stock_prices))*disc,)
print('call struck at 110', statistics.mean(map(call_payoff(S,110), stock_prices))*disc,'\n')
print('put price is', statistics.mean(map(put_payoff(S,100), stock_prices))*disc)
print('put struck at 90', statistics.mean(map(put_payoff(S,90), stock_prices))*disc,'\n')

C1 = bs.EquityOption(1, 100, 100, 0.5, 0)
C2 = bs.EquityOption(1, 100, 110, 0.5, 0)
print('C1 from BS model ', C1.BS_Option(), 'C2  from BS model ', C2.BS_Option())
P1 = bs.EquityOption(0, 100, 100, 0.5, 0)
P2 = bs.EquityOption(0, 100, 90, 0.5, 0)
print('P1  from BS model ', P1.BS_Option(), 'P2  from BS model ', P2.BS_Option(),'\n')


def call_payo(S,K):
    return (S-K) if S > K else 0
def put_payo (S, K):
    return (K-S) if S < K else 0

def Put_Greeks(S, K, S_inc, vol_inc, num):
    put_delta =[]
    put_gamma =[]
    put_vega = []
    for i in range (num):
        mu1 = (r-d-0.5*(vol+ vol_inc)*(vol+vol_inc))*tau
        sigma1 = (vol+vol_inc)*sqrt(tau)
        rand = random.lognormvariate(mu, sigma)
        rand_1 =random.lognormvariate(mu1, sigma1)
        
        stock_1 = S*rand_1 #for vol
        stock_up = (S+ S_inc)*rand
        stock = S*rand
        stock_down = (S- S_inc)*rand
        
        put_delta.append((put_payo(stock_up, K) - put_payo(stock, K))/S_inc)
        put_gamma.append((put_payo(stock_up, K) - 2*put_payo(stock, K) + put_payo(stock_down, K))/(S_inc*S_inc))
        put_vega.append((put_payo(stock_1, K) - put_payo(stock,K))/vol_inc)
        
    print('put______delta', statistics.mean(put_delta))
    print('put______gamma', statistics.mean(put_gamma))
    print('put______vega', statistics.mean(put_vega))

def Call_Greeks(S, K, S_inc, vol_inc, num):
    call_delta = []
    call_gamma = []
    call_vega = []
    for i in range(num):
        mu1 = (r-d-0.5*(vol+ vol_inc)*(vol+vol_inc))*tau
        sigma1 = (vol+vol_inc)*sqrt(tau)
        
        rand = random.lognormvariate(mu, sigma)
        rand_1 =random.lognormvariate(mu1, sigma1)
        
        stock_1 = S*rand_1 #for vol
        stock_up = (S+ S_inc)*rand
        stock = S*rand
        stock_down = (S- S_inc)*rand
        
        call_delta.append((call_payo(stock_up, K) - call_payo(stock, K))/S_inc)
        call_gamma.append((call_payo(stock_up, K) - 2*call_payo(stock, K) + call_payo(stock_down, K))/(S_inc*S_inc))
        call_vega.append((call_payo(stock_1, K) - call_payo(stock, K))/vol_inc)
        
    print('call______delta', statistics.mean(call_delta))
    print('call______gamma', statistics.mean(call_gamma))
    print('call______vega', statistics.mean(call_vega))

print('ATM Call')
Call_Greeks(100, 100, 0.01, 0.1, 1000000)

print('\nC1 Check')
print('delta', C1.delta())
print('gamma', C1.gamma())
print('vega', C1.vega(), '\n\n')
##
print('Call struck at 110')
Call_Greeks(100, 110, 0.01, 0.1, 1000000)

print('\nC2 Check')
print('delta', C2.delta())
print('gamma', C2.gamma())
print('vega', C2.vega(), '\n\n')


print('ATM Put')
Put_Greeks(100, 100, 0.01, 0.1, 1000000)

print('\nP1 Check')
print('P1 delta ', P1.delta())
print('P1 gamma', P1.gamma())
print('P1 vega', P1.vega(), '\n\n')

print('Put struck at 90')
Put_Greeks(100, 90, 0.01, 0.1, 1000000)

print('\nP2 Check')
print('P2 delta ', P2.delta())
print('P2 gamma', P2.gamma())
print('P2 vega', P2.vega(), '\n\n')









