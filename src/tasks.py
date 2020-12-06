import pandas as pd

from db_connects import connect_to_postgres

DEBUG = False

def task_A():
    conn = connect_to_postgres()
    cursor = conn.cursor()

    cursor.execute(
        "select kod, normalizovany_kurz from kurz where den = (SELECT MIN(den) from kurz) ORDER BY kod ASC"
    )
    min_hash = dict(cursor)
    cursor.execute(
        "select kod, normalizovany_kurz from kurz where den = (SELECT MAX(den) from kurz) ORDER BY kod ASC"
    )
    res_labels = []
    res_values = []
    for item in cursor:
        diff = min_hash[item[0]] - item[1]
        res_labels.append(item[0])
        res_values.append(diff)

    df = pd.DataFrame({'cur': res_labels, 'val': res_values})
    ax = df.plot.bar(x='cur', y='val', rot=0)

    cursor.close()
    conn.close()


def task_B():
    res_labels = ['AS']
    res_values = [42]
    df = pd.DataFrame({'cur': res_labels, 'val': res_values})
    ax = df.plot.bar(x='cur', y='val', rot=0)


def task_C():
	# SELECT date_part('dow', den::date) as dow, AVG(normalizovany_kurz) FROM kurz GROUP BY dow order by dow;
    pass
