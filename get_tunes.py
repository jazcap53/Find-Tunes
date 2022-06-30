#!/usr/bin/env python


# file: get_tunes.py
# Andrew Jarcho
# 2022-06-29


"""
Holds code that needs to connect both with the postgresql database, and with discogs
"""


import connect
import scrape


def should_we_continue(n_releases: int, already_have: list = []) -> bool:
    if not already_have:
        already_have = connect.execute_one_query(conn := connect.connect(), "select discogs_release_id from tu_release order by discogs_release_id;")
        if not already_have:
            raise SyntaxError
    return True  # N.Y.I.


if __name__ == '__main__':
    conn = connect.connect(autocomt=True)
    if not conn.closed:
        connect.execute_query(conn, "CALL tu_insert_all(%s, %s, %s, %s, %s)", scrape.get_all_releases, max_iter=0)
        connect.do_close_routine(conn)
    else:
        print('well, we made it this far, anyway')
