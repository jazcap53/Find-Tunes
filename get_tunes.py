#!/usr/bin/env python


# file: get_tunes.py
# Andrew Jarcho
# 2022-06-29


"""
Holds code that needs to connect both with the postgresql database, and with discogs
"""

import argparse
import unicodedata

from back_end import connect
from back_end import scrape


def get_args():
    parser = argparse.ArgumentParser(description='Process Discogs releases.')
    parser.add_argument('-k', '--keep-going', action='store_true', default=False, help='Process all releases in collection.')
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    conn_0 = connect.connect(silent=True)  # suppress printing conn status
    if not conn_0.closed:
        query_0 = "SELECT discogs_release_id FROM tu_release ORDER BY discogs_release_id;"
        release_list = connect.get_release_list(conn_0, query_0)
        connect.do_close_routine(conn_0, silent=True)
        for ix, val in enumerate(release_list):
            release_list[ix] = scrape.normalize_str(val)
        release_set = set(release_list)

    conn = connect.connect(autocomt=True)
    if not conn.closed:
        # query = "CALL tu_insert_all(%s, %s, %s, %s, %s)"
        query = "CALL tu_insert_all(%s, %s, %s)"  # NEW
        connect.execute_query(conn, query, scrape.get_all_releases, release_set, args, max_iter=0)
        connect.do_close_routine(conn)


if __name__ == '__main__':
    main()
