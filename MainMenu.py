import sys
import random
import timeit
from bsddb3 import db

# Make sure you run "mkdir /tmp/my_db" first!
DA_FILE = "/tmp/my_db/sample_db"
DB_SIZE = 1000
SEED = 10000000
if sys.argv[1] == "btree":
	TYPE = "DB_BTREE"
	main()
elif sys.argv[1] == "hash":
	TYPE = "DB_HASH"
	main()
elif sys.argv[1] == "indexfile":
	TYPE = "index"
	main()
else:
	print("Invalid Argument!")
	
def main():
	while True:
		#show main menu
		print ("Main Menu \n")
		print ("Programs Available:")
		print ("\t1. Create and populate a database")
		print ("\t2. Retrieve records with a given key")
		print ("\t3. Retrieve records with a given data")
		print ("\t4. Retrieve records with a given range of key values")
		print ("\t5. Destroy the database")
		print ("\t6. Quit")
		
		program = input("Choose Program Number: \n\t")
		if program == "1":
			# Call fxn to create db and populate it
			createDB()
		elif program == "2":
			# Call key record retreval fxn
			print(2)
		elif program == "3":
			# Call data retreaval record fxn 
			print(3)
		elif program == "4":
			# Call range record retreaval fxn
			print(4)
		elif program == "5":
			# Call destroy db
			print(5)
		elif program == "6":
			# Quit Program
			print("Thank you! \nGoodbye")
			break
		else:
			print ("Invalid Input")



def get_random():
	return random.randint(0, 63)
def get_random_char():
	return chr(97 + random.randint(0, 25))


def createDB():
	database = db.DB()
	try:
		# create a btree file
		database.open(DA_FILE,None, db.DB_BTREE, db.DB_CREATE)
	except:
		print("Error creating file.")
		return
	random.seed(SEED)b

	for index in range(DB_SIZE):
		krng = 64 + get_random()
		key = ""
		for i in range(krng):
			key += str(get_random_char())
		vrng = 64 + get_random()
		value = ""
		for i in range(vrng):
			value += str(get_random_char())
		#print (key)
		#print (value)
		#print ("")
		key = key.encode(encoding='UTF-8')
		value = value.encode(encoding='UTF-8')
		database.put(key, value);

	## retriving all values
	#cur = database.cursor()
	#iter = cur.first()
	#while iter:
		#print(iter[0].decode("utf-8"))
		#print(iter[1].decode("utf-8"))
		#iter = cur.next()
		#print("------------------------")
	try:
		database.close()
	except Exception as e:
		print (e)
		return


main()