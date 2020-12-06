import psycopg2
from pymongo import MongoClient, errors

DEBUG = False

MONGO_DB_CURRENCIES = "currencies"
MONGO_DB_COL_CURRENCIES = "col_currencies"


def connect_to_postgres():
    host = "localhost"
    database = "postgres"
    user = "postgres"
    password = "mysecretpassword"
    port = "5432"

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

    if DEBUG:
        print("POSTGRES - Connecting with")
        print("Host: " + host)
        print("Database: " + database)
        print("User: " + user)
        print("Password: " + password)
        print("Port: " + port)

    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port)


def connect_to_mongodb():
    host = "localhost"
    user = ""
    password = ""
    port = "27017"

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

    if DEBUG:
        print("MONGODB - Connecting with")
        print("Host: " + host)
        print("User: " + user)
        print("Password: " + password)
        print("Port: " + port)

    try:
        return MongoClient(
            host=[host + ":" + port],
            serverSelectionTimeoutMS=3000,
            username=user,
            password=password,
        )
    except errors.ServerSelectionTimeoutError as err:
        print("pymongo ERROR:", err)
        return None
