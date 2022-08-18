import os, glob

def extract_song_name(s):
    song_path = s.split('___')[0].replace('_', ' ')
    return os.path.basename(song_path)


def shorten_path_name(path_name):
    # return '~/' + '/'.join(path_name.split('/')[3:])
    return path_name.rsplit('/')[-1]


def get_mp3_set(dirname):
    mp3_list = [filename for filename in glob.glob(os.path.join(dirname, '*.mp3'))]
    for ix, val in enumerate(mp3_list):
        mp3_list[ix] = extract_song_name(val), shorten_path_name(val)
    return set(mp3_list)


if __name__ == '__main__':
    print(*sorted(list(get_mp3_set('/home/jazcap53/Music/misc_mp3s'))), sep='\n')
