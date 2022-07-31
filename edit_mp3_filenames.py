from pathlib import Path


def subst_us_bar(name, answer):
    us_ct = 0 
    for i in range(len(name)):
        if name[i] == '_':
            us_ct += 1
            if us_ct == answer:
                new_name = name[:i] + '___' + name[i+1:]
                print(new_name)
                yn = input("Is this what you wanted? [y/N] ")
                if yn == 'y':
                    return True, new_name
                return False, name

def get_pos_int(prompt, max):
    while True:
        answer = input(prompt)
        if not answer.isdecimal():
            print('Not a number')
        elif not 1 <= int(answer) <= max:
            print('Out of range')
        else:
            return int(answer)

def print_filenames(path):
    for file in path.iterdir():
        if file.suffix != '.mp3' or '___' in file.name: 
            continue
        name = file.name
        print(name)
        num_us = name.count('_')
        prompt = f"Enter an integer between 1 and {num_us} >>> "
        answer = get_pos_int(prompt, num_us)
        subst_result = subst_us_bar(name, answer)
        while not subst_result[0]:
            answer = get_pos_int(prompt, num_us)
            subst_result = subst_us_bar(name, answer)
        new_name = subst_result[1]
        file.rename(Path(path / new_name))


if __name__  == '__main__':
    print_filenames(Path('/home/jazcap53/Music/misc_mp3s'))
