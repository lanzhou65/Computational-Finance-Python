from collections import Counter
import re
from collections import defaultdict

ii=['red', 'blue', 'red', 'green', 'blue', 'blue']
cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
     cnt[word] += 1

print(cnt)

cnt1 = Counter()
for i in [1,3,4,4,4,5]:
  cnt1[i] +=1 

print(cnt1)

c = Counter([1,3,4,4,4,5])
print('c is ', c)

oo = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])


print('most common',oo.most_common(10))


s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k , v in s:
  d[k].append(v)

print(d.items())

yy = 'mississippi'
y = defaultdict(int)
for i in yy:
  y[i] +=1 

print(y)


#sort using the dict values 
wc = sorted(b.items(), key = lambda (x,y): y, reverse=True)
print(wc)


#sort using the dict values 
wc = sorted(b.items(), key = lambda (x,y): y, reverse=True)
print(wc)

print([i if i %2 ==0 else 99 for i in range(5) ])

a = {i: i*i for i in range(5)}; print(a)
c = {i*i for i in [-2,5, 3]}; print(c)


r = [1,2,3,4,9]
zeros = [0 for _ in r]; print(zeros)

#generage pairs 
o=[(x,y) 
    for x in range(5) 
    for y in range(2)]
print(o)

#generate pairs with x<y 
o=[(x,y) 
    for x in range(5) 
    for y in range(x+1,5)]
print(o)


t=[x for x in range(4,6)]; print('t',t)

