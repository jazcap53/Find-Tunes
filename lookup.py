
import psycopg2

from config import config
from scrape import cleanup_title_string


def lookup():
    title = input('What song do you want to look up? ')
    
    title = cleanup_title_string(title)
    
    yes_no = None
    while not yes_no or yes_no[0] not in 'ynq':
        yes_no = input(f'I will search for \'{title.lower()}\', ok? [Y/n])').strip().lower()
        if not yes_no:
            yes_no = 'y'
            break

    conn = None
    try:
        params = config()
        print('\nconnecting to the db')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query_param = title.lower()
        query = '''
        SELECT r.discogs_release_string
        FROM tu_release r
        JOIN tu_song_release sr
        ON r.release_id = sr.release_id
        JOIN tu_song s
        ON s.song_id = sr.song_id
        WHERE s.song_title = %s;
        '''
        cur.execute(query, (query_param,))
        results = cur.fetchall()
        if not results:
            print(f'\n{title.lower()} not found in the db\n')
        else:
            print(f'\n{title.lower()} found in:')
            for result in results:
                print(result)
            print()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('db connection closed')


if __name__ == '__main__':
    lookup()
