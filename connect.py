# file: connect.py
# Andrew Jarcho
# 2022-05-31


import psycopg2
from config import config

from scrape import get_all_releases, get_one_release

def connect():
    conn = None
    try:
        params = config()
        print('connecting to the db')
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        
        cur = conn.cursor()
        query_params = get_query_params(itr := get_all_releases())
        while True:
            cur.execute("CALL tu_insert_all(%s, %s, %s, %s, %s)", (query_params))
            query_params = get_query_params(itr)

    except StopIteration:
        print('reached StopIteration in connect()')
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('db connection closed')


def get_query_params(itr):  # itr into scrape::get_all_releases()
    # discogs_release_id, discogs_release_string, track_pos_string, track_title_string, track_duration_string = next(itr)
    query_params = next(itr)
    
    return query_params


if __name__ == '__main__':
    connect()
