import os
import db_connects
from scrape import parse

DEBUG = False


def load_data_into_mongodb(client, scrape_dir):
    print("server version:", client.server_info()["version"])
    print("databases:", client.list_database_names())
    print("loading into mongodb...")

    cur_db = client[db_connects.MONGO_DB_CURRENCIES]
    cur_col = cur_db[db_connects.MONGO_DB_COL_CURRENCIES]
    cur_col.drop()

    res = cur_col.insert_many(parse(scrape_dir))
    print("Successfully loaded: " + len(res.inserted_ids) + " records")


def main():
    scrape_dir = 'scraped/'
    if not os.path.isdir(scrape_dir):
        print("Scrapped folder is missing.")
    else:
        client = db_connects.connect_to_mongodb()
        if client is not None:
            load_data_into_mongodb(client, scrape_dir)
        else:
            print("Error while connecting to mongodb")


if __name__ == '__main__':
    main()
