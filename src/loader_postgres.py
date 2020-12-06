from datetime import datetime
import json

from bson.json_util import dumps
from psycopg2 import extensions

from .db_connects import (
    MONGO_DB_CURRENCIES, MONGO_DB_COL_CURRENCIES,
    connect_to_postgres, connect_to_mongodb
)

DEBUG = False


def load_data_into_postgres(conn_postgres, client_mongodb):
    print("Loading into postgres...")
    conn_postgres.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn_postgres.cursor()
    cursor.execute("DROP TABLE IF EXISTS kurz")
    cursor.execute("DROP TABLE IF EXISTS mena")
    cursor.execute(
        "CREATE TABLE mena (zeme varchar(100), "
        "nazev varchar(100), kod varchar(10) primary KEY)"
    )
    cursor.execute(
        "CREATE TABLE kurz (den DATE, kod varchar(10), "
        "CONSTRAINT fk_mena FOREIGN KEY(kod) REFERENCES mena(kod) ON DELETE SET NULL, "
        "normalizovany_kurz FLOAT)"
    )

    cur_db = client_mongodb[MONGO_DB_CURRENCIES]
    cur_col = cur_db[MONGO_DB_COL_CURRENCIES]

    # each currency type
    mena_res = cur_col.find({}, {"currency": 1, "_id": 0}).distinct("currency")
    mena_entries = str(dumps(list(mena_res)))

    # each currency type
    mena_res = cur_col.find({}, {"currency": 1, "_id": 0}).distinct("currency")
    mena_entries = str(dumps(list(mena_res)))
    for mena_item in json.loads(mena_entries):
        cursor.execute("INSERT INTO mena VALUES ('{}', '{}', '{}')".format(
            mena_item["country"],
            mena_item["name"],
            mena_item["code"]
        ))

    entries = str(dumps(list(cur_col.find({}, {"_id": 0}))))
    for item in json.loads(entries):
        date = str(item["date"]["$date"])[:-3]
        cursor.execute("INSERT INTO kurz VALUES ('{}', '{}', '{}')".format(
            datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d"),
            item["currency"]["code"],
            float(item["price"].replace(',', '.')) / int(item["lotSize"])
        ))

    cursor.close()
    conn_postgres.close()


def main():
    conn = connect_to_postgres()
    client = connect_to_mongodb()

    if client is None:
        print("Error while connecting to mongodb")
    elif conn is None:
        print("Error while connecting to postgres/")
    else:
        load_data_into_postgres(conn, client)


if __name__ == '__main__':
    main()
