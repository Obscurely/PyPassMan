import string
import random

char_table = []
used_chars = []

loop_var = 0  # 95
while loop_var < 16:
    val = random.randrange(0, 16)
    if val in used_chars:
        continue

    used_chars.append(val)
    char = string.printable[val]
    char_table.append(char)

    loop_var += 1

with open('encryption_key.txt', 'w', encoding='UTF-8') as f:
    f.write(''.join(char_table))
