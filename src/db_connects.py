import os
import psycopg2
from pymongo import MongoClient, errors

def connect_to_postgres():
	host="localhost"
	database="postgres"
	user="postgres"
	password="mysecretpassword"
	port="5432"

	lines = tuple(open("postgres_config.txt", 'r'))

	for line in lines:
		if line.startswith("host="):
			host = line[len("host="):len(line)].strip()
		if line.startswith("database="):
			database = line[len("database="):len(line)].strip()
		if line.startswith("user="):
			user = line[len("user="):len(line)].strip()
		if line.startswith("password="):
			password = line[len("password="):len(line)].strip()
		if line.startswith("port="):
			port = line[len("port="):len(line)].strip()


	print("POSTGRES - Connecting with")
	print("Host: " + host)
	print("Database: " + database)
	print("User: " + user)
	print("Password: " + password)
	print("Port: " + port)

	conn = psycopg2.connect(
		host=host,
    	database=database,
    	user=user,
    	password=password,
    	port=port)

	return conn

def connect_to_mongodb():
    host="localhost"
    user=""
    password=""
    port="27017"

    lines = tuple(open("mongodb_config.txt", 'r'))

    for line in lines:
        if line.startswith("host="):
            host = line[len("host="):len(line)].strip()
        if line.startswith("user="):
            user = line[len("user="):len(line)].strip()
        if line.startswith("password="):
            password = line[len("password="):len(line)].strip()
        if line.startswith("port="):
            port = line[len("port="):len(line)].strip()


    print("MONGODB - Connecting with")
    print("Host: " +  host)
    print("User: " + user)
    print("Password: " + password)
    print("Port: " + port)



    try:
        client = MongoClient(
            host = [host + ":" + port],
            serverSelectionTimeoutMS = 3000, 
            username = user,
            password = password,
        )

    except errors.ServerSelectionTimeoutError as err:
        client = None
        database_names = []
        print ("pymongo ERROR:", err)

    return client