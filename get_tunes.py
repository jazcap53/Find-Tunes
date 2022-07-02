#!/usr/bin/env python


# file: get_tunes.py
# Andrew Jarcho
# 2022-06-29


"""
Holds code that needs to connect both with the postgresql database, and with discogs
"""


import connect
import scrape


def main():
    conn_0 = connect.connect(silent=True)  # suppress printing conn status
    if not conn_0.closed:
        query_0 = "select discogs_release_id from tu_release order by discogs_release_id;"
        release_list = connect.get_release_list(conn_0, query_0)
        connect.do_close_routine(conn_0, silent=True)
        release_set = set(release_list)

    conn = connect.connect(autocomt=True)
    if not conn.closed:
        query = "CALL tu_insert_all(%s, %s, %s, %s, %s)"
        connect.execute_query(conn, query, scrape.get_all_releases, release_set, max_iter=0)
        connect.do_close_routine(conn)


if __name__ == '__main__':
    main()
