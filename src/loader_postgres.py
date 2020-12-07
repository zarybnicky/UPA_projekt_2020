from datetime import datetime
import json

from bson.json_util import dumps
from psycopg2 import extensions

from db_connects import (
    MONGO_DB_CURRENCIES, MONGO_DB_COL_CURRENCIES,
    connect_to_postgres, connect_to_mongodb
)

DEBUG = False


def load_data_into_postgres(conn, client):
    print("Loading into postgres...")
    conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS kurz")
    cursor.execute("DROP TABLE IF EXISTS mena")
    cursor.execute("CREATE TABLE mena (zeme varchar(100), nazev varchar(100), kod varchar(10) primary KEY)")
    cursor.execute(
        "CREATE TABLE kurz (den DATE, kod varchar(10), "
        "CONSTRAINT fk_mena FOREIGN KEY(kod) REFERENCES mena(kod) ON DELETE SET NULL, "
        "normalizovany_kurz FLOAT)"
    )

    collection = client[MONGO_DB_CURRENCIES][MONGO_DB_COL_CURRENCIES]

	print(collection.find({}, {"currency": 1, "_id": 0}).distinct("currency"))

    # each currency type
    for mena_item in collection.find({}, {"currency": 1, "_id": 0}).distinct("currency"):
        cursor.execute("INSERT INTO mena VALUES ('{}', '{}', '{}')".format(
            mena_item["country"],
            mena_item["name"],
            mena_item["code"]
        ))

    count = 0
    for item in collection.find({}, {"_id": 0}):
        cursor.execute("INSERT INTO kurz VALUES ('{}', '{}', '{}')".format(
            item["date"].strftime("%Y-%m-%d"),
            item["currency"]["code"],
            float(item["price"].replace(',', '.')) / int(item["lotSize"])
        ))
        count += 1

    cursor.close()
    conn.close()

    print("Successfully loaded: %s records" % count)


def main():
    conn = connect_to_postgres()
    client = connect_to_mongodb()
    load_data_into_postgres(conn, client)


if __name__ == '__main__':
    main()
