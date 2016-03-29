# DB_TREE find select key

from bsddb3 import db
import timeit

keyInput = input("Please Enter Key Value to be found: ")

# Starting timer
time = timeit.Timer()

#Get an instance of BerkeleyDB
DATABASE='dbtreeretrievekey.db'
# Create a new databaseof type BTREE 
database = db.DB()
database.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)

#Get cursor object
cur = database.cursor()

# ASSUMING KEY VALUE DATA PAIRS ALREADY INSERTED INTO DATABASE

# INCASE WE NEED TO JUST BE ITERATING THROUGH DATABASE?
# get all rows inserted into the database
# iter = cur.first()
# while iter:
# print(iter) TO PRINT EACH DATABASE ENTRY
# iter = cur.next()

# WHAT IS THE b REFERENCE?
# get only a specific row
# get only the data at that key: searching using the database object
result = database.get(keyInput)
# key value pair at result variable

print("Number of records retrieved: 1")
print("Execution Time: %d" , time)

cur.close()
database.close()
