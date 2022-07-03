# file: connect.py
# Andrew Jarcho
# 2022-05-31

"""
Holds code that connects with postgresql db.
"""

import psycopg2
from config import config


def connect(*, autocomt: bool=False, silent: bool=False):
    conn = None
    try:
        conn_params = config()
        if not silent:
            print('Connecting to the db.')
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = autocomt
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        do_close_routine(conn)


def get_release_list(conn, query) -> any:
    if not conn:
        return
    cur = conn.cursor()
    if not cur:
        print('Failed to get cursor in get_release_list().')
        raise psycopg2.DatabaseError
    try:
        # query: "select discogs_release_id from tu_release order by discogs_release_id;"
        cur.execute(query)
        releases = [item[0] for item in cur.fetchall()]
        return releases
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        do_close_routine(cur, conn, silent=True)


def execute_query(conn, query, iter_f, release_set, args, *, max_iter=0):
    if not conn:
        return
    prev_release_id = 0
    num_processed = 0
    release_set_initial_len = len(release_set)
    cur = conn.cursor()
    if not cur:
        print('Failed to get cursor in execute_query().')
        raise psycopg2.DatabaseError
    new_iter = iter_f(max_iter)
    try:
        while True:
            query_params = next(new_iter)
            release_id = query_params[0]
            if release_id != prev_release_id:
                num_processed += 1
                prev_release_id = release_id
            if release_id not in release_set:
                release_set.add(release_id)
            
            cur.execute(query, (query_params))
            if not args.keep_going and release_set_initial_len + num_processed > len(release_set):  # !!!
                break
    except StopIteration:
        # print('Reached StopIteration in execute_query().')
        do_close_routine(cur, conn)
    except (Exception, psycopg2.DatabaseError):
        raise
    finally:
        show_new_item_count(len(release_set), release_set_initial_len)
        do_close_routine(cur, conn)


def show_new_item_count(cur_len, initial_len):
    new_items = cur_len - initial_len
    if not new_items:
        print("No", end=' ')
    else:
        print(new_items, end=' ')
    print('new items processed.\n')


def do_close_routine(cur=None, conn=None, *, silent=False):
    if cur and not cur.closed:
        cur.close()
        if not silent:
            print('Cursor closed.')
    if conn and not conn.closed:
        conn.close()
        if not silent:
            print('Db connection closed.')
