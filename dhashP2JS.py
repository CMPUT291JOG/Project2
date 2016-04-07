from bsddb3 import db
import time
import random

# creating database path variables
DA_FILE = '/tmp/almokdad_db/sample.db'
OUTPUTPATH = 'answers.txt'
 
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
	try:
		# create a HASH file
		database.open(DA_FILE,None, db.DB_HASH, db.DB_CREATE)
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

	cur = database.cursor()
	iter = cur.first()
	while iter:
		print("Key = ",iter[0].decode('UTF-8'))
		print("Value = ",iter[1].decode('UTF-8'))
		iter = cur.next()
	
	try:
		database.close()
	except Exception as error:
		print(error)
	

# delete existing database file
def deleteDB():
	database = db.DB()
	try:
		database.remove(DA_FILE,None,0)
	except Exception as error:
		print(error)

# gets a given record at a given key
def getRecordByKey(key):
	database = db.DB()
	key = key.encode('UTF-8')
	value = None
	try:
		database.open(DA_FILE, None, db.DB_HASH, db.DB_DIRTY_READ)
		value = database.get(key)
		if value:
			value = value.decode('UTF-8')
	except exception as error:
		print(error)
	return value

# gets a given record from a given value
def getRecordByData(value):
	value = value.encode('UTF-8')
	key = []
	try:
		database = db.DB()
		database.open(DA_FILE, None, db.DB_HASH, db.DB_DIRTY_READ)
		cursor = database.cursor()
		record = cursor.first()
		while record:
			if record[1] == value:
				key.append(record[0].decode('UTF-8'))
			record = cursor.next()
		database.close()
	except Exception as error:
		print(error)
	return key

# gets range of data given upper and lower
def getRange(lower, upper):
	lower = lower.encode('UTF-8')
	upper = upper.encode('UTF-8')
	data = []
	try:
		database = db.DB()
		database.open(DA_FILE, None, db.DB_HASH, db.DB_DIRTY_READ)
		cursor = database.cursor()
		record = cursor.first()
		while record:
			if record[0] < upper and record[0] > lower:
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
