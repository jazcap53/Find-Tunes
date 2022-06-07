# file: scrape.py
# andrew jarcho
# 2022-05-27


from time import sleep

from bs4 import BeautifulSoup
import requests


def get_all_releases():
    print('in get_all_releases()')
    pg = 1
    all_releases = []
    outer_r = requests.get(f'https://www.discogs.com/user/jazcap53/collection?page={pg}')
    print(f'\ngetting page {pg}: ', end='')
    got_release_ct = False

    itr = None
    while outer_r.status_code == 200:
        printed_release_ct = False
        outer_soup = BeautifulSoup(outer_r.text, 'html.parser')
        all_strongs = outer_soup.find_all('strong')
        for strong in all_strongs:
            if not strong.get('class'):
                continue
            release = strong['class']
            if not got_release_ct:
                n_releases = int(strong.string.partition(' of ')[2])
                got_release_ct = True
            if not printed_release_ct:
                print(strong.string.strip())
                printed_release_ct = True
        
        for link in outer_soup.find_all('a'):
            destination = link.get('href')
            if destination and destination.startswith('/release/') and destination[9].isdigit():
                print(f'\nin get_all_releases(), destination is {destination}')
                all_releases.append(destination)
                discogs_release_id, discogs_release_string = parse_dest(destination)
                # yield discogs_release_id, discogs_release_string  # commenting this in results in a tuple index error (from the db ?)

                inner_url = 'https://www.discogs.com' + destination
                if itr is None:
                    print('creating itr')
                    itr = get_one_release(discogs_release_id, discogs_release_string, inner_url)  # DO NOT DELETE
                
                while True:
                    try:
                        all_query_params = next(itr)
                        print(f'in get_all_releases(), in inner while loop, all_query_params is {all_query_params}')
                        yield all_query_params
                    except StopIteration:
                        print('reached StopIteration in get_all_releases()')
                        print('looking for next <anchor> link')
                        break

        if len(all_releases) >= n_releases:
            break
        sleep(2)
        pg += 1
        outer_r = requests.get(f'https://www.discogs.com/user/jazcap53/collection?page={pg}')
        print(f'\ngetting page {pg}: ', end='')
    print(f'{len(all_releases)} items found')


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
                track_pos_string = ''
                track_title_string = ''
                track_duration_string = ''
                for table_data in table_row.find_all('td'):
                    if not table_data.get('class'):
                        continue
                    if table_data['class'][0] == 'trackPos_2RCje':
                        track_pos_string = get_track_string(table_data)
                    elif table_data['class'][0] == 'duration_2t4qr':
                        track_duration_string = get_track_string(table_data)
                    elif table_data['class'][0] == 'trackTitle_CTKp4':
                        track_title_string = get_track_string(table_data)
                if track_pos_string and track_title_string:
                    track_data = (str(track_pos_string).lower(), str(track_title_string).lower(), str(track_duration_string).lower())
                    tuple_to_yield = (dscg_rel_id, str(dscg_rel_str).lower(), *track_data)
                    print(f'in get_one_release(), tuple_to_yield is {tuple_to_yield}')
                    # yield (dscg_rel_id, str(dscg_rel_str).lower(), *track_data)
                    yield tuple_to_yield

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


if __name__ == '__main__':
    
    print('if __name__ block')
    print(get_all_releases())
