"""
Lets the user replace selected instances of
the underscore character in file names with
___ (triple underscore).
"""

from pathlib import Path


def subst_us_3us(name, positions):
    """
    Replace selected instances of _ in
    name with ___ (triple underscore).
    """
    us_ct = 0
    i = 0
    orig_name = name[:]
    while i < len(name):
        if name[i] == '_':
            us_ct += 1
            if us_ct in positions:
                name = name[:i] + '___' + name[i+1:]
                us_ct += 2  # we just added 2 underscores
                i += 3  # look at the 1st position after tne change
            else:
                i += 1
        else:
            i += 1
    print(name)
    if not input("Is this what you wanted? (Press <Enter> "
                 "for yes, 'n' + <Enter> for no) "):
        return True, name
    return False, orig_name


def get_positions(num_us):
    """
    Prompt the user for a space-separated list of
    positions of underscores to replace with triple-underscore.
    """
    prompt = f"Enter positive integers <= {num_us} separated by spaces >>> "
    answer = input(prompt)
    first_list = sorted(list({int(part) for part in answer.split() if 1 <= int(part)}))
    return [val + 2 * ix for ix, val in enumerate(first_list)]


def print_filenames(path):
    """Display and rename all mp3 files in the specified directory."""
    for file in path.iterdir():
        if file.suffix != '.mp3' or '___' in file.name:
            continue
        name = file.name
        print(name)
        num_us = name.count('_')
        positions = get_positions(num_us)
        success, name = subst_us_3us(name, positions)
        while not success:
            print(name)
            positions = get_positions(num_us)
            success, name = subst_us_3us(name, positions)
        file.rename(Path(path / name))


if __name__  == '__main__':
    print_filenames(Path('/home/jazcap53/Music/misc_mp3s'))
