import csv, os

def user_interactions():
	
	#File to read in:
	folder = 'data' #Folder located within the main dir that contains the files
	date = '141214' #The Date of the File you would like to read in format: "YYMMDD"
	kiosk_name = 'KIOSK0001' #The Kiosk that you are interested in looking at format: "KIOSKXXXX"
	path = './'+folder+'/'+date+'_'+kiosk_name+'.csv'

	#read text file into variable
	with open(path, 'r') as f:
		read_data = f.read()
	
	#break variable into array
	reader = csv.reader(read_data.split('\n'), delimiter=',') #Turn read_data into an Array by splitting ","
	results = []
	for row in reader:
		try:
			test_var = row[1].split()[0]
			if test_var != "Multiple" and test_var != "blank" and test_var !=  "---Printer" and test_var !=  "No" and test_var !=  "Touch" and test_var !=  "Swapping" and test_var !=  "Hourly":
				results.append(row)	
#				print row
		except Exception as e:
#			print "----------------------ERROR-------------------------"
#			print e
#			print "----------------------END ERROR---------------------"
			pass
	
	#Identify interactions
	#Interactions are separted by either >5 min or timeout
	tempArray = []
	compoundArray = []
	for i in range(0,len(results)-1):
	#	print i
		try:
			#time stamp values
#			print "Test"
#			print results[i][6]
#			print results[i][6].split(' ')[1]

			timeStampRawNow = results[i][6].split(' ')[1].split('.')[0].split(':')
			timeStampRawThen = results[i+1][6].split(' ')[1].split('.')[0].split(':')
			timeStampNow = int(timeStampRawNow[0])*60 + int(timeStampRawNow[1])
			timeStampThen = int(timeStampRawThen[0])*60 + int(timeStampRawThen[1])
			
			tempArray.append(results[i][1].replace('  ','').split(',')[0])
			
			#time stamp calculations
			interactionTime = abs(timeStampNow - timeStampThen)
#			print interactionTime
#			print i
#			print "length = " + str(len(results)-1)

			if interactionTime > 5 or interactionTime > 1435 or i == len(results)-2:
			
				#prepend lines with the following phrases
				if "Successful coupon: pennytest" in tempArray or "Successful coupon: luggage" in tempArray or "Successful coupon: connections" in tempArray:	
					tempArray.insert(0,str(len(tempArray)))
					tempArray.insert(0,str(interactionTime))
					tempArray.insert(0,"TESTING")
					compoundArray.append(tempArray)
					tempArray = []		
				elif "credit" in tempArray:	
					tempArray.insert(0,str(len(tempArray)))
					tempArray.insert(0,str(interactionTime))
					tempArray.insert(0,"PURCHASE")
					compoundArray.append(tempArray)
					tempArray = []
				else:
					tempArray.insert(0,str(len(tempArray)))
					tempArray.insert(0,str(interactionTime))
					tempArray.insert(0,"INTERACTION")
					compoundArray.append(tempArray)
					tempArray = []
				
		except Exception as e:
			print "----------------------ERROR-------------------------"
			print e
			print "----------------------END ERROR---------------------"
#			pass
	
	
	
	emptyCount = 0
	interactionCount = 0
	try:
		os.remove('cleaned.txt')
	except OSError:
		pass
	for i in range(0,len(compoundArray)):
		if compoundArray[i][0] == "Hourly restart":
			emptyCount += 1
		else:
			interactionCount += 1
			# print "Interaction " + str(interactionCount) + " ----------------------------------------"
			# print compoundArray[i]
			# print ""
			# print ""
			with open('cleaned.txt', 'a') as the_file:
				myString = "~".join(compoundArray[i] )
				the_file.write(myString)
				the_file.write('\n')
			
	print "At %s On %s there were %s Interactions" %(kiosk_name, date, interactionCount)



	
	
	
	
	

	
# Start execution here!
if __name__ == '__main__':
	user_interactions()