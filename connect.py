# file: connect.py
# Andrew Jarcho
# 2022-05-31

"""
Holds code that connects with postgresql db.
"""

import psycopg2
from config import config


def connect(*, autocomt: bool=False):
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


def execute_one_query(conn, query) -> any:
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
