class Blake2b:
    sigma = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15],
        [ 14,10, 4, 8, 9,15,13, 6, 1,12, 0, 2,11, 7, 5, 3 ],
        [ 11, 8,12, 0, 5, 2,15,13,10,14, 3, 6, 7, 1, 9, 4 ],
        [  7, 9, 3, 1,13,12,11,14, 2, 6, 5,10, 4, 0,15, 8 ],
        [  9, 0, 5, 7, 2, 4,10,15,14, 1,11,12, 6, 8, 3,13 ],
        [  2,12, 6,10, 0,11, 8, 3, 4,13, 7, 5,15,14, 1, 9 ],
        [ 12, 5, 1,15,14,13, 4,10, 0, 7, 6, 3, 9, 2, 8,11 ],
        [ 13,11, 7,14,12, 1, 3, 9, 5, 0,15, 4, 8, 6, 2,10 ],
        [  6,15,14, 9,11, 3, 0, 8,12, 2,13, 7, 1, 4,10, 5 ],
        [ 10, 2, 8, 4, 7, 6, 1, 5,15,11, 9,14, 3,12,13 ,0 ],
        [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15 ],
        [ 14,10, 4, 8, 9,15,13, 6, 1,12, 0, 2,11, 7, 5, 3 ]
    ]  
    
    IV = [
    0x6a09e667f3bcc908,
    0xbb67ae8584caa73b,
    0x3c6ef372fe94f82b,
    0xa54ff53a5f1d36f1,
    0x510e527fade682d1,
    0x9b05688c2b3e6c1f,
    0x1f83d9abfb41bd6b,
    0x5be0cd19137e2179]
    stateVector=[]

    def __init__(self):
        for i,val in enumerate(self.IV):
               print(i)
               self.stateVector[i] = self.IV[i]
               self.stateVector.append(val)

    def blake2b(msg):
        pass

    def Rot64(x,y):
        pass

    def B2B_GET64(p):
        pass

    def B2B_G(a,b,c,d,x,y):
        pass
    
    def Blake2b_compress(ctx,last):
        pass

    def Blake2b_update(ctx,inMsg,inlen):
        pass

    def blake2b_final(ctx):
        pass

b = Blake2b()
print(b.h)
