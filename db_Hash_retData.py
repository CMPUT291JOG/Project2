# CMPUT 291, Project 2
# Find input data value in DB_HASH
# Group Members: Gemma, Omar, Waiyi
# Due: April 7, 2016

# the Berkeley db database
from bsddb3 import db
import timeit
                
'''
filename = 't1.db'
#Get an instance of BerkeleyDB
t1DB = db.DB

# Create a database in file "t1" using Hash access method
t1DB.open(filename, None, db.DB_HASH, db.DB_CREATE)

# Insert elements in database 

# Close database
t1DB.close()
'''
# get data value to search for
inputData = input("Please enter data value to be found: ")

# Starting timer
time = timeit.Timer()

# Open database
t1DB = db.DB()

#Get cursor object
cur = t1DB.cursor()

rec = cur.first()
while rec:
        k,d = rec
        count +=1
        if d == inputData:
                print(d)
        rec = cursor.next()
cur.close()
t1DB.close()


print("Number of records retrieved: %d", count)
print("Execution Time: %d", time)
