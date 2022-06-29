def str2coord(coords):
    y = int(coords[1]) - 1
    x = ord(coords[0].upper()) - ord('A')
    return y, x


def coord2str(y, x):
    st = ''
    y = 1 + y
    st += ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][x]
    st += str(y)
    return st

def get_enemy_color(color):
    return (color + 1) % 2

def t2m(t):
    mode_dict = {
        '-': '-',
        'x': 'x',
        'l': '-',
        'xp': 'x'
    }
    if t in mode_dict.keys():
        return mode_dict[t]
    else:
        raise Exception('Неизвестный тип хода')




