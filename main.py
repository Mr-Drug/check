from collections import Counter
import sys

typ = sys.argv[1][1]
file = sys.argv[2][:-4]


def razprog(encoding):
    prog = {}
    for i in encoding:
        key, el = chr(int(i.split('/')[0])), i.split('/')[1]
        prog[el] = key

    return prog


def h(text):
    d = dict(Counter(text).most_common())

    def derevo(d):
        m = Counter(d).most_common()[:-3:-1]
        del d[m[0][0]]
        del d[m[1][0]]
        d[(m[0], m[1])] = m[0][1] + m[1][1]
        if len(d) > 1:
            return derevo(d)
        else:
            return Counter(d).most_common()[0]

    derevo = derevo(d)
    k = {}

    def prog(t, num=''):
        nonlocal k
        e1, e2 = t[0], t[1]
        if type(e1) is tuple and type(e2) is int:
            prog(e1, num)
        elif type(e1) is tuple and type(e2) is tuple:
            prog(e1, num + '0')
            prog(e2, num + '1')
        elif type(e1) is str:
            k[e1] = num

        return k

    return prog(derevo)


def encryption(text_in):
    global prog
    text_out = ''

    for free in text_in:
        text_out += prog[free]

    cut8 = ''
    list8 = []

    for i in text_out:
        if len(cut8) == 8:
            list8.append(cut8)
            cut8 = ''
        cut8 += i

    list8.append(cut8)
    length = len(cut8)

    result = bytes([int(j, 2) for j in list8])

    return result, length


def raztext(f):
    text = []
    for line in f:
        text += [ord(i) for i in line.decode('latin-1')]
    return text


if typ == 'e':
    with open(f'{file}.txt', 'r', encoding="utf8") as f_r:
        text = f_r.read()
        prog = h(text)

    final_text, length = encryption(text)

    with open(f'{file}.par', 'w') as f_w:
        f_w.write(f"{length}'")
        for key, val in prog.items():
            f_w.write(str(ord(key)))
            f_w.write('/')
            f_w.write(val)
            f_w.write("'")
        f_w.write('\n')

    with open(f'{file}.par', 'ab') as f_wb:
        f_wb.write(final_text)

elif typ == 'd':
    with open(f'{file}.par', 'rb') as f_d:
        f_line = f_d.readline().decode('utf-8').strip('\n').split("'")
        encoding = f_line[1:-1]
        length = int(f_line[0])
        prog = razprog(encoding)
        list8 = raztext(f_d)
        text = []
        for i, val in enumerate(list8, start=1):
            cut8 = bin(val)[2:]
            if len(cut8) < 8 and i != len(list8):
                while len(cut8) < 8:
                    cut8 = '0' + cut8
            elif i == len(list8) and len(cut8) < length:
                while len(cut8) < length:
                    cut8 = '0' + cut8
            text.append(cut8)

        text = ''.join(text)
        free = ''
        text_out = ''

        for j in text:
            free += j
            if free in prog:
                text_out += prog[free]
                free = ''

        text = text_out

    with open(f'{file}.txt', 'w', encoding='utf8') as f_w:
        f_w.write(text)
