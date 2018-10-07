# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

try:
    import sys
    import os
    import time
    import hashlib
    import binascii
    import multiprocessing
    from multiprocessing import Process, Queue
    from multiprocessing.pool import ThreadPool
    import threading
    import base58
    import ecdsa
    import requests
except ImportError:
    import subprocess
    subprocess.check_call(["python", '-m', 'pip', 'install', 'base58==1.0.0'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'ecdsa==0.13'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'requests==2.19.1'])
    import base58
    import ecdsa
    import requests

def generate_private_key():
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def private_key_to_WIF(private_key):
    var80 = "80" + str(private_key) 
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')

def private_key_to_public_key(private_key):
    sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve = ecdsa.SECP256k1)
    return ('04' + binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8'))

def public_key_to_address(public_key):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    count = 0; val = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    doublehash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()
    address = '00' + var.hexdigest() + doublehash[0:8]
    for char in address:
        if (char != '0'):
            break
        count += 1
    count = count // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod (n, 58)
        output.append(alphabet[remainder])
    while (val < count):
        output.append(alphabet[0])
        val += 1
    return ''.join(output[::-1])

def get_balance(address):
    try:
        API = requests.get("https://bitcoinlegacy.blockexplorer.com/api/addr/" + str(address) + "/balance")
        if (API.status_code != 200 and API.status_code != 400):
            return -1
        return int(API.text) 
    except:
        return -1
    
def data_export(queue):
    while True:
        if queue.qsize() < 100:
            private_key = generate_private_key()
            public_key = private_key_to_public_key(private_key)
            address = public_key_to_address(public_key)
            data = (private_key, address)
            queue.put(data, block = False)
        else:
            time.sleep(1)

def worker(queue):
    while True:
        if queue.qsize() > 0:
            data = queue.get(block = True)
            balance = get_balance(data[1])
            process(data, balance)

def process(data, balance):
    private_key = data[0]
    address = data[1]
    if (balance == 0):
        print("{:<34}".format(str(address)) + ": " + str(balance))
    if (balance > 0):
        file = open("plutus.txt","a")
        file.write("address: " + str(address) + "\n" +
                   "private key: " + str(private_key) + "\n" +
                   "WIF private key: " + str(private_key_to_WIF(private_key)) + "\n" +
                   "public key: " + str(private_key_to_public_key(private_key)).upper() + "\n" +
                   "balance: " + str(balance) + "\n\n")
        file.close()

def thread(iterator):
    processes = []
    data = Queue()
    data_factory = Process(target = data_export, args = (data,))
    data_factory.daemon = True
    processes.append(data_factory)
    data_factory.start()
    work = Process(target = worker, args = (data,))
    work.daemon = True
    processes.append(work)
    work.start()
    data_factory.join()
              
if __name__ == '__main__':
    try:
        pool = ThreadPool(processes = multiprocessing.cpu_count()*2)
        pool.map(thread, range(0, 10))
    except:
        pool.close()
        exit()
