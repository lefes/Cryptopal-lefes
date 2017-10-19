"""Detect single-character XOR
Detect single-character XOR One of the 60-character strings in this file has been encrypted by single-character XOR.
Find it. (https://cryptopals.com/static/challenge-data/4.txt)
(Your code from #3 should help.)"""

import binascii
from challenge_2 import xored1
from challenge_3 import single_xored

if __name__ == '__main__':
    with open('4.txt', 'r') as secret:
        encrypted = secret.readlines()
    for number,line in enumerate(encrypted):
        if '\n' in line:
            encrypted[number] = line[:-1]

    strings = []
    for line in encrypted:
        strings.append(single_xored(line))
    strings
    result1 = 'Now that the party is jumping\n'
    result = b'Now that the party is jumping\n'
    result2 = binascii.hexlify(result)
    xored1(result2, encrypted[strings.index(result1)])