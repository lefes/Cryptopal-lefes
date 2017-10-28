"""
Break repeating-key XOR

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

1.Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
2.Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:
    this is a test
and
    wokka wokka!!!
is 37. Make sure your code agrees before you proceed.
3.For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
4.The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
5.Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
6.Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
7.Solve each block as if it was single-character XOR. You already have code to do this.
8.For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.
This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.
"""

from base64 import decodebytes
from operator import itemgetter

def xor_enc_key(cypher_text, key):
    """
    Function for XOR text and key
    cypher_text - text for encryption or decryption
    key - key for xor encryption or decryption
    return bytearray of result XOR
    """
    key = norm_key(cypher_text, key)
    size = len(cypher_text)
    result = bytearray(size)
    for i in range(size):
        result[i] = cypher_text[i] ^ key[i]
    return result.decode('utf-8') 

def norm_key(text, key):
    """
    Function to change key size to equal text
    text - text for encryption or decryption
    key - key for xor encryption or decryption
    return key
    """
    while len(key) < len(text):
        key += key
    return key

def single_xored(bytes_string):
    """
    Function for detect single-byte XOR cipher
    bytes_string - string of bytes
    return decrypted string
    """
    xored = (''.join(chr(num ^ key) for num in bytes_string) for key in range(256))
    return max(xored, key=lambda s: s.count(' '))

def hamming_dist(str_bytes, str_bytes2):
    """
    Function to compute the edit distance/Hamming distance between two strings
    str_bytes  - string of bytes 1
    str_bytes2 - string of bytes 2
    return distance of integer 
    """
    # Convert bytes to binary
    word1 = ' '.join(format(x, 'b') for x in str_bytes)
    word2 = ' '.join(format(x, 'b') for x in str_bytes2)
    # Initial a distance of integer
    diffs = 0
    # Split binary words to list
    compare1 = word1.split(' ')
    compare2 = word2.split(' ')
    # Aligning blocks of binary strings
    for i,j in zip(compare1, compare2):
        while len(i) > len(j):
            j = '0' + j
        while len(i) < len(j):
            i = '0' + i
        # Compare strings
        for chr1, chr2 in zip(i,j):
            if chr1 != chr2:
                diffs += 1
    return diffs

def open_and_clear(file_name):
    """
    Function for open file, read all bytes strings from file and clear it from line breaks
    file_name - name of file
    return binary string
    """
    file = open(file_name, 'rb').read()
    while b'\n' in file or b'\r' in file:
        file = file.replace(b'\n', b'')
        file = file.replace(b'\r', b'')
    return file

def average(array_of_numbers):
    """
    Function for arithmetical mean
    return integer
    """
    return sum(array_of_numbers)//len(array_of_numbers)

def break_text(text, length):
    """
    Function for break text on blocks fixed length
    text   - text for break
    length - block length
    return list of blocks
    """
    text_list = []
    for i in range(0, len(text)//length):
            text_list.append(text[i*length:(length*(i+1))])
    return text_list

def keysize_hunter(cypher_bytes, max_keysize=40):
    """
    Main Function to break repeating-key XOR
    cypher_bytes - cleared (without line breaks) text of bytes
    max_keysize  - key length for break
    return None
    """
    # Temp variable for text of bytes
    guess_text = cypher_bytes
    # Dictionary of keysizes for different lengths
    keysizes = {}
    # The cycle of determining the estimated key length
    for keysize in range(2,max_keysize+1):
        guess_list = break_text(guess_text, keysize)
        # The list of distance between block of bytes
        dist = []
        # Length сalculation сycle
        while len(guess_list)>2:
            dist.append(hamming_dist(guess_list.pop(0), guess_list[1])/keysize)
        # Calculating the average length between bytes for the size of the key
        keysizes[keysize] = int(average(dist))
    # Sorting the size of keys by their values 
    keys = sorted(keysizes.items(), key=itemgetter(1))
    i = 0
    # The cycle of breaking repeating-key XOR
    while True:
        # Take keysize from list of keysizes
        len_key = keys[0][i]
        print('Trying keysize: ' + str(len_key))
        guess_list = break_text(guess_text, len_key)
        # Transpose the blocks: block that is the first byte of every block, and a block that is the second byte of every block, and so on.
        transpose = list(map(list, zip(*guess_list)))
        # Assumed key
        key = []
        # Solving each block as if it was single-character XOR
        for block in transpose:
            key.append(ord(single_xored(block)[0]) ^ block[0])
        result = ''
        # Trying to decrypt text
        print(xor_enc_key(cypher_bytes, key))
        responce = input('Is the selected text decrypted?? ')
        if responce.lower() == 'y':
            break
        # If the text was not decrypted try with the next size of the key
        i += 1

if __name__ == '__main__':
    cypher = decodebytes(open_and_clear('6.txt'))
    keysize_hunter(cypher)