from bsddb3 import db
import time
import random

# Try creating a path according to directory named 
# by a user account from one of our group members
DA_FILE = '/tmp/almokdad_db/sample.db'
OUTPUTPATH = 'answers.txt'
 
# start data generation variables
DB_SIZE = 100000
SEED = 10000000

# start program method by generating key/value randomly
def getRandom():
	return random.randint(0, 63)

def getRandomChar():
	return chr(97 + random.randint(0, 25))

# function for creating the hash database 
def createDB():
	# assign database to variable
	database = db.DB()
	try:
		# create a HASH file
		database.open(DA_FILE,None, db.DB_HASH, db.DB_CREATE)
	except Exception as error:
		print(error)
	# feed the database randomly by 10,000,000
	random.seed(SEED)

	# loop index within range of 100,000
	for index in range(DB_SIZE):
		krng = 64 + getRandom()
		key = ""
		# creating random key		
		for i in range(krng):
			key += str(getRandomChar())
		vrng = 64 + getRandom()
		value = ""
		# creating random value		
		for i in range(vrng):
			value += str(getRandomChar())
		# encoding key and value
		key = key.encode('UTF-8')
		value = value.encode('UTF-8')
		# putting it in file
		database.put(key, value)

	# assigning cursor
	cur = database.cursor()
	iter = cur.first()
	# loop for each iteration for decoding
	while iter:
		print("Key = ",iter[0].decode('UTF-8'))
		print("Value = ",iter[1].decode('UTF-8'))
		iter = cur.next()
	# try closing database 
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
	# assign variable name to database
	database = db.DB()
	# encoding key
	key = key.encode('UTF-8')
	value = None
	try:
		# try opening file
		database.open(DA_FILE, None, db.DB_HASH, db.DB_DIRTY_READ)
		# get value by key
		value = database.get(key)
		if value:
			# decoding value
			value = value.decode('UTF-8')
	# exception for error
	except exception as error:
		print(error)
	# return value for this function
	return value

# gets a given record from a given value
def getRecordByData(value):
	# encoding for value
	value = value.encode('UTF-8')
	key = []
	try:
		# try opening file		
		database = db.DB()
		database.open(DA_FILE, None, db.DB_HASH, db.DB_DIRTY_READ)
		# assigning cursor
		cursor = database.cursor()
		# set to first record
		record = cursor.first()
		# loop through the record until found match
		while record:
			# find matched value
			if record[1] == value:
				# add after decoding
				key.append(record[0].decode('UTF-8'))
			record = cursor.next()
		database.close()
	except Exception as error:
		print(error)
	# return key for this function
	return key

# gets range of data given upper and lower
def getRange(lower, upper):
	# encode lower and upper bound
	lower = lower.encode('UTF-8')
	upper = upper.encode('UTF-8')
	# create data as empty list	
	data = []
	try:
		database = db.DB()
		# try opening file				
		database.open(DA_FILE, None, db.DB_HASH, db.DB_DIRTY_READ)
		# assigning cursor		
		cursor = database.cursor()
		record = cursor.first()
		# loop through the record by lower and upper bound		
		while record:
			if record[0] < upper and record[0] > lower:
				data.append((record[0].decode('UTF-8'), record[1].decode('UTF-8')))
			record = cursor.next()
		database.close()
	except Exception as error:
		print(error)
	# return data for this function
	return data

# MAIN
def main():
	# create and initize selection to none
	selection = None
	# keep running the program until call for exit
	while True:
		print()
		print('1. Create and populate a database')
		print('2. Retrieve records with a given key')
		print('3. Retrieve records with a given data')
		print('4. Retrieve records with a given range of key values')
		print('5. Destroy the database')
		print('6. Quit\n')
		# ask for selection from user input
		selection = int(input('Please select an option: '))
		# if selection out of range, print error message
		if selection > 6 or selection < 1:
			print('ERROR: Invalid Selection, Please choose from the following options')
			continue
		# selection for creating and populating the database
		if selection == 1:
			print('Creating and populating the database')
			createDB()
			print('Database created and populated')
		# selection for retrieving records by key
		elif selection == 2:
			print('Retrieving records with key')
			# ask user input for key to search
			key = input('Please enter a key: ')
			# start timer
			start = time.time()
			# save found value to variable
			value = getRecordByKey(key)
			end = time.time()
			
			print()
			# if no value found, print result and continue
			if value is None:
				print("Number of records retrieved: 0")
				print('Time:', int((end - start) * (10**6)), 'ms')
				print("No changes made to the answers file")
				continue
			# otherwise print the time needed for finding the value
			print("Number of records retrieved: 1")
			print('Time taken:', int((end - start) * (10**6)), 'ms')
			# open and write answer to file
			with open(OUTPUTPATH, 'a') as f:
				f.write(key + '\n' + value + '\n\n')
			# print to show the records are written to file
			print("Records are written to answers file")

		# selection for retrieving records by value		
		elif selection == 3:
			print('Retrieving records with data')
			# asking user input for value to search
			value = input('Please enter a value: ')
			# start timer
			start = time.time()
			# assign found key to variable
			keys = getRecordByData(value)
			end = time.time()
			
			# print the time for getting the key result
			print()
			print("Number of records retrieved: ", len(keys))
			print('Time taken:', int((end - start) * (10**6)), 'ms')
			# if no key found, print and continue
			if len(keys) == 0:
				print("No changes made to the answers file.")
				continue
			# otherwise open and write to answer file
			with open(OUTPUTPATH, 'a') as f:
				for key in keys:
					f.write(key + '\n' + value + '\n\n')
		# selection for retrieving records by range				
		elif selection == 4:
			print('Retrieving records with range')
			lower = input('Lower bound: ')
			upper = input('Upper bound: ')
			start = time.time()
			data = getRange(lower, upper)
			end = time.time()
			# print number of records found and by how long it took 
			print("Number of records retrieved: ", len(data))
			print('Time taken:', int((end - start) * (10**6)), 'ms')
			# if found none, print message and continue
			if len(data) == 0:
				print("No changes made to answers.")
				continue
			# otherwise open and write to answer file
			with open(OUTPUTPATH, 'a') as f:
				for dataTuple in data:
					f.write(dataTuple[0] + '\n' + dataTuple[1] + '\n\n')
		# selection for deleting Database	
		elif selection == 5:
			print('Deleting Database')
			deleteDB()
		# selection for exiting the program	
		elif selection == 6:
			print("Quitting and clearing answers...")
			with open(OUTPUTPATH, 'w'):
				pass
			print('Thank you! \nGoodbye')
			break

if __name__ == '__main__':
	main();
