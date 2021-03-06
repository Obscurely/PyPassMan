import string
import random

encryption_key_file = 'PyPassMan_Files\\encryption.key'


def gen_char_table():
    char_table = []
    used_chars = []

    loop_var = 0  # 95
    while loop_var < 95:
        val = random.randrange(0, 95)
        if val in used_chars:
            continue

        used_chars.append(val)
        char = string.printable[val]
        char_table.append(char)

        loop_var += 1

    char_table = ''.join(char_table)
    return char_table


def gen_encryption_key():
    char_table = []
    used_chars = []

    loop_var = 0
    while loop_var < 16:
        val = random.randrange(0, 16)
        if val in used_chars:
            continue

        used_chars.append(val)
        char = string.printable[val]
        char_table.append(char)

        loop_var += 1

        encryption_key = ''.join(char_table)
    return encryption_key


key = gen_char_table() + gen_encryption_key() + gen_encryption_key() + gen_encryption_key()

with open(encryption_key_file, 'w', encoding='UTF-8') as f:
    f.write(key)
