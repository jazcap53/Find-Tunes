# file: connect.py
# Andrew Jarcho
# 2022-05-31


import psycopg2
from config import config

from scrape import get_all_releases

def connect(*, autocomt: bool =False):
    conn = None
    try:
        conn_params = config()
        print('connecting to the db')
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = autocomt
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        do_close_routine(conn)


def execute_query(conn, query, iter_f, *, max_iter=0):
    if not conn:
        return

    cur = conn.cursor()
    if not cur:
        print('failed to get cursor in execute_query()')
        raise psycopg2.DatabaseError
    new_iter = iter_f(max_iter)
    try:
        while True:
            query_params = next(new_iter)
            cur.execute(query, (query_params))
    except StopIteration:
        print('reached StopIteration in execute_query()')
        do_close_routine(cur, conn)
    except (Exception, psycopg2.DatabaseError):
        raise
    finally:
        do_close_routine(cur, conn)


def do_close_routine(cur=None, conn=None):
    if cur and not cur.closed:
        cur.close()
        print('cursor closed')
    if conn and not conn.closed:
        conn.close()
        print('db connection closed')


if __name__ == '__main__':
    conn = connect(autocomt=True)
    if not conn.closed:
        execute_query(conn, "CALL tu_insert_all(%s, %s, %s, %s, %s)", get_all_releases, max_iter=1)
        do_close_routine(conn)
