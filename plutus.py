# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

import requests
import os
import binascii
import ecdsa
import hashlib
import time
import numpy

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
        API = requests.get("https://blockexplorer.com/api/addr/" + str(address) + "/balance")
        if (API.status_code == 429):
            pause.p += 1
            if (pause.p == 10):
                print ("\nUnable to connect to API after several attempts\nRetrying in 30 seconds\n")
                time.sleep(30)
                pause.p = 0  
            return -1
        if (API.status_code != 200 and API.status_code != 400 and API.status_code != 429):
            print("\nHTTP Error Code: " + str(API.status_code) + "\nRetrying in 5 seconds\n")
            time.sleep(5)
            return -1
        balance = numpy.int64(API.text)
        pause.p = 0
        return balance
    except:
        pause.p += 1
        if (pause.p == 10):
            print ("\nUnable to connect to API after several attempts\nRetrying in 30 seconds\n")
            time.sleep(30)
            pause.p = 0   
        return -1

def main():
    data = [0,0,0,0]
    while True:
        data[0] = privateKey()
        data[1] = publicKey(data[0])
        data[2] = address(data[1])
        data[3] = balance(data[2])
        if (data[3] == -1):
            continue
        if (data[3] == 0):
            print("{:<34}".format(str(data[2])) + " = " + str(data[3]))
        if (data[3] > 0):
            print ("\naddress: " + str(data[2]) + "\n" +
                   "private key: " + str(data[0]) + "\n" +
                   "public key: " + str(data[1]).upper() + "\n" +
                   "balance: " + str(data[3]) + "\n")
            file = open("plutus.txt","a")
            file.write("address: " + str(data[2]) + "\n" +
                       "private key: " + str(data[0]) + "\n" +
                       "public key: " + str(data[1]).upper() + "\n" +
                       "balance: " + str(data[3]) + "\n\n")
            file.close()

print("\n|-------- Wallet Address --------| = Balance in Satoshi")
if __name__ == '__main__':
    main()
