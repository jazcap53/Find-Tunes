# file: add_while_new.py
# Andrew Jarcho
# 2022-06-26


import psycopg2
from config import config

from connect import connect, do_close_routine


def execute_one_query(conn, query):
    if not conn:
        return

    cur = conn.cursor()
    if not cur:
        print('failed to get cursor in execute_one_query()')
        raise psycopg2.DatabaseError
    try:
        cur.execute(query)
        releases = [item[0] for item in cur.fetchall()]
        return releases
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        do_close_routine(cur, conn)


if __name__ == '__main__':
    conn = connect()
    query = "select discogs_release_id from tu_release order by discogs_release_id;"
    print(execute_one_query(conn, query))

