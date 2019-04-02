# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 17:32:33 2019

@author: hulan
"""
import datetime as dt
import csv
from collections import defaultdict

d = [dt.date(2019, i, 1) for i in range(1,13) ] 
d_fri = [ [] for _ in range(len(d))]
print("Question_1: 3rd Friday of the Month in 2019 \n")
#Sundy is 0 
for i in range(len(d)): 
    if d[i].isoweekday() == 6 : 
       d_fri[i] =d[i]+dt.timedelta(21 - (7-d[i].isoweekday()))
       print(d_fri[i]) 
    
    elif d[i].isoweekday() == 7:
        d_fri[i] =d[i]+dt.timedelta(19)
        print(d_fri[i])
       
    # <=5
    else: 
        d_fri[i] =d[i]+dt.timedelta(15+4-d[i].isoweekday())
        print(d_fri[i])

oneyear = dt.date(2018,1,1)-dt.date(2017,1,1); 
time_to_M = [(d_fri[i] - dt.date(2019,1,1))/oneyear for i in range (12)]; 
print("time to maturity' as fraction of a year \n",time_to_M)

print("\nQuestion 2 \n")
with open('stockPx.csv', newline ='') as csvfile:
    reader = csv.DictReader(csvfile)
#    row_list = list(reader)
#    row_num = len(row_list)
#    print(row_num)

    max_FB = ['FB', 0, 0]; max_GOOG = ['GOOG', 0,0]; max_IBM = ['IBM', 0,0];
    min_FB= ['FB', 0, 2000]; min_GOOG =['GOOG', 0,2000]; min_IBM =['IBM', 0, 2000];
    for row in reader: 
        row['date'] =dt.datetime.strptime(row['date'], '%m/%d/%Y')
        row['FB'] = float(row['FB'])
        row['GOOG'] = float(row['GOOG'])
        row['IBM'] = float(row['IBM'])
        #print(row.items())
        #print(row.values())
        if row['FB'] > max_FB[2]:
            max_FB[1] = row['date']
            max_FB[2] = row['FB']            
        if row['GOOG'] > max_GOOG[2]:
            max_GOOG[1] = row['date']
            max_GOOG[2] = row['GOOG']            
        if row['IBM'] > max_IBM[2]:
            max_IBM[1] = row['date']
            max_IBM[2] = row ['IBM']
            
        if row['FB'] < min_FB[2]:
            min_FB[1] = row['date']
            min_FB[2] = row['FB']
        if row['GOOG'] < min_GOOG[2]:
            min_GOOG[1] = row['date']
            min_GOOG[2] = row['GOOG']
        if row['IBM'] < min_IBM[2]:
            min_IBM[1] = row['date']
            min_IBM[2] = row['IBM']

    print('max and min of FB is', max_FB, min_FB)
    print('max and min of GOOG is', max_GOOG, min_GOOG)
    print('max and min of IBM is', max_IBM, min_IBM,'\n')
    
    diff_FB = ['FB', max_FB[1] - min_FB[1]]
    diff_GOOG = ['GOOG', max_GOOG[1]- min_GOOG[1]]
    diff_IBM = ['IBM', max_IBM[1]-min_IBM[1]]

    s = [max_FB[:2], min_FB[:2], diff_FB, max_GOOG[:2], min_GOOG[:2], diff_GOOG, max_IBM[:2], min_IBM[:2], diff_IBM]
    d = defaultdict(list)
    for k, v in s:
        d[k].append(v)
    print('day of max, day of min, number of days between max and min\n', d)
           
    
    
    
    
    
    

            
            
            
            
            
            
            
            
            
            
            
            
            