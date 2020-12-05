import os
import db_connects
from psycopg2 import extensions, connect
from pymongo import MongoClient, errors
from bson.json_util import dumps
import json
from datetime import datetime

def load_data_into_postgres(conn_postgres, client_mongodb):
	print("loading into postgres...")
	conn_postgres.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT);

	psqlCursor = conn_postgres.cursor();

	tableName = "news_stories_archive";

	dropTableStmt = "DROP TABLE IF EXISTS kurz;"

	psqlCursor.execute(dropTableStmt);

	dropTableStmt = "DROP TABLE IF EXISTS mena;"

	psqlCursor.execute(dropTableStmt);


	dropTableStmt = "CREATE TABLE mena (zeme varchar(100), nazev varchar(100), kod varchar(10) primary KEY)"

	psqlCursor.execute(dropTableStmt);

	dropTableStmt = "CREATE TABLE kurz (den DATE, kod varchar(10), CONSTRAINT fk_mena FOREIGN KEY(kod) REFERENCES mena(kod) ON DELETE SET NULL, normalizovany_kurz FLOAT);"

	psqlCursor.execute(dropTableStmt);


	cur_db = client[db_connects.MONGO_DB_CURRENCIES]

	cur_col = cur_db[db_connects.MONGO_DB_COL_CURRENCIES]


	# each currency type
	mena_res = cur_col.find({},{ "currency": 1, "_id": 0 }).distinct("currency")
	mena_entries = str(dumps(list(mena_res)))
	mena_json_data = json.loads(mena_entries)

	for mena_item in mena_json_data:
		country = mena_item["country"]
		code =  mena_item["code"]
		name = mena_item["name"]
		insertRowStmt = "INSERT INTO mena VALUES ('{}', '{}', '{}');".format(country,name,code)
		psqlCursor.execute(insertRowStmt);
		# print(mena_item)

	# cursor = cur_col.find()
	cursor = cur_col.find({},{ "_id": 0 })
	 
	entries = str(dumps(list(cursor)))

	json_data = json.loads(entries)
	
	# print(json_data)	

	total_count = len(json_data)

	count = 0

	for item in json_data:  
		currency_code = item["currency"]["code"]
		price = item["price"]
		lotSize = item["lotSize"]
		date = str(item["date"]["$date"])[:-3]
		normalized = float(price.replace(',','.')) / int(lotSize)
		# print(normalized)
		
		date_time = datetime.fromtimestamp(int(date))
	
		date_out = date_time.strftime("%Y-%m-%d")
		
		insertRowStmt = "INSERT INTO kurz VALUES ('{}', '{}', '{}');".format(date_out,currency_code,normalized)
		psqlCursor.execute(insertRowStmt);
		count += 1
		
	psqlCursor.close();

	conn_postgres.close();

	print("Successfully loaded: " + str(count) + "/" + str(total_count))
	
if __name__ == '__main__':
	conn = db_connects.connect_to_postgres()
	client = db_connects.connect_to_mongodb()

	if client is not None and conn is not None:
		load_data_into_postgres(conn, client)
	else:
		if conn is None:
			print("Error while connecting to postgres/")
		elif client is None:
			print("Error while connecting to mongodb")