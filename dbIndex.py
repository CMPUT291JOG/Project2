from bsddb3 import db
import time
import random

# creating database path variables
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

def createDB():
	database = db.DB()
	database2 = db.DB()
	try:
		# create a btree file
		database.open(DA_FILE,None, db.DB_BTREE, db.DB_CREATE)
	except Exception as error:
		print(error)
		
	try:
		# create a second btree file
		database2.open(DA_FILE2,None, db.DB_BTREE, db.DB_CREATE)
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
		database2.put(value, key)

	cur = database.cursor()
	iter = cur.first()
	while iter:
		print("Key = ",iter[0].decode('UTF-8'))
		print("Value = ",iter[1].decode('UTF-8'))
		iter = cur.next()
	
	try:
		database.close()
		database2.close()
	except Exception as error:
		print(error)
	

# delete existing database file
def deleteDB():
	database = db.DB()
	database2 = db.DB()
	try:
		database.remove(DA_FILE,None,0)
		database2.remove(DA_FILE2,None,0)
	except Exception as error:
		print(error)

# gets a given record at a given key
def getRecordByKey(key):
	database = db.DB()
	key = key.encode('UTF-8')
	value = None
	try:
		database.open(DA_FILE, None, db.DB_BTREE, db.DB_DIRTY_READ)
		value = database.get(key)
		if value:
			value = value.decode('UTF-8')
	except exception as error:
		print(error)
	return value

# gets a given record from a given value
def getRecordByData(value):
	database = db.DB()
	value = value.encode('UTF-8')
	key = None
	try:
		database.open(DA_FILE2, None, db.DB_BTREE, db.DB_DIRTY_READ)
		key = database.get(value)
		if key:
			key = key.decode('UTF-8')
	except exception as error:
		print(error)
	return key

# gets range of data given upper and lower
def getRange(lower, upper):
	lower = lower.encode('UTF-8')
	upper = upper.encode('UTF-8')
	data = []
	try:
		database = db.DB()
		database.open(DA_FILE, None, db.DB_BTREE, db.DB_DIRTY_READ)
		cursor = database.cursor()
		record = cursor.set_range(lower)
		while record[0] < upper and record[0] > lower:
			data.append((record[0].decode('UTF-8'), record[1].decode('UTF-8')))
			record = cursor.next()
		database.close()
	except Exception as error:
		print(error)
	return data

# MAIN
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
			key = getRecordByData(value)
			end = time.time()
			
			print()
			if key is None:
				print("Number of records retrieved: 0")
				print('Time:', int((end - start) * (10**6)), 'ms')
				print("No changes made to the answers file")
				continue			
			print("Number of records retrieved: 1")
			print('Time taken:', int((end - start) * (10**6)), 'ms')
			
			with open(OUTPUTPATH, 'a') as f:
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
