import db_connects
import pandas as pd

DEBUG = False

def task_A():
    conn_postgres = db_connects.connect_to_postgres()
    if conn_postgres is None:
        print("Error while connecting to postgres")
        exit(1)

    cursor = conn_postgres.cursor()

    cursor.execute(
        "select kod, normalizovany_kurz from kurz where den = (SELECT MIN(den) from kurz) ORDER BY kod ASC"
    )
    min_arr = cursor.fetchall()

    cursor.execute(
        "select kod, normalizovany_kurz from kurz where den = (SELECT MAX(den) from kurz) ORDER BY kod ASC"
    )
    max_arr = cursor.fetchall()

    min_hash = dict(min_arr)

    res_labels = []
    res_values = []

    for item in max_arr:
        dif = min_hash[item[0]] - item[1]
        res_labels.append(item[0])
        res_values.append(dif)

    if DEBUG:
        print(res_labels)
        print(res_values)

    df = pd.DataFrame({'cur': res_labels, 'val': res_values})
    ax = df.plot.bar(x='cur', y='val', rot=0)

    cursor.close()
    conn_postgres.close()
