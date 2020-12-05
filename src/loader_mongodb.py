import os
from pymongo import MongoClient, errors
import db_connects
from scrape import parse

def load_data_into_mongodb(client, scrape_dir):
    print ("server version:", client.server_info()["version"])
    database_names = client.list_database_names()

    # print ("databases:", database_names)
    print("loading into mongodb...")

    jsonData = list(parse(scrape_dir))
    # for data in jsonData:
        # print(data)


    cur_db = client[db_connects.MONGO_DB_CURRENCIES]

    cur_col = cur_db[db_connects.MONGO_DB_COL_CURRENCIES]

    # print(cur_col.count())

    cur_col.drop()

    # print(cur_col.count())
    
    x = cur_col.insert_many(jsonData)

    # print(x.inserted_ids)

    print("Successfully loaded: " + str(cur_db.col_currencies.count_documents({})) + "/" + str(len(jsonData)))


if __name__ == '__main__':
    scrape_dir = 'scraped/'
    if not os.path.isdir(scrape_dir):
        print("Scrapped folder is missing.")
    else:
        client = db_connects.connect_to_mongodb()
        if client is not None:
            load_data_into_mongodb(client, scrape_dir)
        else:
            print("Error while connecting to mongodb")
        
        