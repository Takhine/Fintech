import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["fintech"]

# Percentage of credit / debit pie chart 
def credit_debit_per():
	col = db.bank_db.find({})
	credit_counter = 0
	debit_counter = 0
	none_counter = 0 

	for row in col: 
		if(row['type'].lower() == 'credit'): 
			credit_counter+=1
		if(row['type'].lower() == 'debit'):
			debit_counter+=1
		else:
			none_counter+=1 



	result_dict = {
		"credit_total" : credit_counter,
		"debit_total" : debit_counter, 
		"none_total" : none_counter, 
	}

	return result_dict


def category_count_bar():
	col = db.bank_db.find({})
	shopping_counter = 0
	restaurant_counter = 0
	entertainment_counter = 0
	medical_counter = 0
	travel_counter = 0
	atm_counter = 0
	interest_counter = 0
	rent_counter = 0
	salary_counter = 0
	none_counter = 0 

	for row in col: 
		if(row['category'].lower() == 'shopping'): 
			shopping_counter+=1
		if(row['category'].lower() == 'restaurant'):
			restaurant_counter+=1
		if(row['category'].lower() == 'entertainment'):
			entertainment_counter+=1
		if(row['category'].lower() == 'medical'):
			medical_counter+=1
		if(row['category'].lower() == 'travel'):
			travel_counter+=1
		if(row['category'].lower() == 'atm'):
			atm_counter+=1
		if(row['category'].lower() == 'interest'):
			interest_counter+=1
		if(row['category'].lower() == 'rent'):
			rent_counter+=1
		if(row['category'].lower() == 'salary'):
			salary_counter+=1
		else:
			none_counter+=1 



	result_dict = {
		"shopping_total" : shopping_counter,
		"restaurant_total" : restaurant_counter, 
		"entertainment_total" : entertainment_counter,
		"medical_total" : medical_counter, 
		"travel_total" : travel_counter,
		"atm_total" : atm_counter,
		"interest_total" : interest_counter, 
		"rent_total" : rent_counter,
		"salary_total" : salary_counter,
		"none_total" : none_counter,
	}

	return result_dict

