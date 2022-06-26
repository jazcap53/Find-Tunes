# file: connect.py
# Andrew Jarcho
# 2022-05-31


import psycopg2
from config import config

from scrape import get_all_releases, get_one_release

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
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('db connection closed')


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
            # breakpoint()
            cur.execute(query, (query_params))
            # query_params = next(new_iter)
    except StopIteration:
        print('reached StopIteration in execute_query()')
        cur.close()
    except (Exception, psycopg2.DatabaseError):
        raise
    finally:
        if conn is not None:
            conn.close()
            print('db connection closed')


if __name__ == '__main__':
    conn = connect(autocomt=True)
    if not conn.closed:
        # breakpoint()
        execute_query(conn, "CALL tu_insert_all(%s, %s, %s, %s, %s)", get_all_releases, max_iter=1)
        conn.close()
