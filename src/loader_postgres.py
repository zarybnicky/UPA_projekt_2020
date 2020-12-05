import os
import psycopg2
import db_connects

def load_data_into_postgres(conn, client):
	print("loading into postgres...")

	# CREATE TABLE meny (
# 	id serial PRIMARY KEY,
# 	země VARCHAR ( 50 ) NOT NULL,
# 	kód VARCHAR ( 50 ) NOT NULL,
# 	měna VARCHAR ( 50 ) UNIQUE NOT NULL,
# 	množství INT NOT NULL,
# 	kurz NUMERIC(3) NOT NULL 
# );

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