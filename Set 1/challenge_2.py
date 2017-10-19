"""Fixed XOR
Write a function that takes two equal-length buffers and produces their XOR combination.
If your function works properly, then when you feed it the string:
1c0111001f010100061a024b53535009181c ... after hex decoding, and when XOR'd against:
686974207468652062756c6c277320657965 ... should produce:
746865206b696420646f6e277420706c6179"""

#First variant
def xored1(string1, string2):
    result = int(string1, 16) ^ int(string2, 16)
    return '{:x}'.format(result)
#Second variant
def xored2(string1, string2):
    result = int(string1, 16) ^ int(string2, 16)
    return hex(result)[2:]

if __name__ == '__main__':
    string1 = b'1c0111001f010100061a024b53535009181c'
    string2 = b'686974207468652062756c6c277320657965'
    result = '746865206b696420646f6e277420706c6179'
    print(result)
    print(xored1(string1, string2))
    print(xored2(string1, string2))
