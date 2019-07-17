# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus
# ------------------------------------------------
# Added fastecdsa - June 2019 - Ian McMurray
# https://github.com/imcmurray/Plutus-fastecdsa
# ------------------------------------------------
# Added convert to pickle from csv - July 2019 - AirShark
# https://github.com/AirShark/Plutus
# ------------------------------------------------
# Added Altcoins - Compressed Keys - Secp256k1 CRPRNG- July 2019 - Jiloumed
# https://github.com/Jiloumed/Plutus

import os
import pickle
import hashlib
import binascii
#import multiprocessing
#from fastecdsa import keys, curve

DATABASE = r'database/JUL_13_2019/'

"""
Start from a random seed
generated Bitcoin private key.
Average Time: 0.0000000000 seconds
"""
seed =  0xdeedbeef

modp = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
gz = 0x1

def inverse_mod(a, m):
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
    if ud > 0: return ud
    else: return ud + m

def from_jacobian(Xp, Yp, Zp):
    z = inverse_mod(Zp, modp)
    return (Xp * z**2) % modp, (Yp * z**3) % modp

def bit_to_add(a):
    d=[]
    bitl= a.bit_length()
    for i in range(bitl):
        c = a | (1 << i)
        if c == a: d.append(2**i)
    return d

def double_gen_point(x, y, z):
    points = {1:[x, y, z]}
    for i in range(1, r.bit_length()):
        x, y, z = double(x, y, z)
        points[2**i] = [x, y, z]
    return points

def double(x, y, z):
    s = 4 * x * y**2 % modp
    m = 3 * x**2 % modp
    x1 = (m**2 - 2 * s) % modp
    y1 = (m * (s - x1) - 8 * y**4) % modp
    z1 = 2 * y * z % modp
    return x1, y1, z1

def add(Xp, Yp, Zp, Xq, Yq, Zq):
    if not Yp: return (Xq, Yq, Zq)
    if not Yq: return(Xp, Yp, Zp)
    u1 = (Xp * Zq**2) % modp
    u2 = (Xq * Zp**2) % modp
    s1 = (Yp * Zq**3) % modp
    s2 = (Yq * Zp**3) % modp
    if u1 == u2:
        if s1 != s2: return(0,0,1)
        return jacobian_double(Xp, Yp, Zp)
    h = u2 - u1
    rs = s2 - s1
    h2 = (h * h) % modp
    h3 = (h * h2) % modp
    u1h2 = (u1 * h2) % modp
    nx = (rs**2 - h3 - 2*u1h2) % modp
    ny = (rs*(u1h2 - nx) - s1 * h3) % modp
    nz = (h*Zp*Zq) % modp
    return nx, ny, nz

dbgen = double_gen_point(gx, gy, gz)

def private_key_to_public_key(private_key):
    """
    Accept a hex private key and convert it to its respective public key. 
    Because converting a private key to a public key requires SECP256k1 ECDSA 
    signing, this function is the most time consuming and is a bottleneck in 
    the overall speed of the program.
    Average Time: 0.0016401287 seconds
    """
    # get the public key corresponding to the private key we just generated
    if private_key in dbgen: return from_jacobian(dbgen[private_key][0], dbgen[private_key][1], dbgen[private_key][2])
    btad = bit_to_add(private_key)
    publicKey = dbgen[btad[0]]
    for i in btad[1:]:
        publicKey = add(publicKey[0], publicKey[1], publicKey[2], dbgen[i][0], dbgen[i][1], dbgen[i][2])
    publicKey = from_jacobian(publicKey[0], publicKey[1], publicKey[2])
    xpublicKey = "%064x" % publicKey[0]
    global seed
    seed = publicKey[0]
    if publicKey[1] % 2 == 1: # If the Y value for the Public Key is odd.
        return "03" + xpublicKey.upper()
    else: # Or else, if the Y value is even.
        return "02" + xpublicKey.upper()

def public_key_to_address(public_key):
    """
    Accept a public key and convert it to its resepective P2PKH wallet RipeMD-160 address.
    Average Time: 0.0000801390 seconds
    """
    var = hashlib.new('ripemd160')
    encoding = binascii.unhexlify(public_key.encode())
    var.update(hashlib.sha256(encoding).digest())
    return var.hexdigest()

def process(private_key, address, database):
    """
    Accept an address and query the database. If the address is found in the 
    database, then it is assumed to have a balance and the wallet data is 
    written to the hard drive. If the address is not in the database, then it 
    is assumed to be empty and printed to the user.
    Average Time: 0.0000026941 seconds
    """
    if address in database[0] or \
        address in database[1] or \
        address in database[2] or \
        address in database[3] or \
        address in database[4]:
        with open('plutus.csv', 'a') as file:
            file.write(hex(private_key) + ';' + str(address) + '\n')

def main(database):
    """
    Create the main pipeline by using an infinite loop to repeatedly call the 
    functions, while utilizing multiprocessing from __main__. Because all the 
    functions are relatively fast, it is better to combine them all into 
    one process.
    """
    while True:
        private_key = seed
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)
        process(private_key, address, database)
    
if __name__ == '__main__':
    """
    Deserialize the database and read into a list of sets for easier selection 
    and O(1) complexity. Initialize the multiprocessing to target the main 
    function with cpu_count() concurrent processes.
    """
    database = [set() for _ in range(5)]
    count = len(os.listdir(DATABASE))
    half = count // 2
    quarter = half // 2
    for c, p in enumerate(os.listdir(DATABASE)):
        print('\rreading database: ' + str(c + 1) + '/' + str(count), end = ' ')
        with open(DATABASE + p, 'rb') as file:
            if c + 1 == 21: # FIXME
                database[4] = database[4] | pickle.load(file) # FIXME
                continue # FIXME
            if c < half:
                if c < quarter: database[0] = database[0] | pickle.load(file)
                else: database[1] = database[1] | pickle.load(file)
            else:
                if c < half + quarter: database[2] = database[2] | pickle.load(file)
                else: database[3] = database[3] | pickle.load(file)
    print('DONE')
    # To verify the database size, remove the # from the line below
    #print('database size: ' + str(sum(len(i) for i in database))); quit()

    #for cpu in range(multiprocessing.cpu_count()):
    #    multiprocessing.Process(target = main, args = (database, )).start()
    try:
        main(database)
    except KeyboardInterrupt:
        print("Next Seed: "+hex(seed))
