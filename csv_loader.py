import csv 
import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["fintech"]



index = 0
with open('chatbot.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		if index != 0:
			#add to the database
			db.bank_db.insert_one({
				"date" : row[0],
				"day"  : row[1], 
				"type" : row[2], 
				"category" : row[3], 
				"debit_amount" : row[4], 
				"credit_amount" : row[5], 
				"closing_balance" : row[6]

			})
		index+=1
csvFile.close()