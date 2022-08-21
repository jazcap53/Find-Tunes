# file: get_1024_sr_pairs.py
# andrew jarcho
# 2022-08-15

from time import sleep

from back_end.connect import connect, get_release_list, do_close_routine
from back_end.add_mp3s import get_mp3_set


DB_BATCH_SIZE = 1024


def get_song_release_ct():
    """Get and return the number of tu_song_release items in the db"""
    query= "SELECT COUNT(*) FROM tu_song_release"
    with connect(silent=True) as conn:
        cur = conn.cursor()
        cur.execute(query)
        n_song_releases = cur.fetchone()[0]
    print(f'I count {n_song_releases} song-release pairs in db')
    return n_song_releases


def get_item_batches(directory: str ='/home/jazcap53/Music/misc_mp3s') -> set:
    limit = DB_BATCH_SIZE
    max_offset = get_song_release_ct()
    offset = 0
    batches_looked_at = 0
    song_and_file_names = list(get_mp3_set(directory))
    songs_found_in_db = set()
    query = ("SELECT s.song_id, s.song_title, r.release_id, r.release_string "
             "FROM tu_song s JOIN tu_song_release sr ON s.song_id = sr.song_id "
             "               JOIN tu_release r ON sr.release_id = r.release_id "
             "LIMIT %s OFFSET %s")
    with connect(silent=True) as conn:
        while offset < max_offset:
            all_items = get_one_batch(conn, query, offset)
            if not all_items:
                raise ValueError
            songs_found_in_db |= find_songs_in_db(all_items, song_and_file_names)
            offset += limit
            batches_looked_at += 1
    print(f'Checked {batches_looked_at} batches of <= {DB_BATCH_SIZE} db items')
    print(f'Found {len(songs_found_in_db)} songs from {directory} in db')
    print(*sorted(songs_found_in_db), sep='\n')
    return songs_found_in_db


def find_songs_in_db(all_items: list[tuple], song_and_file_names: list[tuple]):
    """
    Return a set containing a (song name, file name) tuple for each
    song from the file system that is found in the database.

    parameter: all_items --
               DB_BATCH_SIZE (song id, song title,
                              release id, release string) tuples
    parameter: song_and_file_names --
               a (song name, file name) tuple for each song found in
               the directory being examined
    """
    song_names_only = [safn[0] for safn in song_and_file_names]
    songs_found_in_db = set()
    for item in all_items:
        if item[1] in song_names_only:
            for song_and_file in song_and_file_names:
                if song_and_file[0] == item[1]:
                    songs_found_in_db.add(song_and_file)
    return songs_found_in_db


def get_one_batch(conn, query, offset) -> list:
    """Get and return a batch of up to DB_BATCH_SIZE results from db connection"""
    with conn.cursor() as cur:
        cur.execute(query, (DB_BATCH_SIZE, offset))
        all_items = sorted(cur.fetchall())
        cur.close()
    return all_items


if __name__ == '__main__':
    # get_song_release_ct()
    # sleep(3)
    get_item_batches()
