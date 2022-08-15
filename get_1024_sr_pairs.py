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


def get_1024_items():
    limit = 1024
    max_offset = get_song_release_ct()
    offset = 0
    batches_printed = 0
    while offset < max_offset:
        query = ("SELECT s.song_id, s.song_title, r.release_id, r.release_string "
                "FROM tu_song s JOIN tu_song_release sr ON s.song_id = sr.song_id "
                "               JOIN tu_release r ON sr.release_id = r.release_id "
                "LIMIT %s OFFSET %s")
        with connect() as conn:
            cur = conn.cursor()
            cur.execute(query, (limit, offset))
            all_items = sorted(cur.fetchall())
        offset += limit
        print(*all_items, sep='\n')
        batches_printed += 1
        print(f'printed batch #{batches_printed}')
        sleep(1)

if __name__ == '__main__':
    get_song_release_ct()
    sleep(3)
    get_1024_items()
