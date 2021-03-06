# file: scrape.py
# andrew jarcho
# 2022-05-27

"""
Holds code that connects with Discogs
"""

import string
from time import sleep
import unicodedata
import urllib.parse

from bs4 import BeautifulSoup
import requests

    
def get_all_releases(max_page: int = 0):
    if max_page < 0:
        print('Error: max_page is < 0.')
        return
    pg = 1
    all_releases = []
    outer_resp = requests.get(f'https://www.discogs.com/user/jazcap53/collection?page={pg}')
    print(f'\nGetting page {pg}: ', end='')
    got_release_ct = False

    itr = None
    while outer_resp.status_code == 200:
        printed_release_ct = False
        outer_soup = BeautifulSoup(outer_resp.text, 'html.parser')
        all_strongs = outer_soup.find_all('strong')
        for strong in all_strongs:
            if not strong.get('class'):
                continue
            release = strong['class']
            if not got_release_ct:
                n_releases_at_start = int(strong.string.partition(' of ')[2])
                got_release_ct = True
            if not printed_release_ct:
                print(f'item(s) {strong.string.strip()}.')
                printed_release_ct = True

        for link in outer_soup.find_all('a'):
            destination = link.get('href')
            if destination and destination.startswith('/release/') and destination[9].isdigit():
                all_releases.append(destination)
                discogs_release_id, discogs_release_string = parse_dest(destination)

                inner_url = 'https://www.discogs.com' + destination
                if itr is None:
                    itr = get_one_release(discogs_release_id, discogs_release_string, inner_url)  # DO NOT DELETE
                
                while True:
                    try:
                        all_query_params = next(itr)
                        # yield to: 
                        # `connect.execute_query(conn, query, scrape.get_all_releases, release_set, args, max_iter=0)`
                        # in get_tunes.py: main()
                        # where query is `"CALL tu_insert_all(%s, %s, %s, %s, %s)"`
                        yield all_query_params
                    except StopIteration:
                        itr = None
                        break
                print(f'Just processed release {len(all_releases)}: {all_query_params[1]}')
                        
        n_just_processed = len(all_releases)
        if n_just_processed >= n_releases_at_start:
            break
        sleep(2)
        pg += 1
        if max_page and pg > max_page:
            # raise StopIteration
            return
        outer_resp = requests.get(f'https://www.discogs.com/user/jazcap53/collection?page={pg}')
        print(f'\nGetting page {pg}: ', end='')
    print(f'{len(all_releases)} items found.')


def get_one_release(dscg_rel_id, dscg_rel_str, url):
    sleep(1.5)
    inner_r = requests.get(url)
    inner_soup = BeautifulSoup(inner_r.text, 'html.parser')

    for table in inner_soup.find_all('table'):
        if not table.get('class'):
            continue
        if table['class'][0] == 'tracklist_3QGRS':  # we've found the right table
            table_body = table.tbody
            for table_row in table_body.find_all('tr'):
                # reset output strings
                track_posn_str = ''
                track_title_string = ''
                track_duration_string = ''
                for table_data in table_row.find_all('td'):
                    if not table_data.get('class'):
                        continue
                    if table_data['class'][0] == 'trackPos_2RCje':
                        track_posn_str = get_track_string(table_data)
                    elif table_data['class'][0] == 'duration_2t4qr':
                        track_duration_string = get_track_string(table_data)
                    elif table_data['class'][0] == 'trackTitle_CTKp4':
                        track_title_string = get_track_string(table_data)
                        track_title_string = cleanup_title_string(track_title_string)
                if track_posn_str and track_title_string:
                    track_data = (normalize_str(track_posn_str), normalize_str(track_title_string),
                                  normalize_str(track_duration_string))
                    tuple_to_yield = (dscg_rel_id, normalize_str(dscg_rel_str), *track_data)
                    yield tuple_to_yield


def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def url_parse_unquote(s):
    return urllib.parse.unquote(s)


def normalize_str(s):
    if isinstance(s, int):
        return s
    s = url_parse_unquote(str(s))
    return strip_accents(s).casefold()


def get_track_string(td):
    s = td.string
    if not s:
        td_span = td.find('span')
        if td_span and td_span.get('class'):
            s = td_span.string
    return s


def parse_dest(dest: str):
    partitioned_one = dest[1:].partition('/')  # 'result' '/'  'song-number-and-title'
    partitioned_two = partitioned_one[2].partition('-')  # 'song-number' '/' 'song-title'
    dscg_id = int(partitioned_two[0])
    dscg_title = partitioned_two[2]
    return dscg_id, dscg_title


def cleanup_title_string(title):
    if not title:
        return title

    if (l_paren_posn := title.find('(')) != -1:
        if (r_paren_posn := title.find(')')) != -1:
            if r_paren_posn > l_paren_posn:
                title = title[:l_paren_posn] + title[r_paren_posn + 1: ]
    punct = string.punctuation
    trans_dict = {}
    for c in punct:
        if c == '&':
            trans_dict[c] = 'and'
        else:
            trans_dict[c] = ''
    trans_table = str.maketrans(trans_dict)
    return title.translate(trans_table).strip()


if __name__ == '__main__':
    it = get_all_releases()
    while True:
        try:
            glorious_data = next(it)
            print('\n')
            print(glorious_data)
        except StopIteration:
            break
