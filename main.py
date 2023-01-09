from collections import Counter
import sys

alp = ['\n', ' ', '!', '"', "'", '(', ')', '*', ',', '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '\\', '^', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'Ё', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё']

typ = sys.argv[1][1]
file = sys.argv[2][:-4]
vigen = False
try:
    vigen = sys.argv[3]
except IndexError:
    pass


def huffman(text):  # Кодирование Хаффмана
    d = dict(Counter(text).most_common())

    def tree(d):  # Рекурсивное строительство дерева
        m = Counter(d).most_common()[:-3:-1]
        del d[m[0][0]]
        del d[m[1][0]]
        d[(m[0], m[1])] = m[0][1] + m[1][1]
        if len(d) > 1:
            return tree(d)
        else:
            return Counter(d).most_common()[0]

    tree = tree(d)
    k = {}

    def kod(t, num=''):  # Получение кода из дерева
        nonlocal k
        e1, e2 = t[0], t[1]
        if type(e1) is tuple and type(e2) is int:
            kod(e1, num)
        elif type(e1) is tuple and type(e2) is tuple:
            kod(e1, num + '0')
            kod(e2, num + '1')
        elif type(e1) is str:
            k[e1] = num

        return k

    return kod(tree)


def encryption(text_in):  # Шифрование текста
    global kod
    text_out = ''

    for let in text_in:
        text_out += kod[let]

    slice = ''
    slices = []

    for i in text_out:
        if len(slice) == 8:
            slices.append(slice)
            slice = ''
        slice += i

    slices.append(slice)
    length = len(slice)

    result = bytes([int(j, 2) for j in slices])

    return result, length


def dekod(line):  # Получение кода
    kod = {}
    leng = int(line[0])
    lis = line[2:-1].split()
    for i in range(0, len(lis), 2):
        el, k = chr(int(lis[i])), lis[i + 1]
        kod[k] = el

    return kod, leng


def detext(f):  # Получение текста
    text = []
    for line in f:
        text += [ord(i) for i in line.decode('latin-1')]
    return text


def decryption(slices, kod, length):  # Дешифрование текста
    text = []
    for i, val in enumerate(slices, start=1):
        slice = bin(val)[2:]
        if len(slice) < 8 and i != len(slices):
            while len(slice) < 8:
                slice = '0' + slice
        elif i == len(slices) and len(slice) < length:
            while len(slice) < length:
                slice = '0' + slice
        text.append(slice)

    text = ''.join(text)
    let = ''
    text_out = ''

    for j in text:
        let += j
        if let in kod:
            text_out += kod[let]
            let = ''

    return text_out


def key_vig(word):
    res = []
    for i in word:
        res.append(ord(i))
    return res


def vigenere(text, key):  # Шифрование Виженера
    result = ''
    for i, val in enumerate(text):
        result += alp[(alp.index(val) + alp.index(key[i % len(key)])) % len(alp)]

    return result


def devigenere(text, key):  # Дешифрование Виженера
    result = ''
    for i, val in enumerate(text):
        result += alp[(alp.index(val) - alp.index(key[i % len(key)]) + len(alp)) % len(alp)]

    return result


# Шифрование
if typ == 'e':
    with open(f'{file}.txt', 'r', encoding="utf8") as f_r:
        if vigen:
            text = vigenere(f_r.read(), vigen)
        else:
            text = f_r.read()
        kod = huffman(text)

    final_text, length = encryption(text)

    with open(f'{file}.par', 'w') as f_w:
        f_w.write(f"{length} ")
        for key, val in kod.items():
            f_w.write(str(ord(key)))
            f_w.write(' ')
            f_w.write(val)
            f_w.write(" ")
        f_w.write('\n')

    with open(f'{file}.par', 'ab') as f_wb:
        f_wb.write(final_text)
# Дешифрование
elif typ == 'd':
    with open(f'{file}.par', 'rb') as f_d:
        f_line = f_d.readline().decode('utf-8').strip('\n')
        kod, length = dekod(f_line)
        slices = detext(f_d)
        text = decryption(slices, kod, length)

    with open(f'{file}.txt', 'w', encoding='utf8') as f_w:
        f_w.write(text)

    if vigen:
        with open(f'{file}.txt', 'r', encoding="utf8") as f_r:
            text = devigenere(f_r.read(), vigen)
        with open(f'{file}.txt', 'w', encoding="utf8") as f_w:
            f_w.write(text)
