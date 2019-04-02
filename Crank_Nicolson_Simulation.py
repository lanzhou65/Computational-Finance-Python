# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:37:22 2019

@author: Lan
"""

import numpy as np
import bs_option4 as bs
import matplotlib.pyplot as plt
#%matplotlib inline
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')

class Crank_Nicolson: 
    
    def __init__(self, *args):
        self.AmericanEuropean = str(args[0])
        self.CallFlag = int(args[1])
        self.S0 = float(args[2])
        self.K = float(args[3])
        self.T = float(args[4])
        self.vol = float(args[5])
        self.r = float(args[6]) 
        self.d = float(args[7])
    
    def __str__(self):
        call_put = 'Call' if self.CallFlag else 'Put'
        str_output = '__str__ is called.' + "It's a "+ self.AmericanEuropean +' '+ call_put +' option. Spot ='+\
        str(self.S0) + ', Strike='+ str(self.K) +', Maturity ='+str(self.T)+', Dividend = '+str(self.d)\
        +', volatility ='+ str(self.vol) +', riskfree is '+str(self.r) + '\n'
        return str_output
    
    
    def Option_Payoff(self, S = None, T = None):
        
        if S is None:
            S = self.S0
        if T is None:
            T = self.T
        
        mu = self.r-self.d-0.5*self.vol*self.vol
        x_max = self.vol*np.sqrt(T)*5
        #number of steps along stock 
        N = 500
        dx = 2*x_max/N
        # grid along stock dimension:
        X = np.linspace(-x_max, x_max,N+1)  #an array 
        #n = np.arange(0,N+1)  #an array
        J = 500 #number of time steps
        dt = T/J #scaler 
        # grid along time dimension:
        #Tau = np.arange(J)*dt #array
        #print(S, self.K, T, self.vol, dx, dt)
        
        pd = 0.25*dt/dx*(self.vol*self.vol/dx - mu)
        pu = 0.25*dt/dx*(self.vol*self.vol/dx + mu)
        pc = 1- dt*self.r - (self.vol*self.vol*dt/2/dx/dx)
        pcc = 1 + self.vol*self.vol*dt/2/dx/dx 

        A = np.eye(N+1, k=0)*pcc + np.eye(N+1, k=1)*(-pu) + np.eye(N+1, k=-1)*(-pd)
        B = np.eye(N+1, k=0)*pc + np.eye(N+1, k=1)*pu + np.eye(N+1, k=-1)*pd
        cut = int(N/4)
        n_mid = int(N/2)
        
        if (self.AmericanEuropean=='European') and (self.CallFlag==1):
            bs_c = bs.EquityOption(self.CallFlag, S, self.K, T, self.d)
            bs_c.setRiskFree(self.r)
            #print(bs_c)
            
            V = np.clip(S*np.exp(X)-self.K,0,1e10)
            for j in range(J):
                V[0] = 0
                V=np.linalg.inv(A).dot(B).dot(V)
                V[N] = S*np.exp(x_max) - self.K*np.exp(-self.r*j*dt)
                if j%50==0: plt.plot(S*np.exp(X[cut:-cut]), V[cut:-cut])
                
            print ('bs_price is {}, Crank Nicolson price is {}'.format(bs_c.BS_Option(),V[n_mid]))
            return V[n_mid]
                
        if (self.AmericanEuropean =='European') and (self.CallFlag==0):
            bs_p = bs.EquityOption(self.CallFlag, S, self.K, T, self.d)
            bs_p.setRiskFree(self.r)
            #print(bs_p)
            
            V = np.clip(self.K -S*np.exp(X),0,1e10)
            
            for j in range(J):
                V[0] = self.K*np.exp(-self.r*j*dt)-S*np.exp(x_max)
                V=np.linalg.inv(A).dot(B).dot(V)
                V[N] = 0
                if j%50==0: plt.plot(S*np.exp(X[cut:-cut]), V[cut:-cut])
                
            print ('bs_price is {}, Crank Nicolson price is {}'.format(bs_p.BS_Option(),V[n_mid]))
            return V[n_mid]   
                
                
        if (self.AmericanEuropean=='American') and (self.CallFlag==1):
            V0 = np.clip(S*np.exp(X)-self.K,0,1e10) #V0 is an array, not exercise price 
            V_ac = V0.copy()  #make V_ac = V0
            
            for j in range(J):
                V_ac = np.linalg.inv(A).dot(B).dot(V_ac)
                V_ac = np.where (V_ac<V0, V0, V_ac) #V_ac is the price to exercise at previous time 
                
                V_ac[0] = 0
                V_ac[N] = S*np.exp(x_max) - self.K*np.exp(-self.r*j*dt)
                if j%50==0: plt.plot(S*np.exp(X[cut:-cut]), V_ac[cut:-cut])
            print ('Crank Nicolson price is {}'.format(V_ac[n_mid]))
            return V_ac[n_mid]
             
        if (self.AmericanEuropean=='American') and (self.CallFlag ==0):
            V0 = np.clip(self.K-S*np.exp(X),0,1e10) #V0 is an array, not exercise 
            V_ap = V0.copy()  #make V_ac = V0
            
            for j in range(J):
                V_ap = np.linalg.inv(A).dot(B).dot(V_ap)
                V_ap = np.where (V_ap<V0, V0, V_ap) #V_ac is exercise previous time 
                
                V_ap[0] = 0
                V_ap[N] = self.K*np.exp(-self.r*j*dt) - S*np.exp(x_max)
                if j%50==0: plt.plot(S*np.exp(X[cut:-cut]), V_ap[cut:-cut])
            print ('Crank Nicolson price is {}'.format(V_ap[n_mid]))
            return V_ap[n_mid]   
                
           
    
    def bs_greeks(self):
        bs_test= bs.EquityOption(self.CallFlag, self.S0, self.K, self.T, self.d)
        bs_test.setRiskFree(self.r)
        print('bs delta is {}'.format(bs_test.delta()))
        print('bs gamma is {}'.format(bs_test.gamma()))
        print('bs theta is {}'.format(bs_test.theta()))
        
    def greeks(self):
        N = 100
        #x_max = self.vol*np.sqrt(self.T)*5
        #dx = 2*x_max/N
        dx = self.S0/N
       
        J = 100 #number of time steps
        dt = self.T/J  
        
        V_n1_j1 = self.Option_Payoff(self.S0+dx, self.T+dt)        
        V_n1_j = self.Option_Payoff(self.S0+dx, self.T)
        V_n_1_j1 = self.Option_Payoff(self.S0-dx, self.T+dt)
        V_n_1_j = self.Option_Payoff(self.S0-dx, self.T)
        V_n_j = self.Option_Payoff(self.S0, self.T)
        V_n_j1 = self.Option_Payoff(self.S0, self.T+dt)
        
        delta = (V_n1_j1 - V_n_1_j1 + V_n1_j - V_n_1_j)/(4*dx)
        gamma = ((V_n1_j1 -2*V_n_j1 + V_n_1_j1) + (V_n1_j -2*V_n_j + V_n_1_j))/(2*dx*dx)
        theta = (V_n_j -V_n_j1)/dt
        
        #print('s0 {} T {}'.format(self.S0, self.T))
        print('the delta is {}, the gamma is {}, the theta is {}'.format(delta, gamma, theta))
        return delta, gamma, theta

c_e = Crank_Nicolson('European', 1, 90, 100, 1, 0.3, 0.01, 0.15)
print('European Call Option Premium is {}'.format(c_e.Option_Payoff()))
print(c_e.bs_greeks())
print(c_e.greeks(), '\n')

p_e = Crank_Nicolson('European', 0, 110, 100, 1, 0.3, 0.05, 0.)
print('European Put Option Premium is {}'.format(p_e.Option_Payoff()))
print(p_e.bs_greeks())
print(p_e.greeks(),'\n')

c_a = Crank_Nicolson('American', 1, 90, 100, 1, 0.3, 0.01, 0.15)
print('American Call Option Premium is {}'.format(c_a.Option_Payoff()))
print(c_a.greeks(),'\n')


p_a = Crank_Nicolson('American', 0, 110, 100, 1, 0.3, 0.05, 0.)
print('American Put Option Premium is {}'.format(p_a.Option_Payoff()))
print(p_a.greeks(),'\n')       
                
                
        
