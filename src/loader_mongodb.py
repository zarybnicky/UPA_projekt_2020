import os

from db_connects import MONGO_DB_CURRENCIES, MONGO_DB_COL_CURRENCIES, connect_to_mongodb
from scrape import parse

DEBUG = False


def load_data_into_mongodb(client, scrape_dir):
    print("Loading into mongodb...")

    cur_db = client[MONGO_DB_CURRENCIES]
    cur_col = cur_db[MONGO_DB_COL_CURRENCIES]
    cur_col.drop()

    res = cur_col.insert_many(parse(scrape_dir))
    print("Successfully loaded: %s records" % len(res.inserted_ids))


def main():
    scrape_dir = 'scraped/'
    if not os.path.isdir(scrape_dir):
        print("Scrapped folder is missing.")
    else:
        client = connect_to_mongodb()
        load_data_into_mongodb(client, scrape_dir)


if __name__ == '__main__':
    main()
