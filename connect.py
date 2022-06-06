# file: connect.py
# Andrew Jarcho
# 2022-05-31


import psycopg2
from config import config

from scrape import get_all_releases

def connect():
    conn = None
    try:
        params = config()
        print('connecting to the db')
        conn = psycopg2.connect(**params)
        # breakpoint()
        cur = conn.cursor()
        
        while True:
            query_params_itr = get_query_params(get_all_releases())
            query_params = next(query_params_itr)
        # discogs_release_id, discogs_release_string, 
        # track_pos_str, track_title_str, track_duration_str
            cur.execute("CALL tu_insert_all(%s, %s, %s, %s, %s)", (query_params))

        # conn.commit()

        # cur.close()
    except StopIteration:
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('db connection closed')


def get_query_params(itr):
    # discogs_release_id, discogs_release_string, track_pos_string, track_title_string, track_duration_string = next(itr)
    query_params = next(itr)
    # breakpoint()
    # params = (discogs_release_id, discogs_release_string, track_pos_string, track_title_string, track_duration_string)
    yield query_params


if __name__ == '__main__':
    connect()
