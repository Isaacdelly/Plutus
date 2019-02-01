# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

import os

import hashlib
import binascii
import multiprocessing

from fastecdsa import curve, keys
from bloom_filter import BloomFilter

DATABASE = r'database/JAN_09_2019/'
BLOOM_FILTER_NAME = 'filter.bf'


def generate_private_key(): 
    """Generate a random 32-byte hex integer which serves as a randomly generated Bitcoin private key.
    Average Time: 0.0000061659 seconds
    """
    return keys.gen_private_key(curve.secp256k1)


def private_key_to_public_key(private_key):
    """Accept a hex private key and convert it to its respective public key. Because converting a private key to 
    a public key requires SECP256k1 ECDSA signing, this function is the most time consuming and is a bottleneck
    in the overall speed of the program.
    Average Time: 0.0031567731 seconds
    """
    public_key = keys.get_public_key(private_key, curve.secp256k1)
    return '04' + str((public_key.x).to_bytes(32, byteorder='big').hex()) + str((public_key.y).to_bytes(32, byteorder='big').hex())


def public_key_to_address(public_key):
    """Accept a public key and convert it to its resepective P2PKH wallet address.
    Average Time: 0.0000801390 seconds
    """
    output = []; alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    var = '00' + var.hexdigest() + hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()[0:8]
    count = [char != '0' for char in var].index(True) // 2
    n = int(var, 16)
    while n > 0:
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    [(output.append(alphabet[0]), ) for i in range(count)]
    return ''.join(output[::-1])


def process(private_key, public_key, address, bf):
    """Accept an address and query the database. If the address is found in the database, then it is assumed to have a 
    balance and the wallet data is written to the hard drive. If the address is not in the database, then it is 
    assumed to be empty and printed to the user. This is a fast and efficient query.
    Average Time: 0.0000026941 seconds
    """
    if bf.lookup(address):
        with open('plutus.txt', 'a') as file:
            file.write('hex private key: ' + str(private_key) + '\n' +
                       'WIF private key: ' + str(private_key_to_WIF(private_key)) + '\n' +
                       'public key: ' + str(public_key) + '\n' +
                       'address: ' + str(address) + '\n\n')
    else: 
         print(str(address))


def private_key_to_WIF(private_key):
    """Convert the hex private key into Wallet Import Format for easier wallet importing. This function is 
    only called if a wallet with a balance is found. Because that event is rare, this function is not significant 
    to the main pipeline of the program and is not timed.
    """
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify('80' + private_key)).hexdigest())).hexdigest()
    var = binascii.unhexlify('80' + private_key + var[0:8])
    alphabet = chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''; value = pad = 0;
    for i, c in enumerate(var[::-1]): value += 256**i * c
    while value >= len(alphabet):
        div, mod = divmod(value, len(alphabet))
        result, value = chars[mod] + result, div
    result = chars[value] + result
    for c in var:
        if c == 0: pad += 1
        else: break
    return chars[0] * pad + result


def main(bf):
    """Create the main pipeline by using an infinite loop to repeatedly call the functions, while utilizing 
    multiprocessing from __main__. Because all the functions are relatively fast, it is better to combine
    them all into one process.
    """
    while True:
        private_key = generate_private_key()                # 0.0000061659 seconds
        public_key = private_key_to_public_key(private_key) # 0.0031567731 seconds
        address = public_key_to_address(public_key)         # 0.0000801390 seconds
        process(private_key, public_key, address, bf)       # 0.0000026941 seconds
                                                            # --------------------
                                                            # 0.0032457721 seconds


if __name__ == '__main__':
    """Deserialize the database and read into a list of sets for easier selection and O(1) complexity. Initialize
    the multiprocessing pool to target the main function with cpu_count() concurrent processes.
    """
    database = [set() for _ in range(4)]
    count = len(os.listdir(DATABASE))
    half = count // 2; quarter = half // 2
    if os.path.exists(BLOOM_FILTER_NAME) and os.path.isfile(BLOOM_FILTER_NAME):
        bf = BloomFilter.deserialize()
    else:
        BloomFilter.convert_db_to_bloom_filter()
        bf = BloomFilter.deserialize()
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            pool.map(main(bf), range(multiprocessing.cpu_count() * 2))

