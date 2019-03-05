import json
from flask import Flask, render_template, flash, redirect, session, logging, request, make_response
from urllib.parse import unquote
from passlib.hash import sha256_crypt 
from bson.objectid import ObjectId
from functools import wraps 
import datetime
import pymongo



from analytics import credit_debit_per
from analytics import category_count_bar

app = Flask(__name__)

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["fintech"]

# ====================================================
# ==================== PAGE ROUTES ===================
# ====================================================


@app.route('/')
def login():
	return render_template('login.html')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

@app.route('/financeplan')
def financeplan():
	return render_template('financeplan.html')

@app.route('/budgetplan')
def budgetplan():
	return render_template('budgetplan.html')

@app.route('/calendar')
def calendar():
	return render_template('calendar.html')

@app.route('/bank')
def bank():
	return render_template('bank.html')
@app.route('/chatbot')
def chatbot():
	return render_template('chatbot.html')

@app.route('/members')
def members():
	return render_template('members.html')

@app.route('/settings')
def settings():
	return render_template('settings.html')


# ===================================================
# ==================== REST APIS ====================
# ===================================================

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
	if request.method == 'POST':	
		try: 

			values = {
				"user_name" 		: request.json['user_name'], 
				"user_email"  		: request.json['user_email'], 
				"user_income" 		: request.json['user_income'], 
				"user_date_create" 	: datetime.datetime.utcnow()
			} 

			db.users.insert_one(values)

		except: 
			app.logger.info("error adding the user")
		return json.dumps({'success':True, 'data': "user_added"}), 200, {'ContentType':'application/json'}

@app.route('/addexpense', methods=['GET', 'POST'])
def addexpense(): 
	if request.method == 'POST':
		try: 

			values = {
				"user_name" 			: request.json['user_name'], 
				"item_name"				: request.json['item_name'], 
				"expense_amnt"  		: request.json['expense_amnt'],
				"expense_date_create" 	: datetime.datetime.utcnow() 
			}

			db.expense.insert_one(values)

		except: 
			app.logger.info("error adding expense")

	return json.dumps({'success':True, 'data': "expense_added"}), 200, {'ContentType':'application/json'}


@app.route('/addneed', methods=['GET', 'POST'])
def addneed():
	if request.method == 'POST':
		try:				
			values = {
				"user_name" 		: request.json['user_name'],
				"item_name"			: request.json['item_name'],  
				"need_amnt"	 		: request.json['need_amnt'], 
				"need_date_create"	: datetime.datetime.utcnow()
			}

			db.needs.insert_one(values)

		except: 
			app.logger.info("error adding need")

	return json.dumps({'success':True, 'data': "need_added"}), 200, {'ContentType':'application/json'}



@app.route('/addsavings', methods=['GET', 'POST'])
def addsavings():
	if request.method == 'POST':
		try:				
			values = {
				"user_name" 			: request.json['user_name'], 
				"item_name"				: request.json['item_name'], 
				"savings_amnt"	 		: request.json['need_amnt'], 
				"savings_date_create"	: datetime.datetime.utcnow()
			}

			db.savings.insert_one(values)

		except: 
			app.logger.info("error adding savings")

	return json.dumps({'success':True, 'data': "savings_added"}), 200, {'ContentType':'application/json'}


@app.route('/get_analytics', methods=['GET', 'POST'])
def get_analytics():
	data = {
		"data_pie_perc" : credit_debit_per(),
		"data_bar_perc": category_count_bar()

	}		

	return json.dumps({'success':True, 'data': data}), 200, {'ContentType':'application/json'}


@app.route('/get_expense_db', methods=['GET', 'POST'])
def get_expense_db():
	bank_db_collection = db.bank_db.find({})
	bank_db_arr = []


	for bank_row in bank_db_collection: 
		bank_db_new = {
				"date" : "", 
				"day" : "", 
				"type" : "", 
				"category" : "", 
				"debit_amount" : "", 
				"credit_amount" : "", 
				"closing_balance" : ""
		}

		bank_db_new['date'] 			= bank_row['date']
		bank_db_new['day'] 				= bank_row['day']
		bank_db_new['type'] 			= bank_row['type']
		bank_db_new['category'] 		= bank_row['category']
		bank_db_new['debit_amount'] 	= bank_row['debit_amount']
		bank_db_new['credit_amount'] 	= bank_row['credit_amount']
		bank_db_new['closing_balance'] 	= bank_row['closing_balance']

		bank_db_arr.append(bank_db_new)
	return json.dumps({'success':True, 'data': bank_db_arr}), 200, {'ContentType':'application/json'}

@app.route('/get_amount_data', methods=['GET', 'POST'])
def get_amount_data():
	saving_coll = db.savings.find({})
	needs_coll  = db.needs.find({})
	expense_coll  = db.expense.find({})

	savings_data = []
	for save_row in saving_coll: 
		single_save_data = {
			"user_name" 				: save_row['user_name'],
			"item_name"					: save_row['item_name'],  
			"savings_amnt"	 			: save_row['savings_amnt'], 
			"savings_date_create"		: str(save_row['savings_date_create'])
		}

		savings_data.append(single_save_data)



	needs_data = []
	for need_row in needs_coll: 
		single_need_data = {
			"user_name" 		: need_row['user_name'],
			"item_name"			: need_row['item_name'],  
			"need_amnt"	 		: need_row['need_amnt'], 
			"need_date_create"	: str(need_row['need_date_create'])
		}

		needs_data.append(single_need_data)


	expense_data = []
	for expense_row in expense_coll:
		single_want_data = {
			"user_name"				: expense_row['user_name'], 
			"item_name"				: expense_row['item_name'], 
			"expense_amnt"  		: expense_row['expense_amnt'], 
			"expense_date_create"	: str(expense_row['expense_date_create'])
		}



	data = {
		"savings_data" : savings_data, 
		"needs_data"   : needs_data, 
		"expense_data" : expense_data
	}
	
	return json.dumps({'success':True, 'data': data}), 200, {'ContentType':'application/json'}



@app.route('/set_debt', methods=['GET', 'POST'])
def set_debt():
	debt_name= request.json["debt_name"]
	debt_balance = request.json["debt_balance"]
	minimum_payment=request.json["minimum_payment"]
	interest_rate=request.json["interest_rate"]

	db.debt.insert_one({
		"debt_name":debt_name,
		"debt_balance":debt_balance,
		"minimum_payment":minimum_payment,
		"interest_rate":interest_rate
				})
	return json.dumps({'success':True, 'data': "success"}), 200, {'ContentType':'application/json'}

@app.route('/get_debt', methods=['GET','POST'])
def get_debt():
	get_debt_collection = db.debt.find({})
	get_debt_arr = []


	for debt_row in get_debt_collection: 
		get_debt_new = {
				"debt_name" : "", 
				"debt_balance" : "", 
				"minimum_payment" : "", 
				"interest_rate" : ""
			
		}

		get_debt_new['debt_name'] 			= debt_row['debt_name']
		get_debt_new['debt_balance'] 				= debt_row['debt_balance']
		get_debt_new['minimum_payment'] 			= debt_row['minimum_payment']
		get_debt_new['interest_rate'] 		= debt_row['interest_rate']


		get_debt_arr.append(get_debt_new)
	return json.dumps({'success':True, 'data': get_debt_arr}), 200, {'ContentType':'application/json'}




if __name__=='__main__':
	app.secret_key = 'jmf57nt4#T'
	app.run(debug=True)



