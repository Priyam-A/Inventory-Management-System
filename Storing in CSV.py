#Making Random data and storing in csv file

import csv
import random as r
import string
with open('project.csv','w',newline='') as p:
    q=csv.writer(p)
    for i in range(1,101):
        a=r.choice(('Hitachi','Daikin','BlueStar','Voltas'))
        b=r.choice(('Split','Concealed','Window'))
        c=r.choice((1.5,1.8,2.0,2.5))
        d=r.choice(string.ascii_uppercase)+str(r.randint(1000000,5000000))
        if c==1.5:
            e=r.randint(28,32)*1000-1
        elif c==1.8:
            e=r.randint(30,34)*1000-1
        elif c==2.0:
            e=r.randint(32,38)*1000-1
        elif c==2.5:
            e=r.randint(36,42)*1000-1
        f=round(r.randint(6,10)/2,1)
        g=r.randint(2019,2021)
        h=round(r.randint(30,50)/10,1)
        t=(i,a,b,c,d,e,f,g,h)
        q.writerow(t)
        
        
        
