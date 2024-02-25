import math
from menuitem.helpers import *
# SHA-256 Constants
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

# Initial Hash Values
h0 = 0x6a09e667
h1 = 0xbb67ae85
h2 = 0x3c6ef372
h3 = 0xa54ff53a
h4 = 0x510e527f
h5 = 0x9b05688c
h6 = 0x1f83d9ab
h7 = 0x5be0cd19

def sha256(message):
    global h0, h1, h2, h3, h4, h5, h6, h7  # Make the hash values global

    # Pre-processing
    message = pad_message(message)
    blocks = [message[i:i + 64] for i in range(0, len(message), 64)]

    for block in blocks:
        # Initialize hash values for this block
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        # Convert the block to 16 big-endian 32-bit words
        w = [int.from_bytes(block[i:i + 4], byteorder='big') for i in range(0, 64, 4)]

        # Extend the 16 words to 64 words
        for i in range(16, 64):
            s0 = gamma0(w[i - 15])
            s1 = gamma1(w[i - 2])
            w.append((w[(i - 16) % 64] + s0 + w[(i - 7) % 64] + s1) & 0xFFFFFFFF)

        # Main loop
        for i in range(64):
            S1 = sigma1(e)
            ch_result = ch(e, f, g)
            temp1 = (h + S1 + ch_result + K[i % 64] + w[i]) & 0xFFFFFFFF
            S0 = sigma0(a)
            maj_result = maj(a, b, c)
            temp2 = (S0 + maj_result) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        # Update the hash values
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    # Concatenate the hash values and return the final hash
    hash_result = (
        h0.to_bytes(4, byteorder='big') +
        h1.to_bytes(4, byteorder='big') +
        h2.to_bytes(4, byteorder='big') +
        h3.to_bytes(4, byteorder='big') +
        h4.to_bytes(4, byteorder='big') +
        h5.to_bytes(4, byteorder='big') +
        h6.to_bytes(4, byteorder='big') +
        h7.to_bytes(4, byteorder='big')
    )

    return hash_result


# Convert hash result to hexadecimal string for better readability
def hash_to_hex(hash_result):
    return ''.join(format(byte, '02x') for byte in hash_result)


def generateSHA256(message):
    input_message = message.encode('utf-8')
    hashed_result = sha256(message)
    hex_result = hash_to_hex(hashed_result)

    return hex_result