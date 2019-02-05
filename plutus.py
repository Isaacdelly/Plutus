# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

import os
import pickle
import hashlib
import binascii
import multiprocessing
import fastecdsa
import bloom_filter

DATABASE = r'database/FEB_03_2019.pickle'

def generate_private_key(): 
    """Generate a random 32-byte hex integer which serves as a randomly generated Bitcoin private key.
    Average Time: 0.0000061659 seconds
    """
    return binascii.hexlify(os.urandom(32)).decode('utf-8').upper()

def private_key_to_public_key(private_key):
    """Accept a hex private key and convert it to its respective public key using SECP256k1 ECDSA signing.
    Average Time:  seconds
    """
    public_key = fastecdsa.keys.get_public_key(private_key, fastecdsa.curve.secp256k1)
    return '04' + public_key.x.to_bytes(32, byteorder='big').hex().upper() + public_key.y.to_bytes(32, byteorder='big').hex().upper()

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

def process(private_key, public_key, address, database):
    """Accept an address and query the database. If the address is found in the database, then it is assumed to have a 
    balance and the wallet data is written to the hard drive. If the address is not in the database, then it is 
    assumed to be empty and printed to the user. This is a fast and efficient query.
    Average Time:  seconds
    """
    if address in database:
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
              
def main(database):
    """Create the main pipeline by using an infinite loop to repeatedly call the functions, while utilizing 
    multiprocessing from __main__. Because all the functions are relatively fast, it is better to combine
    them all into one process.
    """
    while True:
        private_key = generate_private_key()                # 0.0000061659 seconds
        public_key = private_key_to_public_key(private_key) #  seconds
        address = public_key_to_address(public_key)         # 0.0000801390 seconds
        process(private_key, public_key, address, database) #  seconds
                                                            # --------------------
                                                            # seconds
                                                            # brute forces per second =  ÷ cpu_count()
    
if __name__ == '__main__':
    """Deserialize the database and load into a bloom filter. Initialize the multiprocessing pool to target the 
    main function with cpu_count() concurrent processes.
    """
    with open(DATABASE, 'rb') as file:
            database = pickle.load(file)
      
    # To verify the bloom filter configuration, remove the # from the line below
    #print('Database Information: ' + repr(database))
    
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            pool.map(main(database), range(multiprocessing.cpu_count() * 2))
            
