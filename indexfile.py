#Includes
from bsddb3 import db
import random
import time

#Ensure our database path exists
DB_PATH = '/tmp/almokdad_db'
OUTPUTPATH = 'answers.txt'


#START SAMPLE FILE CODE
DA_FILE = DB_PATH + '/sample.db'
DA_FILE2 = DB_PATH + '/sample2.db'

# start data generation variables
DB_SIZE = 100000
SEED = 10000000

# STARTING PROGRAM METHODS
def getRandom():
	return random.randint(0, 63)

def getRandomChar():
	return chr(97 + random.randint(0, 25))

#Creates a new database and populates with data
def createDB():
	database = db.DB()
	try:
		# create a btree file
		database.open(DA_FILE,None, db.DB_BTREE, db.DB_CREATE)
	except Exception as error:
		print(error)	

	try:
		# create a btree file
		database.open(DA_FILE2,None, db.DB_BTREE, db.DB_CREATE)
	except Exception as error:
		print(error)
    
	random.seed(SEED)

	for index in range(DB_SIZE):
		krng = 64 + getRandom()
		key = ""
		for i in range(krng):
			key += str(getRandomChar())
		vrng = 64 + getRandom()
		value = ""
		for i in range(vrng):
			value += str(getRandomChar())
		key = key.encode('UTF-8')
		value = value.encode('UTF-8')
		database.put(key, value)

        usedVal = []
        if(value in usedVal):
            db2[value] += ";;;".encode('utf-8') + key
        else:
            db2[value] = key
        
    try:
        db.close()
        db2.close()
    except Exception as e:
        print(e)

#Deletes the existing database file
def delete_db():
    try:
        os.remove(DA_FILE)
        os.remove(DA_FILE2)
    except Exception as e:
        print(e)

#Get a given record from a given key
def get_record(key):
    key = key.encode('utf-8')
    value = None
    try:
        db = bsddb.btopen(DA_FILE, "w")
        if db.has_key(key):
            value =  db[key].decode('utf-8')
    except Exception as e:
        print(e)
    return value

#Get a given record from a given value
def get_key(value):
    value = value.encode('utf-8')
    keys = []
    try:
        db = bsddb.btopen(DA_FILE2, "w")
        if db.has_key(value):
            keys = db[value].decode('utf-8').split(";;;")
        db.close()
    except Exception as e:
        print(e)
    
    return keys

def get_range(lower, upper):
    lower = lower.encode('utf-8')
    upper = upper.encode('utf-8')
    data = []
    try:
        #db = bdb.DB()
        #db.open(DA_FILE, None, bdb.DB_BTREE, bdb.DB_DIRTY_READ)
        db = bsddb.btopen(DA_FILE, "w")
        rec = db.set_location(lower)
        while rec[0] < upper and rec[0] > lower:
            data.append((rec[0], rec[1]))
            rec = db.next()
        db.close()
    except Exception as e:
        print(e)
    return data

#Main program
def main():
    selection = None
    while True:
	    print()
	    print('1. Create and populate a database')
	    print('2. Retrieve records with a given key')
	    print('3. Retrieve records with a given data')
	    print('4. Retrieve records with a given range of key values')
	    print('5. Destroy the database')
	    print('6. Quit\n')
	    
	    selection = int(input('Please select an option: '))
	    if selection > 6 or selection < 1:
		    print('ERROR: Invalid Selection, Please choose from the following options')
		    continue
    
	    if selection == 1:
		    print('Creating and populating the database')
		    createDB()
		    print('Database created and populated')
	    
	    elif selection == 2:
		    print('Retrieving records with key')
		    key = input('Please enter a key: ')
		    start = time.time()
		    value = getRecordByKey(key)
		    end = time.time()
		    
		    print()
		    if value is None:
			    print("Number of records retrieved: 0")
			    print('Time:', int((end - start) * (10**6)), 'ms')
			    print("No changes made to the answers file")
			    continue
		    
		    print("Number of records retrieved: 1")
		    print('Time taken:', int((end - start) * (10**6)), 'ms')
		    
		    with open(OUTPUTPATH, 'a') as f:
			    f.write(key + '\n' + value + '\n\n')
		    
		    print("Records are written to answers file")
	    
	    elif selection == 3:
		    print('Retrieving records with data')
		    value = input('Please enter a value: ')
		    start = time.time()
		    keys = getRecordByData(value)
		    end = time.time()
		    
		    print()
		    print("Number of records retrieved: ", len(keys))
		    print('Time taken:', int((end - start) * (10**6)), 'ms')
    
		    if len(keys) == 0:
			    print("No changes made to the answers file.")
			    continue
		    
		    with open(OUTPUTPATH, 'a') as f:
			    for key in keys:
				    f.write(key + '\n' + value + '\n\n')
	    
	    elif selection == 4:
		    print('Retrieving records with range')
		    lower = input('Lower bound: ')
		    upper = input('Upper bound: ')
		    start = time.time()
		    data = getRange(lower, upper)
		    end = time.time()
		    
		    print("Number of records retrieved: ", len(data))
		    print('Time taken:', int((end - start) * (10**6)), 'ms')
    
		    if len(data) == 0:
			    print("No changes made to answers.")
			    continue
		    with open(OUTPUTPATH, 'a') as f:
			    for dataTuple in data:
				    f.write(dataTuple[0] + '\n' + dataTuple[1] + '\n\n')
		    
	    elif selection == 5:
		    print('Deleting Database')
		    deleteDB()
		    
	    elif selection == 6:
		    print("Quitting and clearing answers...")
		    with open(OUTPUTPATH, 'w'):
			    pass
		    print('Thank you! \nGoodbye')
		    break
if __name__ == '__main__':
    main();

#Cleanup the tmp folder
try:
    shutil.rmtree(DB_PATH)
    os.remove('answers.txt')
except Exception as e:
    print(e)
