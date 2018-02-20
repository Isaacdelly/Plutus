# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus
# Donate: 1B1k2fMs6kEmpxdYor6qvd2MRVUX2zGEHa

import requests
import os
import binascii
import ecdsa
import hashlib
import base58
import time
from multiprocessing import Process, Queue

class pause:
    p = 0

def privateKey():
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def publicKey(privatekey):
    privatekey = binascii.unhexlify(privatekey)
    s = ecdsa.SigningKey.from_string(privatekey, curve = ecdsa.SECP256k1)
    return '04' + binascii.hexlify(s.verifying_key.to_string()).decode('utf-8')

def address(publickey):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    c = '0'; byte = '00'; zero = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(publickey.encode())).digest())
    a = (byte + var.hexdigest())
    doublehash = hashlib.sha256(hashlib.sha256(binascii.unhexlify(a.encode())).digest()).hexdigest()
    address = a + doublehash[0:8]
    for char in address:
        if (char != c):
            break
        zero += 1
    zero = zero // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod (n, 58)
        output.append(alphabet[remainder])
    count = 0
    while (count < zero):
        output.append(alphabet[0])
        count += 1
    return ''.join(output[::-1])


def balance(address):
    try:
        API = requests.get("https://bitcoinlegacy.blockexplorer.com/api/addr/" + str(address) + "/balance")
        if (API.status_code == 429):
            pause.p += 1
            if (pause.p >= 10):
                print ("\nUnable to connect to API after several attempts\nRetrying in 30 seconds\n")
                time.sleep(30)
                pause.p = 0  
            return -1
        if (API.status_code != 200 and API.status_code != 400 and API.status_code != 429):
            print("\nHTTP Error Code: " + str(API.status_code) + "\nRetrying in 5 seconds\n")
            time.sleep(5)
            return -1
        balance = int(API.text)
        pause.p = 0
        return balance
    except:
        pause.p += 1
        if (pause.p >= 10):
            print ("\nUnable to connect to API after several attempts\nRetrying in 30 seconds\n")
            time.sleep(30)
            pause.p = 0   
        return -1

def toWIF(privatekey):
    var80 = "80" + str(privatekey) 
    var = hashlib.sha256(binascii.unhexlify(var80)).hexdigest()
    var = hashlib.sha256(binascii.unhexlify(var)).hexdigest()    
    checksum = var[0:8]
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(checksum))))

##################
#format of dataset:
# 0: address
# 1: private key
# 2: public key
# 3: WIF
#################
def put_dataset(queue):
    while 1:
        if queue.qsize()>100:
            time.sleep(10)
        else:
            privatekey=privateKey()
            publickey=publicKey(privatekey)
            Address=address(publickey)
            WIF=toWIF(privatekey)
            
            dataset=(Address,privatekey,publickey,WIF)
            queue.put(dataset,block=False)
    return None

def worker(queue):
    time.sleep(1)
    while 1:
        if queue.qsize()>0:
            dataset=queue.get(block=True)
            balan=balance(dataset[0])
            process_balance(dataset,balan)
        else:
            time.sleep(3)
    return None

def process_balance(dataset,balance):
    if balance == -1 :
        return None
    elif balance == 0 :
        print("{:<34}".format(str(dataset[0])) + " = " + str(balance))
        return None
    else:
        addr=dataset[0]
        privatekey=dataset[1]
        publickey=dataset[2]
        WIF=dataset[3]
        file = open("plutus.txt","a")
        file.write("address: " + str(addr) + "\n" +
                   "private key: " + str(privatekey) + "\n" +
                   "WIF private key: " + str(WIF) + "\n" +
                   "public key: " + str(publickey).upper() + "\n" +
                   "balance: " + str(balance) + "\n" +
                   "Donate to the author of this program: 1B1k2fMs6kEmpxdYor6qvd2MRVUX2zGEHa\n\n")
        file.close()
    return None

if __name__ == '__main__':
    print("\n|-------- Wallet Address --------| = Balance in Satoshi")
    processes=[]
    dataset=Queue()
    datasetProducer=Process(target=put_dataset,args=(dataset,))
    datasetProducer.daemon=True
    processes.append(datasetProducer)
    datasetProducer.start()
    for core in range(4):
        work=Process(target=worker,args=(dataset,))
        work.deamon=True
        processes.append(work)
        work.start()
    try:
        datasetProducer.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        print('\n -----------------------\n All processes terminated.')
