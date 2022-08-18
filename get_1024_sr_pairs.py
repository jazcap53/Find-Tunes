# file: get_1024_sr_pairs.py
# andrew jarcho
# 2022-08-15

from time import sleep

from back_end.connect import connect, get_release_list, do_close_routine


def get_song_release_ct():
    query= "SELECT COUNT(*) FROM tu_song_release"
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(query)
        n_song_releases = cur.fetchone()[0]
    print(f'I count {n_song_releases} song-release pairs')
    return n_song_releases


def get_item_batches():
    limit = 1024
    max_offset = get_song_release_ct()
    offset = 0
    batches_looked_at = 0
    query = ("SELECT s.song_id, s.song_title, r.release_id, r.release_string "
             "FROM tu_song s JOIN tu_song_release sr ON s.song_id = sr.song_id "
             "               JOIN tu_release r ON sr.release_id = r.release_id "
             "LIMIT %s OFFSET %s")
    with connect() as conn:
        while offset < max_offset:
            all_items = get_one_batch(conn, query, limit, offset)
            if not all_items:
                return
            offset += limit
            print(*all_items, sep='\n')
            batches_looked_at += 1
            print(f'looked at batch #{batches_looked_at}')
            print(f'LEN ALL ITEMS IS {len(all_items)}')
            sleep(1)


def get_one_batch(conn, query, limit, offset):
    with conn.cursor() as cur:
        cur.execute(query, (limit, offset))
        all_items = sorted(cur.fetchall())
        cur.close()
    return all_items


if __name__ == '__main__':
    get_song_release_ct()
    sleep(3)
    get_item_batches()
