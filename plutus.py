# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus
# ------------------------------------------------
# Added fastecdsa - June 2019 - Ian McMurray
# https://github.com/imcmurray/Plutus-fastecdsa
# ------------------------------------------------
# Added convert to pickle from csv - July 2019 - AirShark
# https://github.com/AirShark/Plutus

import os
import pickle
import hashlib
import binascii
import multiprocessing
from fastecdsa import keys, curve

DATABASE = r'database/JUL_06_2019/'

def generate_private_key(): 
    """
    Generate a random 32-byte hex integer which serves as a randomly 
    generated Bitcoin private key.
    Average Time: 0.0000061659 seconds
    """
    return binascii.hexlify(os.urandom(32)).decode('utf-8').upper()

def private_key_to_public_key(private_key):
    """
    Accept a hex private key and convert it to its respective public key. 
    Because converting a private key to a public key requires SECP256k1 ECDSA 
    signing, this function is the most time consuming and is a bottleneck in 
    the overall speed of the program.
    Average Time: 0.0016401287 seconds
    """
    # get the public key corresponding to the private key we just generated
    c = int('0x%s'%private_key,0)
    d = keys.get_public_key(c, curve.secp256k1)
    return '04%s%s'%('{0:x}'.format(int(d.x)), '{0:x}'.format(int(d.y)))

def public_key_to_address(public_key):
    """
    Accept a public key and convert it to its resepective P2PKH wallet RipeMD-160 address.
    Average Time: 0.0000801390 seconds
    """
    var = hashlib.new('ripemd160')
	encoding = binascii.unhexlify(public_key.encode())
	var.update(hashlib.sha256(encoding).digest())
	return var.hexdigest()

def process(private_key, public_key, address, database):
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
            file.write(str(private_key) + '\tn' + str(address) + '\n')
    else: 
        # Is printing every address slowing the process down since it has to write to STDOUT?
        #print(str(private_key),":",str(address))
        print('\r' + str(address), end = "")

def main(database):
    """
    Create the main pipeline by using an infinite loop to repeatedly call the 
    functions, while utilizing multiprocessing from __main__. Because all the 
    functions are relatively fast, it is better to combine them all into 
    one process.
    """
    while True:
        private_key = generate_private_key()                    # 0.0000061659 seconds
        public_key = private_key_to_public_key(private_key)     # 0.0016401287 seconds
        address = public_key_to_address(public_key)             # 0.0000801390 seconds
        if address != -1:
            process(private_key, public_key, address, database) # 0.0000026941 seconds
                                                                # --------------------
                                                                # 0.0017291287 seconds
    
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

    for cpu in range(multiprocessing.cpu_count()):
        multiprocessing.Process(target = main, args = (database, )).start()
