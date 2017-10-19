"""Single-byte XOR cipher
The hex encoded string:
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736 ... has been XOR'd against a single character. Find the key, decrypt the message.
You can do this by hand. But don't: write code to do it for you.
How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.
Achievement Unlocked You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter."""

import binascii

def single_xored(string1):
    encoded = binascii.unhexlify(string1)
    xored = (''.join(chr(num ^ key) for num in encoded) for key in range(256))
    return max(xored, key=lambda s: s.count(' '))

def single_xored2(string1):
    encoded = binascii.unhexlify(string1)
    key = max(encoded, key=encoded.count) ^ ord(' ')
    return ''.join(chr(num ^ key) for num in encoded)

if __name__ == '__main__':
    encoded = b'1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print(single_xored(encoded))
    print(single_xored2(encoded))