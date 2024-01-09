import struct
import struct
import codecs


# Updated padding and finalization logic 
def finish(ctx): 
    ctx['t'][0] += (ctx['c'] * 8)  
    if ctx['t'][0] < (ctx['c'] * 8):
         ctx['t'][1] += 1

    ctx['b'][ctx['c']] = 0x80
    ctx['c'] += 1

    while ctx['c'] < 128:
         ctx['b'][ctx['c']] = 0    
         ctx['c'] += 1

    ctx['b'][112] = 0
    ctx['b'][113] = 0
    ctx['b'][114] = 0
    ctx['b'][115] = 0
    ctx['b'][116] = 0
    ctx['b'][117] = 0
    ctx['b'][118] = 0
    ctx['b'][119] = 0

    ctx['b'][120] = (ctx['t'][0]) & 0xFF
    ctx['b'][121] = (ctx['t'][0] >> 8) & 0xFF
    ctx['b'][122] = (ctx['t'][0] >> 16) & 0xFF
    ctx['b'][123] = (ctx['t'][0] >> 24) & 0xFF
    ctx['b'][124] = (ctx['t'][0] >> 32) & 0xFF
    ctx['b'][125] = (ctx['t'][0] >> 40) & 0xFF 
    ctx['b'][126] = (ctx['t'][0] >> 48) & 0xFF
    ctx['b'][127] = (ctx['t'][0] >> 56) & 0xFF

    compress(ctx, True)

IV = [
    0x6a09e667f3bcc908, 0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
    0x510e527fade682d1, 0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b, 0x5be0cd19137e2179
]

rotr64 = lambda x, n: ((x >> n) | (x << (64 - n))) 

def G(v, m, a, b, c, d, x, y):
    v[a] = (v[a] + v[b] + x)  
    v[d] = rotr64(v[d] ^ v[a], 32) 
    v[c] = (v[c] + v[d]) 
    v[b] = rotr64(v[b] ^ v[c], 24)
    v[a] = (v[a] + v[b] + y) 
    v[d] = rotr64(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d])  
    v[b] = rotr64(v[b] ^ v[c], 63)
    '''
    v[a] = (v[a] + v[b] + x) & 0xffffffffffffffff
    v[d] = rotr64(v[d] ^ v[a], 32) 
    v[c] = (v[c] + v[d]) & 0xffffffffffffffff
    v[b] = rotr64(v[b] ^ v[c], 24)
    v[a] = (v[a] + v[b] + y) & 0xffffffffffffffff
    v[d] = rotr64(v[d] ^ v[a], 16)
    v[c] = (v[c] + v[d]) & 0xffffffffffffffff 
    v[b] = rotr64(v[b] ^ v[c], 63)
    '''

def compress(ctx, last):
    v = list(ctx['h']) + IV
    v[12] ^= ctx['t'][0]
    v[13] ^= ctx['t'][1]
    if last:
        v[14] = ~v[14]
        
    m = struct.unpack('<16Q', bytes(ctx['b']))

    for i in range(12):
        s = SIGMA[i]
        G(v, m, 0, 4,  8, 12, m[s[0]], m[s[1]])
        G(v, m, 1, 5,  9, 13, m[s[2]], m[s[3]])
        G(v, m, 2, 6, 10, 14, m[s[4]], m[s[5]])
        G(v, m, 3, 7, 11, 15, m[s[6]], m[s[7]])
        G(v, m, 0, 5, 10, 15, m[s[8]], m[s[9]])
        G(v, m, 1, 6, 11, 12, m[s[10]], m[s[11]])
        G(v, m, 2, 7, 8, 13, m[s[12]], m[s[13]])
        G(v, m, 3, 4, 9, 14, m[s[14]], m[s[15]])

    for i in range(8):
        ctx['h'][i] ^= (v[i] ^ v[i + 8]) & 0xFFFFFFFFFFFFFFFF
        
def blake2b(outlen, key, data):
    ctx = {
        'h': IV.copy(), 
        't': [0, 0],
        'c': 0,
        'outlen': outlen,
        'b': bytearray(128)
    }
    
    if key:
        keylen = len(key)
    else:
        keylen = 0


    ctx['h'][0] ^= 0x01010000 ^ (keylen << 8) ^ outlen 

    if key:
        update(ctx, key) 
        ctx['c'] = 128

    # Body
    while data:
        update(ctx, data[:128])
        data = data[128:]

    # Finalize
    finish(ctx)

    # Output
    out = bytearray(outlen) 
    for i in range(outlen):
        out[i] = (ctx['h'][i>>3] >> (8 * (i & 7))) & 0xFF  
    return bytes(out)
        

def update(ctx, data):
    inlen = len(data)
    
    for i in range(inlen):
        if ctx['c'] == 128:
            ctx['t'][0] += ctx['c']
            if ctx['t'][0] < ctx['c']:
                ctx['t'][1] += 1

            compress(ctx, False)
            ctx['c'] = 0

        ctx['b'][ctx['c']] = data[i]
        ctx['c'] += 1
'''

def finish(ctx):
    ctx['t'][0] += ctx['c']
    if ctx['t'][0] < ctx['c']:
        ctx['t'][1] += 1

    while ctx['c'] < 128:
        ctx['b'][ctx['c']] = 0
        ctx['c'] += 1
        
    compress(ctx, True)
    '''

# Precomputed permutation indices
SIGMA = [
    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15],
    [14,10, 4, 8, 9,15,13, 6, 1,12, 0, 2,11, 7, 5, 3],  
    [11, 8,12, 0, 5, 2,15,13,10,14, 3, 6, 7, 1, 9, 4],
    [ 7, 9, 3, 1,13,12,11,14, 2, 6, 5,10, 4, 0,15, 8],
    [ 9, 0, 5, 7, 2, 4,10,15,14, 1,11,12, 6, 8, 3,13],
    [ 2,12, 6,10, 0,11, 8, 3, 4,13, 7, 5,15,14, 1, 9],
    [12, 5, 1,15,14,13, 4,10, 0, 7, 6, 3, 9, 2, 8,11], 
    [13,11, 7,14,12, 1, 3, 9, 5, 0,15, 4, 8, 6, 2,10],
    [ 6,15,14, 9,11, 3, 0, 8,12, 2,13, 7, 1, 4,10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5,15,11, 9,14, 3,12,13, 0 ], 
    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15],
    [14,10, 4, 8, 9,15,13, 6, 1,12, 0, 2,11, 7, 5, 3]  
]

message = "The quick brown fox jumps over the lazy dog"
message_bytes = message.encode('utf-8') 

hash_bytes = blake2b(64, None, message_bytes)

print(hash_bytes.hex())
