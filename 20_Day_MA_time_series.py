# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 15:19:16 2019

@author: hulan
"""

import numpy as np
import pandas as pd
import csv
from math import sqrt, log, exp
import datetime as dt

df_old = pd.read_csv('adj_close_hist.csv')
#print(df_old.shape)
#print(df_old.isna().sum())
df1 = df_old.fillna(method = 'bfill')
#print(df1.isna().sum())
df1.to_csv('non_missing.csv', index=False)


def medium_term_performance(stock_column):

    A=[]
    date = []
    A_trade=[]
    A_signal= [0.0 for i in range(1744)]
    hold = []
    A_return = [0.0 for i in range(1794)]
    stock_tot_return = [0.0 for i in range(1794)]

    count_buy=0; count_sell =0;  holding =0
    with open('non_missing.csv') as f:
        reader = csv.reader(f)
                   
        for i in reader:    
            A.append(i[stock_column])  #what's changed
            date.append(i[0])  
        for j in range(1,len(A)):
            A[j]=float(A[j])
            date[j] = (dt.datetime.strptime(date[j], '%Y-%m-%d'))
            #print(date[j])
        #print(a)
        number_of_years = (date[len(date)-1] - date[1])/dt.timedelta(365)
        print('Stock', (A[0]))
        
        def moving_average(x, w):
            return (np.convolve(x, np.ones(w), 'valid') / w)
        
        ##15-day SMA
        A_15=moving_average(A[1:],15)
        
        #50-day SMA
        A_50=moving_average(A[1:],50)
        
        #create A_trade column
        for i in range(len(A_50)):
            if A_50[i] < A_15[i+35]:
                count_buy+=1
                A_trade.append(1)
            else:
                A_trade.append(-1) 
                count_sell+=1
        #print(A_trade[:10])
        #print('buy count ' ,count_buy)
        #print('sell count', count_sell)
        
        #create A_signal column 
        A_signal[0]=A_trade[0]
        for i in range(1,(len(A_trade)-1)):
            if A_trade[i] != A_trade[i-1]:
                A_signal[i]=A_trade[i]
                #print('row', i, A_signal[i])
            else:
                A_signal[i]= 0.0
                #print('row', i, A_signal[i])
            
            
        #create an array of Stock Price, A_trade based on logic, Trade Signal when it swithes
        A_frame = np.full((len(A),4),0.0,'f')
    
        for i in range(1,len(A)):
            A_frame[i][0] = A[i]
        for i in range(0, len(A_trade)):
            A_frame[i+50][1] = A_trade[i]
            A_frame[i+50][2] = A_signal[i]
            
        #calculate return
        if A_signal[0]==1:
            for i in range(1,len(A)):     
                if (A_frame[i][1]==1 and A_frame[i-1][1]==1):
                    #print(' i is ', i, '...',A_frame[i][0], '   ... ', A_frame[i-1][0])
                    A_return[i]= log((A_frame[i][0])/(A_frame[i-1][0]))
                    #print('return ', A_return[i])
                    
                if (A_frame[i][1]==1 and A_frame[i-1][1] ==-1):
                    A_return[i] = 0
                    #print('return is   ',A_return[i])
                    
                if (A_frame[i][1]==-1 and A_frame[i-1][1]==1) :
                    A_return[i]= log((A_frame[i][0])/(A_frame[i-1][0]))
                
                if (A_frame[i][1]==-1 and A_frame[i-1][1]== -1):
                    A_return[i] = 0
                    
                    
        if A_signal[0]== -1:
            for i in range(1,len(A)):     
                if (A_frame[i][1]==-1 and A_frame[i-1][1]==-1):
                    A_return[i]= log((A_frame[i][0])/(A_frame[i-1][0]))
                    
                if (A_frame[i][1]==-1 and A_frame[i-1][1]== 1):
                    A_return[i] = 0
                    
                if (A_frame[i][1]==1 and A_frame[i-1][1]==-1) :
                    A_return[i]= log((A_frame[i][0])/(A_frame[i-1][0]))
                
                if (A_frame[i][1]==1 and A_frame[i-1][1]== 1):
                    A_return[i] = 0

    
        def annulized_geo_return(list):
            b = np.array(A_return)
            geo_r = 1+b
            prod = np.prod(geo_r)
            return prod**(252/(len(A_return)-15))
        print ('annulized geometric return is ', '{0:.2%}'.format(annulized_geo_return(A_return)-1))
        


         #invest $1000 to begin with 
        def stock_8_year_return():
            stock_tot_return[6]= 1000 * (1+A_return[6])
            
            for i in range(7, 1794):
                stock_tot_return[i]=stock_tot_return[i-1]*(1+A_return[i])
                #print("stock_return", stock_tot_return[i])
            return ((stock_tot_return[1793]-stock_tot_return[6])/stock_tot_return[6])/8
        
        #print('stock 7 year return /8 is ', '{0:.2%}'.format(stock_8_year_return()))
        



        
        def annulized_vol(list):
            c = np.array(A_return)
            return np.std(c)*sqrt(252)
        #print('SD of return is', np.std(np.array(A_return)))
        print('annulized_volatility is', '{0:.2%}'.format(annulized_vol(A_return))  )
        
        #holding period
        for i in range(len(A_50)-1):
            if A_trade[i] ==1:
                holding = holding +1
    
            if A_trade[i] ==-1:
                hold.append(holding)
                holding =0
    
        h = np.array(hold)
        average = h[np.nonzero(h)].mean()
        print('average holding period is ', round(average,2))
    
        #average position turn-over per annum 
        turn_over_c =0
        for i in range(len(A_50)):
            if A_frame[i][2] == -1:
                turn_over_c += 1
        print ('average position turn over per annum is ', round( turn_over_c / number_of_years, 2) )
    

    return stock_8_year_return()

port_return = []
for i in range(1,9):
    port_return.append(medium_term_performance(i))
    print('\n')

#print(port_return)

b = np.array(port_return)
c = np.sum(b+1)
d= np.prod(c)
final = d**(1/8)-1

print("Final Portfolio return is", '{0:.2%}'.format(final))

    