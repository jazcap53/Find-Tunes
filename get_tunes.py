#!/usr/bin/env python


# file: get_tunes.py
# Andrew Jarcho
# 2022-06-29


"""
Holds code that needs to connect both with the postgresql database, and with discogs
"""


# NOTE TO SELF: this module must direct traffic. `should_we_continue()` *cannot* be imported by `scrape.py` !!!


import connect
import scrape

#  `number_of_releases_in_collection_at_start + number_of_releases_processed > SELECT COUNT(*) FROM tu_release`
def should_we_continue(n_releases_at_start: int, n_just_processed: int, already_have: list = None) -> bool:
    conn = connect.connect()
    cur = conn.cursor()
    if not cur:
        print('failed to get cursor in `should_we_continue()`')
        raise psycopg2.DatabaseError
    cur.execute("SELECT COUNT(*) FROM tu_release;")
    num_in_db = cur.fetchone()
    breakpoint()  # <========< <========< <========<
    if n_releases_at_start + n_just_processed > num_in_db:  # at least one release has been processed twice
        return False

    # if not already_have:
    #     already_have = connect.execute_one_query(conn := connect.connect(), "select discogs_release_id from tu_release order by discogs_release_id;")
    #     if not already_have:
    #         raise SyntaxError
    return True  # N.Y.I.


def main():
    conn = connect.connect(autocomt=True)
    if not conn.closed:
        connect.execute_query(conn, "CALL tu_insert_all(%s, %s, %s, %s, %s)", scrape.get_all_releases, max_iter=0)
        connect.do_close_routine(conn)


if __name__ == '__main__':
    main()
