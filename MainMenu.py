
import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it
import datetime



def main() :
	while True:
		# get usename, defult to current user
		user = input("Username [%s]: " % getpass.getuser())
		if not user:
			user=getpass.getuser()
		
		# get password
		pw = getpass.getpass()
	
		# The URL we are connnecting to 
		conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
		
		try:  
			# Establish a connection
			connection = cx_Oracle.connect(conString)
		except cx_Oracle.DatabaseError as exc:
			# Failed connection
			print ("Invalid Username/Password. \nPlease try again\n")
			continue
		
		print ("Connection Established!")
		break
	
	#create a cursor 
	cur = connection.cursor()     
	while True:
		#show main menu
		print ("Main Menu \n")
		print ("Programs Available:")
		print ("\t1. New Vehicle Registration")
		print ("\t2. Auto Transaction Registration")
		print ("\t3. Driver Licence Registration")
		print ("\t4. Violation Record")
		print ("\t5. Search Engine")
		print ("\t6. Exit")
	
		program = input("Choose Program Number: \n\t")
		if program == "1":
			# Call New Vehichle Registrarion
			vehicle_input(cur)
		elif program == "2":
			# Call Auto Transaction Registration
			trans_input(cur)
		elif program == "3":
			# Call Driver Licence Registration
			licence_input(cur)
		elif program == "4":
			# Call Violatio Record
			violation_input(cur)
		elif program == "5":
			# Call Search Engine
			print(5)
		elif program == "6":
			# Quit Program
			print(6)
			break
		else:
			print ("Invalid Input")
	
	cur.close()
	connection.close()	
		      
#-------------------------------New Vehichle Registration---------------------------------------#
# This component is used to register a new vehicle by an auto registration officer.
# A new vehicle is one that has not been registered in the database. 
# This will allow an officer to enter the detailed information of vehicle and personal information 
# with new owners, if it is not in the database.
# You may assume that all the information about vehicle types has been loaded in the initial database.
# how is it assigning these registering people to the following vehicle?
# how are we assuring there is at least one primary owner?
#---------------------------------------------------------------------------------------------
# Assume vehicle type is loaded in database with two attributes in specified format as follow:  
#      type_id     integer	an	  type    CHAR(10),
#----------------------------------------------------------------------------------------------
# A Vehicle has  8 attributes in specified format as follow accordingly:
# serial_no    CHAR(15),  maker   VARCHAR(20),  model   VARCHAR(20),
# year     number(4,0),  color    VARCHAR(10),  type_id   integer
#--------------------------------------------------------------------------------------------
# Function for vehicle input
def vehicle_input(cur):
	# try to get the SIN in proper format which is 15 character or less	
	sin = input('Enter Owner SIN Number: ')
	while len(sin) > 15:
		print('Invalid SIN Number Format [too long]')
		sin = input('Enter Owner SIN Number: ')
		
	# execute query to get for matched SIN
	valid_people = "SELECT sin FROM people WHERE sin = '%s'" % (sin)
	cur.execute(valid_people)
	valid_people = cur.fetchall()
	# if result empty, no match for SIN	
	if len(valid_people) == 0:
		# while SIN not found, check with user to register person or not
		while True:
			answer = input("Person not in database, Register person?(y,n) \n\t")
			# if register person, call for inputting person data			
			if answer == 'y':
				person_input(cur,sin)
				break
			# if not registering person, back to main menu			
			elif answer == 'n':
				print("Back to Main Menu")
				return
			# otherwise error message			
			else:
				print("Invalid Input")	
	# try to check with user where this person is primary vehicle owner, with proper input
	is_primary_owner = input('Is this owner the primary vehicle owner? (y/n) \n\t')
	while ((is_primary_owner != 'y') and (is_primary_owner != 'n')):
		print ("Invalid Input")
		is_primary_owner = input('Is this owner the primary vehicle owner? (y/n)\n\t')	
	# try to get serial number in proper format for 15 character or less
	while True:
		serial_no = input('Please enter vehicle serial number: ')
		while len(serial_no) > 15:
			print('Invalid Serial Number length')
			serial_no = input('Please enter vehicle serial number: ')
		
		# execute query to confirm serial number does not already exist in database
		serials = "SELECT serial_no FROM vehicle WHERE serial_no = '%s'" % (serial_no)
		cur.execute(serials)
		inDb = cur.fetchall()
		if len(inDb) == 0:
			break
		else:
			# if vehicle already registered, check with user for registering another vehicle			
			answer = input("Vehicle already regestered, try new Vehicle?(y,n) \n\t")
			# if yes, continue			
			if answer == 'y':
				continue
			# if no, back to main menu			
			elif answer == 'n':
				print("Back to Main Menu")
				return
			# otherwise error message			
			else:
				print("Invalid Input")			
	# try to get vehicle maker input in proper format 20 character or less		 	
	maker = input('Please enter vehicle maker: ')
	while len(maker) > 20:
		print('Invalid Maker length')
		maker = input('Please enter vehicle maker: ')
	# try to get model in format 20 character or less	
	model = input('Please enter vehicle model: ')
	while len(model) > 20:
		print('Invalid Model length')
		model = input('Please enter vehicle model: ')
	# try to get year input in 4 character
	while True:
		year = input('Please enter vehicle year [yyyy]: ')
		if len(year) != 4:
			print('Invalid Year')
			continue
		else:
			# try to convert string to integer			
			try:	
				year = int(year)
			# if failed, improper format and print error message			
			except ValueError:
				print('Invalid Year')
				continue
			break
	# try to get vheicle color in 10 character or less	
	color = input('Please enter vehicle color: ')
	while len(color) > 10:
		print('Invalid Color length')
		color = input('Please enter vehicle color: ')
		
	# try to get type ID and check if input is integer
	while True :
		type_id = input('Please enter type_id: ')
		try: 
			int(type_id)
		# if input failed to convert to integer, print error message
		except ValueError:
			print('Invalid type Id format [Must be Integer]')
			continue
		# execute query to check type ID inputed correctly whether in database		
		types = "SELECT type_id FROM vehicle_type WHERE type_id = '%s'" % (type_id)
		cur.execute(types)
		exists = cur.fetchall()
		if len(exists) > 0:
			break
		else:
			# if not, wrong input for type ID			
			print("Type ID does not exist")	
	# try execute query for inserting values into vehicle table and commit
	sqlstr1 = "INSERT INTO vehicle VALUES (:serial_no, :maker, :model, :year, :color, :type_id)"
	try:
		cur.execute(sqlstr1, {'serial_no':serial_no, 'maker':maker, 'model':model, 'year':year, 'color':color, 'type_id':type_id})
		cur.execute("commit")
	# if failed, print error message  
	except cx_Oracle.DatabaseError as exc:
		error = exc.args[0]
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
				
	# Owner table entry
	# Owner_id is the one of above entered sin number
	
	# try inserting values into owner table and commit
	while True:
	
		sqlstr2 = "INSERT INTO owner VALUES (:owner_id, :vehicle_id, :is_primary_owner)"
		try:
			cur.execute(sqlstr2, {'owner_id':sin, 'vehicle_id':serial_no, 'is_primary_owner':is_primary_owner})
			cur.execute("commit")
		# otherwise print error messge			
		except cx_Oracle.DatabaseError as exc:
			error = exc.args[0]
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message) 
			
		# check with user for inputting another owner
		while True:
			answer = input("Add another Owner?(y/n)\n\t")
			if answer == "y":
				# try to get the SIN in proper format which is 15 character or less			
				sin = input('Enter Owner SIN Number: ')
				while len(sin) > 15:
					print('Invalid SIN Number Format [too long]')
					sin = input('Enter Owner SIN Number: ')
				# execute query to get for matched SIN  
				valid_people = "SELECT sin FROM people WHERE sin = '$s'" % (sin)
				cur.execute(valid_people)
				valid_people = cur.fetchall()
				# if result empty, no match for SIN				
				if len(valid_people) == 0:
					# while SIN not found, check with user to register person or not
					while True:
						answer = insert("Person not in database, Register person?(y,n) \n\t")
						# if register person, call for inputting person data						
						if answer == 'y':
							person_input(cur,sin)
							break
						# if not registering person, back to main menu						
						elif try_again == 'n':
							print("Back to Main Menu")
							return
						# otherwise error message						
						else:
							print("Invalid Input")	
				# try to check with user where this person is primary vehicle owner, with proper input
				is_primary_owner = input('Is this owner the primary vehicle owner? (y/n) \n\t')
				while ((is_primary_owner != 'y') and (is_primary_owner != 'n')):
					print ("Invalid Input")
					is_primary_owner = input('Is this owner the primary vehicle owner? (y/n)\n\t')				
				
				break
			elif answer == 'n':
				break
			else:
				print("invalid input")
				continue
			
		if answer == "y":
			continue
		else:
			break
	# successfully input data			
	print("Input Successfull!")
	# check with user for inputting another vehicle	
	while True:
		try_again = input("Do you want to input another vehichle? (y/n)")
		if try_again == 'y':
			vehicle_input(cur)
			return
		elif try_again == 'n':
			return
		else:
			print("invalid input") 

# function for inputting a person
def person_input(cur, sin):
	# try to get input of the person's name in 15 characters or less	
	name = input('Enter Name: ')
	while len(name) > 15:
		print('Invalid Name format [max 15 char]')
		sin = input('Enter Name: ')
	# try to get input for height in 8 character or less
	while True:
		height = input('Enter registrants height: ')
		# if more than 8 characters, print error		
		if len(height) > 8:
			print("invalid input")
			continue
		# otherwise try converting it to float format		
		else:
			try: 
				height = float(height)
			# if failed, print error			
			except ValueError: 
				print('Invalid height format')
				continue
			break
	
	height = round(height,2)

	# try to get input weight in 8 characters or less	
	while True:
		weight = input('Enter registrants weight: ')
		if len(weight) > 8:
			print("invalid input")
			continue
		else:
			try: 
				weight = float(weight)
			except ValueError: 
				print('Invalid height format')
				continue
			break
	# round weight to 2 decimals
	weight = round(weight,2)
	
	# try to get eyecolor in 10 characters or less	    
	eyecolor = input('Enter registrants eye color: ')
	while len(eyecolor) > 10:
		print('Invalid eyecolor format [max 10 char]')
		eyecolor = input('Enter registering eye color: ')
	# try to get hair color in 15 characters or less		
	haircolor = input('Enter registrants hair color: ')
	while len(haircolor) > 15:
		print('Invalid hair color format [max 15 char]')
		haircolor = input('Enter registrants hair color: ')
	# try to get address in 50 characters or less		
	addr = input('Enter registrants address: ')
	while len(addr) > 50:
		print('Invalid address format [only 50 characters]')
		addr = input('Enter registrants address: ')
	# try to get gender in m or f	  
	gender = input('Enter registrants gender [m/f]: ')
	while ((gender != 'm') and (gender != 'f')):
		print('Invalid gender format [m/f]')
		gender = input('Enter registrants gender [m/f]: ')
	# try to get birthday in 8 characters	  
	birthday = input('Enter registrants birthday [ddmmyyyy]: ')
	while len(birthday) != 8:
		print('Invalid birthday format [ddmmyyyy]')
		birthday = input('Enter registrants birthday [ddmmyyyy]: ')
		    
	# converting birthday to sql date format
	birthday = datetime.datetime.strptime(birthday, "%d%m%Y").date()
	
	# inputting into database
	sqlStr1 = 'INSERT INTO people VALUES (:sin, :name, :height, :weight, :eyecolor, :haircolor, :addr, :gender, :birthday)'

	# try execute query to insert values into people	
	try:
		cur.execute (sqlStr1, {'sin':sin, 'name':name, 'height':height, 'weight':weight, 'eyecolor':eyecolor, 'haircolor':haircolor, 'addr':addr, 'gender':gender, 'birthday':birthday})
		cur.execute ("commit")
	
	# if failed, print error message	
	except cx_Oracle.DatabaseError as exc:
		error = exc.args[0]
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)


#------------------------------- Violation Record---------------------------------------#
# This component is used by a police officer to issue a traffic ticket
# for each violation. Assume that all information in regards to the ticket type
# has been loaded and initialized to the database. 
#---------------------------------------------------------------------------------------------
# Ticket Type is initialized with two attributes in specified format as follow:  
#     vtype   CHAR(10)   and   fine number   (5,2)
#----------------------------------------------------------------------------------------------
# A violation ticket has  8 attributes in specified format as follow accordingly:
#  ticket_no     int,              violator_no   CHAR(15),     vehicle_id    CHAR(15),
#  office_no     CHAR(15),    vtype          CHAR(10),      vdate             date,
#  place        varchar(20),  descriptions varchar(1024),
#--------------------------------------------------------------------------------------------

# function for inputting violation record
def violation_input(cur):
	
	# try to get ticket_no from input in correct integer format
	# keep looping until input is correct
	while True :
		ticket_no = input('Enter Ticket Number: ')
		try: 
			int(ticket_no)
		except ValueError:
			print('Invalid Ticket Number format [Must be Integer]')
			continue
		break
	
	ticketexists = "SELECT ticket_no FROM ticket WHERE ticket_no = '%s'" % (ticket_no)
	# execute query to match violator and SIN
	cur.execute(ticketexists)	
	# get data
	ticketexists = cur.fetchall()
	
	# while return empty, sin not match
	while len(ticketexists) != 0:
		# print error message for sin not match 
		print('Ticket Number exist, try again')
		# request violator_no again until correct and exit while loop
		violator_no = input('Enter Ticket Number: ')
		ticketexists = "SELECT ticket_no FROM ticket WHERE ticket_no = '%s'" % (ticket_no)
		# execute query to match violator and SIN
		cur.execute(ticketexists)	
		# get data
		ticketexists = cur.fetchall()	
	
	# get violator_no which contains 15 or less character
	# keep looping until getting the proper format
	violator_no = input('Enter Violator Number: ')
	while len(violator_no) > 15:
		print('Invalid Violator Number Format [too long]')
		violator_no = input('Enter Violator Number: ')
	
	# check if violator_no is a valid SIN and for which if it already exists
	valid_people = "SELECT sin FROM people WHERE sin = '%s'" % (violator_no)
	# execute query to match violator and SIN
	cur.execute(valid_people)	
	# get data
	valid_people = cur.fetchall()
	
	# while return empty, sin not match
	while len(valid_people) == 0:
		# print error message for sin not match 
		print('Violator Number doesnt exist, try again [must be registered sin number]')
		# request violator_no again until correct and exit while loop
		violator_no = input('Enter Violator Number: ')
		valid_people = "SELECT sin FROM people WHERE sin =  '%s'" % (violator_no)
		cur.execute(valid_people)
		valid_people = cur.fetchall()

	# get vehicle_id for charater 15 or less	
	vehicle_id = input('Enter Vehicle Identification: ')
	while len(vehicle_id) > 15:
		print('Invalid Vehicle Id Format [too long]')
		vehicle_id = input('Enter Vehicle Identification: ')
		
	# making sure vehicle id is extant serial no
	serials = "SELECT serial_no FROM vehicle WHERE serial_no = '%s'" % (vehicle_id)
	cur.execute(serials)
	inDb = cur.fetchall()
	while len(inDb) == 0:
		print('Vehicle ID Number doesnt exist, try again [must be registered serial number]')
		vehicle_id = input('Enter vehicle ID: ')
		serials = "SELECT serial_no FROM vehicle WHERE serial_no = '%s'" % (vehicle_id)
		cur.execute(serials)
		inDb = cur.fetchall()
	
	# input office_no for number  15 or less	
	office_no = input('Enter Officer Number: ')
	while len(office_no) > 15:
		print('Invalid Officer Number Format [too long]')
		office_no = input('Enter Officer Number: ') 
	
	# input violation type with 10 or less number	 
	vtype = input('Enter Violation Type: ')
	while len(vtype) > 10:
		print('Invalid Violation Type [too long]')
		vtype = input('Enter Violation Type: ')
	
	# input violation date length less than 8	
	vdate = input('Enter Violation Date [ddmmyyyy]: ')
	while len(vdate) > 8:
		print('Invalid Violation Date format')
		vdate = input('Enter Violation Date [ddmmyyyy]: ')
	
	# input place in length 20 or less
	place = input('Enter Violation Place: ')
	while len(place) > 20:
		print('Invalid violation place length')
		place = input('Enter Violation Place: ')
	
	#input descriptions no more than 1024 characters	
	descriptions = input('Enter Violation Description: ')
	while len(descriptions) > 1024:
		print('Invalid description length')
		descriptions = input('Enter Violation Description: ')
	
	# convert to date
	vdate = datetime.datetime.strptime(vdate, "%d%m%Y").date()
	
	# insert statement
	sqlstr1 = "INSERT INTO ticket VALUES (:ticket_no, :violator_no, :vehicle_id, :office_no, :vtype, :vdate, :place, :descriptions)"
	
	# try execute sql insert statment
	try:
		cur.execute(sqlstr1, {'ticket_no':ticket_no, 'violator_no':violator_no, 'vehicle_id':vehicle_id, 'office_no':office_no, 'vtype':vtype, 'vdate':vdate, 'place':place, 'descriptions':descriptions})
		cur.execute("commit")
	# if fail, print errors	
	except cx_Oracle.DatabaseError as exc:
		error = exc.args[0]
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
		
		# allow to choose try again or not
		while True:
			try_again = input('Would you like to try new input? (y/n)')
			if try_again == 'y':
				violation_input(cur)
				return
			elif try_again == 'n':
				return
			else:
				print("invalid input")
	
	print("Input Successfull!")
	# check with user for inptting another entry	
	while True:
		try_again = input("Do you want to input another? (y/n)")
		if try_again == 'y':
			violation_input(cur)
			return
		elif try_again == 'n':
			return
		else:
			print("invalid input")  	


# -------------------------------- Driver Licence Regestration -------------------------------#
# General information:
# Record information as needed to issue a drive licence 
# licence no.CHAR(15), sin CHAR(15), class VARCHAR(10), photo BLOB,
# issuing_date DATE, expiring_date DATE, 
# PRIMARY KEY (licence_no), UNIQUE (sin), FOREIGN KEY (sin) REFERENCES people
# assume image files are stored in a local disk system
#--------------------------------------------------------------------------------------------#
# Specific Requirement:   
# -Register a new driver license (with photo) where the person does not exist in the database.
# -New person should be added.
# -Add driver license for an existing person in database.
# -Add driver license of a person who already has a license. An error message should be shown.
# Note: Most python code are referenced from lab files
#---------------------------------------------------------------------------------
# function for inputting licence registration
def licence_input(cur):

	# create and initialize variables
	file = None
	try_again = 0
	issue = 1
	
	# try to get SIN and in proper format, 15 character or less
	sin = input ('Enter Social insurance number: ')
	while len(sin) > 15:
		print('Invalid SIN input.')
		sin = input ('Enter Social insurance number: ')
	
	# execute query to get licence number by the specified SIN		    
	check = "SELECT licence_no FROM drive_licence WHERE sin = '%s'" % (sin) 
	cur.execute(check)   
	rows = cur.fetchall()
	
	# if there's a driver licence by the specified SIN, error message	
	if (len(rows) != 0):
		print ("Person already has licence, cannot register")
		print ("Returning to main menu")
		return

	# if there is no SIN and driver licence, then execute query to get SIN data
	else:
		valid_people = "SELECT sin FROM people WHERE sin = '%s'" % (sin)
		cur.execute(valid_people)
		valid_people = cur.fetchall()
		# if results nothing
		if len(valid_people) == 0:
			# sin match not found
			while True:
				
				answer = input("Person not in database, Register person?(y,n) \n\t")
				if answer == 'y':
					person_input(cur,sin)
					break
				elif answer == 'n':
					print("Back to Main Menu")
					return
				else:
					print("Invalid Input")
    
    
	licence_num = input ('Enter Licence number: ')
	while len(licence_num) > 15:
		print('Invalid licence number input.')
		licence_num = input ('Enter Licence number: ')	
		# call input function for the rest

	# try to get the licence class and in proper format which is 10 character or less
	licence_class = input ('Enter licence class: ')
	while len(licence_class) > 10:
		print('Invalid licence class iput.')
		licence_class = input ('Enter Licence class: ')
	# while there's nothng in file
	while file == None :
		# try to get a photo and open it		
		photo = input ('Insert photo path: ')
		try:
			file = open (photo,'rb') 
		# if can't open photo, print error message		
		except IOError :	
			print('File not found!')
			
	# read file and then close it	    		
	blobVar = file.read ()
	file.close ()
    
	# try to get input for issuing_date in proper format length of 8
	while issue == 1:    
		issuing_date = input ('Enter issuing date (ddmmyyyy): ')
		# error message for wrong format		
		if len(issuing_date) != 8:
			print("Invalid input")
			continue
		# otherwise try convert to integer		
		else: 
			try: 
				int(issuing_date)
			# print error message if failed to convert to integer				
			except ValueError:
				print("invalid input")
				continue
			issue = 0
	
	# reset issue to 1
	issue = 1
	
	# try to get input for expiring_date in proper format length of 8
	while issue == 1:    
		expiring_date = input ('Enter expiring date (ddmmyyyy): ')
		# if not 8 character, invalid input		
		if len(expiring_date) != 8:
			print("Invalid input")
			continue
		else: 
			# try to convert character to integer			
			try: 
				int(expiring_date)
			# print error message if failed to convert to integer	
			except ValueError:
				print("invalid input")
				continue
			issue = 0    
	      
	# converting integer to date format 
	issuing_date = datetime.datetime.strptime(issuing_date, "%d%m%Y").date()
	expiring_date = datetime.datetime.strptime(expiring_date, "%d%m%Y").date()
	
	# try execute to insert values    
	sqlStr1 = "INSERT INTO drive_licence VALUES ('%s', '%s', '%s', :blobData, :i_d, :e_d)" % (licence_num, sin, licence_class)
	cur.setinputsizes(blobData=cx_Oracle.BLOB)
    
	try:
		cur.execute (sqlStr1, {'blobData': blobVar, 'i_d': issuing_date, 'e_d': expiring_date})
		cur.execute ("commit")
	# if result in error, print error message	
	except cx_Oracle.DatabaseError as exc:
		error = exc.args[0]		
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
		# if failed, check if user wants to try again for new input		
		while True:
			try_again = input('Would you like to try new input? (y/n)')
			# if yes, call the function again			
			if try_again == "y":
				licence_input(cur)
				return
			# otherwise error message			
			elif try_again == "n":
				return
			else:
				print("invalid input")
	# if pass all, input success			    
	print("Input Successfull!")
	# check if user want to have another input    
	while True:
		try_again = input("Do you want to input another? (y/n)")
		# if so, call function again, otherwise exit		
		if try_again == "y":
			licence_input(cur)
			return
		elif try_again == "n":
			return
		else:
			print("invalid input")    

# ------------------------- Auto Transaction  ----------------------#
# allows the officer to enter infomaion to complete the transaction
# w.r.t the details of seller, buyer, date and price
# --------------------------------------------------------------------#
# Auto Transaction has attributes as following:
#  s_date  date,  	price  numeric(9,2),    t_id    CHAR(15),
#  seller_id   CHAR(15), 	  buyer_id    CHAR(15),
#  vehicle_id  CHAR(15),	  officer_id  CHAR(15),
#----------------------------------------------------------------------#  
# Scenerio
# 1) Add a sale record where buyer does not exist in the database
# a new person should be added after asking appropriate information.
# 2) Add a sale record where seller is not an owner of the vehicle 
# an appropriate error message should be shown.
# 3) Add a sale record where vehicle does not exist in the database
# an appropriate message should be displayed.
#----------------------------------------------------------------------#
# function for auto transaction input
def trans_input(cur):
	
	# get transaction id and make sure less than 15 character	
	while True:
		t_id = input ('Enter transaction ID: ')
		# try converting to integer
		try: 
			int(t_id)
		# if failed, print error message and continue
		except ValueError:
			print("Invalid ID")
			continue	
		break	
	# execute query to check transaction_id 
	checktrans = "SELECT transaction_id FROM auto_sale where transaction_id = '%s'" % (t_id) 
	cur.execute(checktrans) 
	rows = cur.fetchall()
	
	# if seller not exist in database
	if (len(rows) != 0):	
		print("Transaction Id exists.")
		print("Returning to main menu")
		return	
	
	# get buyer id and make sure less than 15 characters
	buyer_id = input ('Enter buyer SIN: ')
	while len(buyer_id) > 15:
		print('Invalid SIN.')
		buyer_id = input ('Enter buyer SIN: ')
	# execute query to checki for buyer	
	checkBuyer = "SELECT SIN FROM people WHERE SIN = '%s'" % (buyer_id) 
	cur.execute(checkBuyer) 
	rows = cur.fetchall()
	
	# if buyer not exist in database
	if (len(rows) == 0):
		while True:
			# check with user whether to register the person
			answer = input("Person not in database, Register person?(y,n) \n\t")
			# if yes, call for person input function then break
			if answer == 'y':
				person_input(cur,sin)
				break
			# if no, then back to main menu
			elif answer == 'n':
				print("Back to Main Menu")
				return
			# otherwise error message
			else:
				print("Invalid Input")
 
	
	# get seller id and make sure less than 15 characters
	seller_id = input ('Enter seller ID: ')
	while len(seller_id) > 15:
		print('Invalid seller ID.')
		seller_id = input ('Enter transaction ID: ')
	# execute query to check if the person exist in database
	checkBuyer = "SELECT SIN FROM people WHERE SIN = '%s'" % (seller_id) 
	cur.execute(checkBuyer) 
	rows = cur.fetchall()
	
	# if seller not exist in database
	if (len(rows) == 0):	
		print("Seller not in database.")
		print("Returning to main menu")
		return
	
	
	# get vehicle id and make sure less than 15 characters
	vehicle_id = input ('Enter vehicle ID: ')
	while len(vehicle_id) > 15:
		print('Invalid vehicle ID.')
		vehicle_id = input ('Enter vehicle ID: ') 
	 
	# scenerio 3, check if vehicle in database
	checkVehicle = "SELECT serial_no FROM vehicle WHERE serial_no = '%s'" % (vehicle_id)
	cur.execute(checkVehicle)
	rows = cur.fetchall()
	if len(rows) == 0:
		print("Vehichle not in database.")
		print("Returning to main menu")
		return
		
	# scenerio 2 if seller not owner, error msg
	getOwners = "SELECT owner_id, vehicle_id FROM owner WHERE vehicle_id = '%s' and owner_id = '%s'" % (vehicle_id, seller_id)
	cur.execute(getOwners) 
	rows = cur.fetchall()
	# if return no result, print msg and return menu
	if rows == 0:
		print("Seller does not own vehicle")
		print("Returning to main menu")
		return

	# if s_date not valid, prompt proper message
	while True:
		s_date = input ('Enter sale date (ddmmyyyy): ')
		if len(s_date) != 8:
			print("Invalid input")
			continue
		else: 
			try: 
					int(s_date)
			except ValueError:
					print("invalid input")
					continue	
			break

	# convert to date format
	s_date = datetime.datetime.strptime(s_date, "%d%m%Y").date()
 
	# input for price with 2 decimals
	while True:
		# get input as a float number
		price = input ('Enter price: ')	
		# price cannot be less than 0
		while len(price) > 15:
			print('Invalid price.')
			price = input ('Enter price: ')			
		# try to convert to float format
		try:
			price = float(price)
		# if failed, print error
		except ValueError:
			print("invalid price")
			continue
		# otherwise pass checking 
		break
		
	#convert price from float to two decimals
	price = round(price, 2)
 	
	# try execute inserting values into auto sale table
	sqlStr1 = "INSERT INTO auto_sale VALUES (:transaction_id, :seller_id, :buyer_id, :vehicle_id, :s_date, :price)"
	try:
		cur.execute (sqlStr1, {'transaction_id': t_id, 'seller_id': seller_id, 'buyer_id': buyer_id, 'vehicle_id': vehicle_id, 's_date': s_date, 'price': price})
		cur.execute ("commit")
	# print error if failed
	except cx_Oracle.DatabaseError as exc:
		error = exc.args[0]
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
	
	# successfully executed
	print("Input Successfull!") 
	# check with user for another transaction input
	while True:
		try_again = input('Would you like to input another transaction? (y/n)')
		if try_again == "y":
			licence_input(cur)
			return
		elif try_again == "n":
			return
		else:
			print("invalid input")

main()