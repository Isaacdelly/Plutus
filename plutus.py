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
import sys
from multiprocessing import Process, Queue

class pause: # Counts API failures for timeout
    p = 0

def privateKey(): # Generates random 256 bit private key in hex format
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def publicKey(privatekey): # Private Key -> Public Key
    privatekey = binascii.unhexlify(privatekey)
    s = ecdsa.SigningKey.from_string(privatekey, curve = ecdsa.SECP256k1)
    return '04' + binascii.hexlify(s.verifying_key.to_string()).decode('utf-8')

def address(publickey): # Public Key -> Wallet Address
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

def balance(address): # Query API for wallet balance
    return 666

def toWIF(privatekey): # Hex Private Key -> WIF format
    var80 = "80" + str(privatekey) 
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))))

def isRich(address,myList): #Determine if the address belongs to Richie Rich
    if (address in myList):
        print(address+' is in list')
        return 1
    print(address+' not in list')
    return 0

def Plutus(): # Main Plutus Function
    data = [0,0,0,0]
    with open('balances.txt') as file:
        myList= file.read().split()
    while True:
        data[0] = privateKey()
        data[1] = publicKey(data[0])
        data[2] = address(data[1])
        # data[3] = balance(data[2])
        # if (data[3] == -1):
        #     continue
        # if (data[3] == 0):
        #     print("{:<34}".format(str(data[2])) + " = " + str(data[3]))
        # if (data[3] > 0):

        if (isRich(data[2],myList)):
            print ("\naddress: " + str(data[2]) + "\n" +
                   "private key: " + str(data[0]) + "\n" +
                   "WIF private key: " + str(toWIF(str(data[0]))) + "\n" +
                   "public key: " + str(data[1]).upper() + "\n" +
                   "balance: " + str(data[3]) + "\n")
            file = open("plutus.txt","a")
            file.write("address: " + str(data[2]) + "\n" +
                       "private key: " + str(data[0]) + "\n" +
                       "WIF private key: " + str(toWIF(str(data[0]))) + "\n" +
                       "public key: " + str(data[1]).upper() + "\n" +
                       "balance: " + str(data[3]) + "\n\n")
            file.close()

### Multiprocessing Extension Made By Wayne Yao https://github.com/wx-Yao ###
            
def put_dataset(queue,balance,myList):
    while True:
        if queue.qsize() > 100:
            time.sleep(10)
        else:
            privatekey = privateKey()
            publickey = publicKey(privatekey)
            Address = address(publickey)
            WIF = toWIF(privatekey)
            dataset = (Address, privatekey, publickey, WIF)
            queue.put(dataset, block = False)
    return None

def worker(queue,balance,myList):
    time.sleep(1)
    while True:
        if queue.qsize() > 0:
            dataset = queue.get(block = True)
            balan = balance(dataset[0])
            process_balance(dataset, balan,myList)
        else:
            time.sleep(3)
    return None

def process_balance(dataset,balance,myList):
    addr = dataset[0]
    privatekey = dataset[1]
    publickey = dataset[2]
    WIF = dataset[3]

    if (isRich(data[2],myList)):
        file = open("plutus.txt","a")
        file.write("address: " + str(addr) + "\n" +
                   "private key: " + str(privatekey) + "\n" +
                   "WIF private key: " + str(WIF) + "\n" +
                   "public key: " + str(publickey).upper() + "\n" +
                   "balance: " + str(balance) + "\n\n")
        file.close()
    return None

def multi():
    with open('balances.txt') as file:
        myList= file.read().split()
    processes = []
    dataset = Queue()
    datasetProducer = Process(target = put_dataset, args = (dataset,balance,myList))
    datasetProducer.daemon = True
    processes.append(datasetProducer)
    datasetProducer.start()
    for core in range(4):
        work = Process(target = worker, args = (dataset,balance,myList))
        work.deamon = True
        processes.append(work)
        work.start()
    try:
        datasetProducer.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        print('\n\n------------------------\nALL PROCESSES TERMINATED\n')

### End of Multiprocessing Extension ###

def main():
    if ("-m" in sys.argv):
        print("\n-------- MULTIPROCESSING MODE ACTIVATED --------\n")
        time.sleep(3)
        print("\n|-------- Wallet Address --------| = Balance in Satoshi")
        multi()
    else:
        print("\n|-------- Wallet Address --------| = Balance in Satoshi")
        Plutus()

if __name__ == '__main__':
    main()
