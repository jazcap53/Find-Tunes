# file: queries.py
# Andrew Jarcho
# 2022-06-16


selection_map = {1: 0, 3: 1}

QUERIES = (
    '''
    SELECT r.discogs_release_string
    FROM tu_release r
    JOIN tu_song_release sr
    ON r.release_id = sr.release_id
    JOIN tu_song s
    ON s.song_id = sr.song_id
    WHERE s.song_title = %s;
    ''',
    '''
    SELECT r.discogs_release_string, s.song_title
    FROM tu_release r
    JOIN tu_song_release sr
    ON r.release_id = sr.release_id
    JOIN tu_song s
    ON s.song_id = sr.song_id
    WHERE s.song_title LIKE %s;
    '''
)

def return_query(selection: int) -> str:
    return QUERIES[selection_map[selection]]
