#reading csv file and storing the data into a database

import csv
import mysql.connector as m
mycon=m.connect(host='localhost',user='root',passwd='Kolkata52',database='file')
c=mycon.cursor()
c.execute('CREATE TABLE product(\
Product_ID INTEGER NOT NULL PRIMARY KEY,\
Company VARCHAR(10) NOT NULL,\
Type VARCHAR(10) NOT NULL,\
Tonnage FLOAT NOT NULL,\
Model_no VARCHAR(10) NOT NULL,\
Cost INTEGER NOT NULL,\
Star FLOAT,\
YOM INTEGER,\
Rate FLOAT);')
with open('project.csv','r') as p:
    r=csv.reader(p)
    for i in r:
        a="INSERT INTO product VALUES({},'{}','{}',{},'{}',{},{},{},{})"
        c.execute(a.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    mycon.commit()
