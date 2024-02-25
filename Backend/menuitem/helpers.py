import math

# Helper Functions
def rotate_right(val, r_bits):
    return ((val >> r_bits) | (val << (32 - r_bits))) & 0xFFFFFFFF

def ch(x, y, z):
    return (x & y) ^ (~x & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def sigma0(x):
    return rotate_right(x, 2) ^ rotate_right(x, 13) ^ rotate_right(x, 22)

def sigma1(x):
    return rotate_right(x, 6) ^ rotate_right(x, 11) ^ rotate_right(x, 25)

def gamma0(x):
    return rotate_right(x, 7) ^ rotate_right(x, 18) ^ (x >> 3)

def gamma1(x):
    return rotate_right(x, 17) ^ rotate_right(x, 19) ^ (x >> 10)

# Padding Function
def pad_message(message):
    # Convert the message to bytes if it's not already
    if isinstance(message, str):
        message = message.encode('utf-8')

    # Calculate the padding length
    pad_len = 64 - (len(message) % 64)

    # Add the padding and length
    padded_message = message + b'\x80' + b'\x00' * (pad_len - 1) + (8 * len(message)).to_bytes(8, byteorder='big')

    return padded_message