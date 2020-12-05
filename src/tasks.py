import os
import db_connects
from psycopg2 import extensions, connect
from pymongo import MongoClient, errors
from bson.json_util import dumps
import json
from datetime import datetime
import pandas as pd

DEBUG = False

def task_A():
	conn_postgres = db_connects.connect_to_postgres()
	if conn_postgres is None:
		print("Error while connecting to postgres")
		exit(1)

	psqlCursor = conn_postgres.cursor();

	psqlStmt = "select kod, normalizovany_kurz from kurz where den = (SELECT MIN(den) from kurz) ORDER BY kod ASC"
	psqlCursor.execute(psqlStmt);
	
	min_arr = psqlCursor.fetchall() 	

	psqlStmt = "select kod, normalizovany_kurz from kurz where den = (SELECT MAX(den) from kurz) ORDER BY kod ASC"
	psqlCursor.execute(psqlStmt);
	
	max_arr = psqlCursor.fetchall() 	

	# print(min_arr)
	# print(max_arr)
		
	min_hash = dict(min_arr)

	res_labels = []
	res_values = []

	for item in max_arr:
		dif = min_hash[item[0]] - item[1]
		res_labels.append(item[0])
		res_values.append(dif)

	if DEBUG:
		print(res_labels)
		print(res_values)

	df = pd.DataFrame({'cur':res_labels, 'val':res_values})
	ax = df.plot.bar(x='cur', y='val', rot=0)

	psqlCursor.close();

	conn_postgres.close();