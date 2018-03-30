
''' This script will be ran continously onsite.

	Functions:
	- Enroll new emp in fingerprint-scanner and local database. 
	- Clock in current emp
	- Clock out current emp and execute pay-emp.js (to envoke contact call)  '''



from pyfingerprint.pyfingerprint import PyFingerprint
import time
import calendar
import json
import subprocess

# While condition
world_is_spinning = True

while world_is_spinning is True:

	# Load emp_dict.json into python dictionary
	emp_dict = json.load(open('/home/ted/dev/balance/local/emp-dict.json'))

	# Start scanner
	if raw_input("Welcome to DQ. Please hit enter.") == "":
		f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)	

		# emp instructions
		print("Please place finger on scanner.")

		# Wait that finger is read
		while (f.readImage() == False ):
			pass

		# Converts read image to characteristics and stores it in charbuffer 1
		f.convertImage(0x01)

		# Checks if fingerprint enrollment status
		result = f.searchTemplate()
		positionNumber = str(result[0])	

		# If fingerprint is not enrolled
		if positionNumber not in emp_dict:
			
			# Mis-typed name or new emp
			if raw_input("Are you a new employee (y/n)?: ").lower() == 'y':
			
				# emp instructions
				print("Great. Let's get you enrolled.")
				f_name = raw_input("Please enter your first name: ").lower()
				l_name = raw_input("Please enter your last name: ").lower()
				emp_eth_address = raw_input("Please enter your ethereum address: ")

				# Double check emp name
				if raw_input("Is this correct?\n" + f_name + ' ' + l_name +'\nethereum address: ' + emp_eth_address + '\n(y/n): ').lower() == 'y':

					print("Please place finger on scanner.")

					# Wait that finger is read
					while (f.readImage() == False ):
						pass

					# Converts read image to characteristics and stores it in charbuffer 1
					f.convertImage(0x01)

					# Checks if finger is already enrolled
					result = f.searchTemplate()
					positionNumber = result[0]

					if (positionNumber >= 0 ):
						print('Your finger is already enrolled at # ' + str(positionNumber))
						exit(0)

					print('Remove finger...')
					time.sleep(2)

					print('Please place the same finger on the scanner.')

					# Wait that finger is read again
					while ( f.readImage() == False ):
						pass

					# Converts read image to characteristics and stores it in charbuffer 2
					f.convertImage(0x02)

					# Compares the charbuffers
					if ( f.compareCharacteristics() == 0 ):
						raise Exception('Fingers do not match')

					# Creates a template
					f.createTemplate()

					# Saves template at new position number in scanner
					positionNumber = str(f.storeTemplate())

					# Saves template position in local dictionary (position, True is clocked in / False in out, wallet address)
					emp_dict[positionNumber] = [0, emp_eth_address, f_name, l_name]

					# emp message
					print("Thank you " + f_name + ' ' + l_name + '. You are now enrolled.\n')

					# Save json 
					with open('/home/ted/dev/balance/local/emp-dict.json', 'w') as json_file:
						json.dump(emp_dict, json_file)

			else:
				print("Sorry your fingerprint does not match our records.\n")
				# Log event

		# If fingerprint is enrolled and exists in library
		elif positionNumber in emp_dict:

			# See that he is not clocked in (time in == 0)
			if emp_dict[positionNumber][0] == 0: 

				# Set time-in to currect epoch time clock in seconds
				emp_dict[positionNumber][0] = calendar.timegm(time.gmtime()) 

				# emp return message
				print("Welcome to work " + emp_dict[positionNumber][2] +". You are now clocked in at " + str(calendar.timegm(time.gmtime())) + '.\n')
			
				# Save json locally 
				with open('/home/ted/dev/balance/local/emp-dict.json', 'w') as json_file:
					json.dump(emp_dict, json_file)

			# emp is clocked in (time != 0)
			else:

				# Calculate hours worked
				hours_worked = calendar.timegm(time.gmtime()) - emp_dict[positionNumber][0] 

				# emp return message
				print("Thanks you for your work " + emp_dict[positionNumber][2] + ". You are now clocked out.")
				print("You have been paid for " + str(hours_worked) + " seconds.\n")
			
				# write local file with address for pay-emp.js to reference (address, hours_worked)
				with open('/home/ted/dev/balance/local/pay-emp-info.txt', 'w') as emp_address_file:
					emp_address_file.write(emp_dict[positionNumber][1] +  ', ' + str(hours_worked))

				# Executing clock-out-emp.js
				subprocess.call(['node', 'clock-out-emp.js'])

				# Exectuting pay-emp.js
				subprocess.call(['node', 'pay-emp.js'])

				# Resetting clock-in-time to zero
				emp_dict[positionNumber][0] = 0
									
				# Save json dictionary locally 
				with open('/home/ted/dev/balance/local/emp-dict.json', 'w') as json_file:
					json.dump(emp_dict, json_file)


			


