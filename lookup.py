# file: lookup.py
# andrew jarcho
# 2022-06-01


from config import config
import psycopg2

from queries import return_query
from scrape import cleanup_title_string


def lookup() -> None:
    search_type = select_search_type()
    search_string = get_search_string(search_type)
    if search_string == 'N.Y.I.':
        print(search_string)
        search_string = ''
    if not search_string:
        print('Goodbye!!!')
        return
    query = return_query(search_type)
    call_db(query, search_string)


def select_search_type() -> int:
    """
    Return an int, selected by the user, representing the search type
    """
    selection = int(input('\tEnter 1 to search by song title,\n'
                          '\tEnter 2 to search by band/leader name,\n'
                          '\tEnter 3 to search by partial song title,\n'
                          '\tEnter 0 to quit:\n').strip() or '0')
    while not 0 <= selection < 4:
        selection = int(input('\t').strip())
    return selection


def get_search_string(selection: int) -> str:
    """
    Return a str representing the item the user is searching for
    """
    if not selection:
        search_string = ''
    elif selection == 1:
        yes_no = None
        while not yes_no or yes_no[0] not in 'ynq':
            title = input('What song title do you want to look up? ')
            search_string = cleanup_title_string(title).lower()
            if search_string:
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
    elif selection == 3:
        yes_no = None
        while not yes_no or yes_no[0] not in 'ynq':
            title = input('What partial song title do you want to look up? ')
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
        if search_string:
            search_string = '%' + search_string + '%'
    return search_string


def call_db(query,  query_param):
    conn = None
    try:
        params = config()
        print('\nconnecting to the db')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        cur.execute(query, (query_param,))
        results = cur.fetchall()
        if not results:
            print(f'\n{query_param} not found in the db\n')
        else:
            print(f'\n{query_param} found in:')
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
