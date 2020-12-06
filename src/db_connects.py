from os.path import dirname, realpath, join

import psycopg2
from pymongo import MongoClient, errors

DEBUG = False

MONGO_DB_CURRENCIES = "currencies"
MONGO_DB_COL_CURRENCIES = "col_currencies"


def connect_to_postgres():
    config = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "mysecretpassword",
        "port": "5432",
    }

    lines = open(join(dirname(realpath(__file__)), "postgres_config.txt"), 'r')
    config.update(dict(line.strip().split('=') for line in lines))

    if DEBUG:
        print("POSTGRES - Connecting to ", config)

    return psycopg2.connect(
        host=config['host'],
        database=config['database'],
        user=config['user'],
        password=config['password'],
        port=config['port']
    )


def connect_to_mongodb():
    config = {
        "host": "localhost",
        "user": "",
        "password": "",
        "port": "27017",
    }

    lines = open(join(dirname(realpath(__file__)), "mongodb_config.txt"), 'r')
    config.update(dict(line.strip().split('=') for line in lines))

    if DEBUG:
        print("MONGODB - Connecting to ", config)

    return MongoClient(
        host=["%s:%s" % (config['host'], config['port'])],
        serverSelectionTimeoutMS=3000,
        username=config['user'],
        password=config['password'],
    )
