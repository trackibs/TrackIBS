from flask import Flask, render_template,request,redirect,url_for,jsonify, send_from_directory # For flask implementation
import pymongo
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
import logging
from werkzeug.utils import secure_filename
import os

#client = MongoClient('localhost', 27017)	#Configure the connection to the database
client = MongoClient('mongo', 27017)	#Configure the connection to the database

db = client.tracker	#Select the database
todos = db.entries #Select the collection
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
title = "TrackIBS"
heading = "TrackIBS"
#modify=ObjectId()

UPLOAD_FOLDER = '/trackibs/csv/upload'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def redirect_url():
	return request.args.get('next') or \
		   request.referrer or \
		   url_for('index')

@app.route("/")
def lists ():
	#Display the all Tasks
	todos_l = todos.find().sort("date", pymongo.DESCENDING)
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

# @app.route("/")
@app.route("/food")
def food ():
	#Display the Uncompleted Tasks
	todos_l = todos.find({"tracking":"Food"}).sort("date", pymongo.DESCENDING)
	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)

@app.route("/stool")
def stool ():
	todos_l = todos.find({"tracking":"Stool"}).sort("date", pymongo.DESCENDING)
	import datetime
	import pytz
	# timestamp = datetime.datetime.now(pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%dT%H:%M')
	# logging.debug('+++ timestamp :')
	# logging.debug(timestamp)
	import pandas as pd
	import numpy as np
	from datetime import datetime
	import csv
	import matplotlib
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	import matplotlib.dates as mdates
	import matplotlib.ticker as ticker
	from pandas.io.json import json_normalize
	logging.debug("--- stool ---")
	df = pd.DataFrame(list(todos_l))
	logging.debug(df)
	df['date'] = pd.to_datetime(df['date'])
	df.index = df['date']
	#del df['date']
	df['type1'] = np.where(df['string_value'].str.contains('1'), 1, 0)
	df['type2'] = np.where(df['string_value'].str.contains('2'), 1, 0)
	df['type3'] = np.where(df['string_value'].str.contains('3'), 1, 0)
	df['type4'] = np.where(df['string_value'].str.contains('4'), 1, 0)
	df['type5'] = np.where(df['string_value'].str.contains('5'), 1, 0)
	df['type6'] = np.where(df['string_value'].str.contains('6'), 1, 0)
	df['type7'] = np.where(df['string_value'].str.contains('7'), 1, 0)
	df = df.groupby(df.index.date).sum()

	fig, ax = plt.subplots(nrows=1, sharex=True, figsize=(10,3))
	#fig, ax = plt.subplots(nrows=1, sharex=True )

	bristol_colors = ["#000000", "#333300", "#663300", "#996600", "#cc9900", "#ff9900", "#ff0000"]
	df[['type1','type2','type3','type4','type5','type6','type7']].plot.bar( stacked=True, ax=ax, title='Bristol', color=bristol_colors)
	ax.grid(True, which='major', axis='y')
	ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0), ncol=7, fancybox=False, shadow=False)

	plt.tight_layout()
	plt.savefig('static/bm.png', bbox_inches='tight')
	a3="active"

	todos_l = todos.find({"tracking":"Stool"}).sort("date", pymongo.DESCENDING)
	chart = "bm"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading,c=chart)

@app.route("/medication")
def medication ():
	#Display the Completed Tasks
	todos_l = todos.find({"tracking":"Medication"}).sort("date", pymongo.DESCENDING)
	a4="active"
	import datetime
	import pytz
	# timestamp = datetime.datetime.now(pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%dT%H:%M')
	# logging.debug('+++ timestamp :')
	# logging.debug(timestamp)
	import pandas as pd
	import numpy as np
	from datetime import datetime
	import csv
	import matplotlib
	matplotlib.use('Agg')
	import matplotlib.pyplot as plt
	import matplotlib.dates as mdates
	import matplotlib.ticker as ticker
	from pandas.io.json import json_normalize
	logging.debug("--- stool ---")
	df = pd.DataFrame(list(todos_l))
	logging.debug(df)
	df['date'] = pd.to_datetime(df['date'])
	df.index = df['date']
	#del df['date']
	df['Caltrate']     = np.where(df['string_value'].str.contains('Caltrate'), 1, 0)
	df['Turmeric']     = np.where(df['string_value'].str.contains('Turmeric'), 1, 0)
	df['Metamucil']    = np.where(df['string_value'].str.contains('Metamucil'), 1, 0)
	df['Creon']        = np.where(df['string_value'].str.contains('Creon'), 1, 0)
	df['Imodium']      = np.where(df['string_value'].str.contains('Imodium'), 1, 0)
	df['Multivitamin'] = np.where(df['string_value'].str.contains('Multivitamin'), 1, 0)
	df['Symprove']     = np.where(df['string_value'].str.contains('Symprove'), 1, 0)
	df = df.groupby(df.index.date).sum()
	fig, ax = plt.subplots(nrows=1, sharex=True, figsize=(10,3))
	#fig, ax = plt.subplots(nrows=1, sharex=True )
	df[['Caltrate','Turmeric','Metamucil','Creon','Imodium','Multivitamin','Symprove']].plot.bar( stacked=True, ax=ax, title='Medication')
	ax.grid(True, which='major', axis='y')
	ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0), ncol=7, fancybox=False, shadow=False)
	plt.tight_layout()
	plt.savefig('static/medication.png', bbox_inches='tight')
	todos_l = todos.find({"tracking":"Stool"}).sort("date", pymongo.DESCENDING)
	chart = "medication"
	return render_template('index.html',a4=a4,todos=todos_l,t=title,h=heading,c=chart)

@app.route("/exercise")
def exercise ():
	#Display the Completed Tasks
	todos_l = todos.find({"tracking":"Workout"}).sort("date", pymongo.DESCENDING)
	a5="active"
	return render_template('index.html',a5=a5,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	# Re-directed URL i.e. PREVIOUS URL from where it came into this one

#	if(str(redir)=="http://localhost:5000/search"):
#		redir+="?key="+id+"&refer="+refer

	return redirect(redir)

#@app.route("/add")
#def add():
#	return render_template('add.html',h=heading,t=title)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	date=request.values.get("date")
	tracking=request.values.get("tracking")
	string_value=request.values.get("string_value")
	numerical_value=request.values.get("numerical_value")
	additional_information=request.values.get("additional_information")
	todos.insert({ "date":date, "tracking":tracking, "string_value":string_value,  "numerical_value":numerical_value, "additional_information":additional_information, "done":"no"})
	return redirect("/")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "date":date, "tracking":tracking, "string_value":string_value,  "numerical_value":numerical_value, "additional_information":additional_information }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/about")
def about():
	return render_template('credits.html',t=title,h=heading)

# @app.route("/upload")
# def upload():
# 	return render_template('upload.html',t=title,h=heading)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
# 	    import pandas as pd
# 	    import json
# 	    filepath = 'export.csv'
# 	    mng_client = pymongo.MongoClient('localhost', 27017)
# 	    mng_db = mng_client['tracker']
# 	    collection_name = 'entries'
# 	    db_cm = mng_db[collection_name]
# 	    cdir = os.path.dirname(__file__)
# 	    file_res = os.path.join(cdir, filepath)
# 	    data = pd.read_csv(file_res)
# 	    data.columns = data.columns.str.strip()
# 	    data.columns = data.columns.str.replace('\s+', '_')
# 	    data.columns = data.columns.str.lower()
# 	    data_json = json.loads(data.to_json(orient='records'))
# 	    db_cm.remove()
# 	    db_cm.insert(data_json)
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        submitted_file = request.files['file']
        if submitted_file and allowed_filename(submitted_file.filename):
            import sys
            import pandas as pd
            import pymongo
            import json
            import os
            filename = secure_filename(submitted_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            submitted_file.save(file_path)
            mng_client = pymongo.MongoClient('mongo', 27017)
            mng_db = mng_client['tracker']
            collection_name = 'entries'
            db_cm = mng_db[collection_name]
            cdir = os.path.dirname(__file__)
            data = pd.read_csv(file_path)
            data.columns = data.columns.str.strip()
            data.columns = data.columns.str.replace('\s+', '_')
            data.columns = data.columns.str.lower()
            data_json = json.loads(data.to_json(orient='records'))
            db_cm.remove()
            db_cm.insert(data_json)
            return redirect(url_for('index', filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

# @app.route("/upload", methods=['POST'])
# def import_content(filepath):
# 	import sys
# 	import pandas as pd
# 	import pymongo
# 	import json
# 	import os
# 	file_path=request.values.get("file_path")
# 	mng_client = pymongo.MongoClient('localhost', 27017)
# 	mng_db = mng_client['tracker']
# 	collection_name = 'entries'
# 	db_cm = mng_db[collection_name]
# 	cdir = os.path.dirname(__file__)
# 	file_res = os.path.join(cdir, filepath)
# 	data = pd.read_csv(file_path)
# 	data.columns = data.columns.str.strip()
# 	data.columns = data.columns.str.replace('\s+', '_')
# 	data.columns = data.columns.str.lower()
# 	data_json = json.loads(data.to_json(orient='records'))
# 	db_cm.remove()
# 	db_cm.insert(data_json)
# 	return redirect("/")


if __name__ == "__main__":
	app.run(debug=True)
# Careful with the debug mode..
