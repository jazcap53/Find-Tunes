# file: lookup.py
# andrew jarcho
# 2022-06-01


import psycopg2

from config import config
from scrape import cleanup_title_string


def lookup():
    search_type = select_search()
    search_string = get_search_string(search_type)
    if search_string == 'N.Y.I.':
        print(search_string)
        search_string = ''
    if not search_string:
        print('Goodbye!!!')
        return
    conn = None
    try:
        params = config()
        print('\nconnecting to the db')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        query_param = search_string
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
            print(f'\n{search_string} not found in the db\n')
        else:
            print(f'\n{search_string} found in:')
            for result in results:
                print(result)
            print()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('db connection closed')


def select_search():
    selection = int(input('\tEnter 1 to search by song title,\n'
                          '\tEnter 2 to search by band/leader name,\n'
                          '\tEnter 0 to quit:\n').strip())
    while not 0 <= selection < 3:
        selection = int(input('\t').strip())
    return selection


def get_search_string(selection: int):
    if not selection:
        search_string = ''
    elif selection == 1:
        yes_no = None
        while not yes_no or yes_no[0] not in 'ynq':
            title = input('What song title do you want to look up? ')
            search_string = cleanup_title_string(title).lower()
            yes_no = input(f'I will search for \'{search_string}\', ok? [Y/n])').strip().lower()
            if not yes_no:
                yes_no = 'y'
            elif yes_no == 'y':
                pass
            elif yes_no == 'n':
                yes_no = None
            elif yes_no == 'q':
                search_string = ''
    elif selection == 2:
        search_string = 'N.Y.I.'
    return search_string



if __name__ == '__main__':
    lookup()
