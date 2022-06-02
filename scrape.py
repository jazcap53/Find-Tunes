# file: scrape.py
# andrew jarcho
# 2022-05-27


from time import sleep

from bs4 import BeautifulSoup
import requests


def get_all_releases():
    pg = 1
    all_releases = []
    outer_r = requests.get(f'https://www.discogs.com/user/jazcap53/collection?page={pg}')
    print(f'\ngetting page {pg}: ', end='')
    got_release_ct = False
    
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
                print('\n' + destination)
                all_releases.append(destination)
                inner_url = 'https://www.discogs.com' + destination
                get_one_release(inner_url)

        if len(all_releases) >= n_releases:
            break
        sleep(2)
        pg += 1
        outer_r = requests.get(f'https://www.discogs.com/user/jazcap53/collection?page={pg}')
        print(f'\ngetting page {pg}: ', end='')
    print(f'{len(all_releases)} items found')


def get_one_release(url):
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
                    track_data = (track_pos_string, track_title_string, track_duration_string)
                    print(*track_data)


def get_track_string(td):
    s = td.string
    if not s:
        td_span = td.find('span')
        if td_span and td_span.get('class'):
            s = td_span.string
    return s


if __name__ == '__main__':
    get_all_releases()
