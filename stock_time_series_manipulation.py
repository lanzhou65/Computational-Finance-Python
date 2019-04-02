
with open("AAPL.csv") as f:

    L = [line.strip().split(",") for line in f]
    
    #change sting to float for column 2:6
    for j in range(1, len(L)):
        for i in range(2,7):
            L[j][i] = float(L[j][i])
        
    #print(L[:50])    
    rows = len(L);
    cols = len(L[1]);
    print(rows)
    print(cols); 
    
    daysRange = []
    for i in range(rows-1):
        daysRange.append(round((L[i+1][3]- L[i+1][4]),3))
    #print(type(L))

f = open('AAPL.csv', 'a')
L[0].append('daysRange')
for i in range(rows -1):
    L[i+1].append(daysRange[i])


appl_sorted = sorted(L[1:], key = lambda x: x[7])
appl_sorted.insert(0,L[0])
#print(appl_sorted[:5])

close_on_high = list(filter(lambda x: (x[3]- x[5]) <= 0.01, appl_sorted[1:] ))
#print('close on high is ', close_on_high)

low_vol_days = list(filter(lambda x: (x[7]/x[4]) <= 0.01, appl_sorted[1:]))
print('low_vol_days is ', low_vol_days[3][3])
#print(len(low_vol_days))

f.close()
if f.closed:
    print('AAPL file is closed')

f = open("Output_file.csv", "w+")
f.writelines( "first 5 appl_sorted lines are\n")
f.writelines( "%s\n" % item for item in appl_sorted[:6] );

f.writelines( "last 5 appl_sorted lines are\n")
f.writelines( "%s\n" % item for item in appl_sorted[-5:] );

f.writelines( "close_on_high\n")
f.writelines( "%s\n" % item for item in close_on_high );

f.writelines( "low_vol_days\n")
f.writelines( "%s\n" % low_vol_days[i][0] for i in range(len(low_vol_days)));

f.close()
if f.closed:
    print('Output_file is closed')

