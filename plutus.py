# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly
# https://github.com/Isaacdelly/Plutus

try:
    import os
    import hashlib
    import binascii
    import multiprocessing
    from multiprocessing import Process, Queue
    from multiprocessing.pool import ThreadPool
    import base58
    import ecdsa
    import requests
    # For some weird exceptions that might occur
    from requests.exceptions import *
except ImportError:
    import subprocess
    subprocess.check_call(["python", '-m', 'pip', 'install', 'base58==1.0.0'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'ecdsa==0.13'])
    subprocess.check_call(["python", '-m', 'pip', 'install', 'requests==2.19.1'])
    import base58
    import ecdsa
    import requests


# Presumably rate-limiting or static IP blocking, could also be server down
# for maintenance
bci_blocked = False
bitaps_blocked = False
btc_blocked = False


def generate_private_key():
    return binascii.hexlify(os.urandom(32)).decode('utf-8')

def private_key_to_WIF(private_key):
    var80 = '80' + str(private_key) 
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

#
#   We could add a round-robin option, where the function cycles through
#   the get_balance API options, so it doesn't repeatedly hit the same
#   API too quickly.  In the event an API is down for some reason, it
#   will just move onto the next API.  If they're all down, though, the
#   program will just have to save the addresses, and add an option, e.g.
#   plutus.py --check --file=addresses.txt that it saved because the
#   APIs were down, or no Internet connection/sparodic connectivity
#   for a while.  Otherwise specify --no-api-stop if the program should
#   just quit if all are down.
#
#   https://tools.ietf.org/html/rfc6585#page-3
#
#   TODO: Proper 429 handling, and see if the server gives us a retry-after
#   header.  In that case, we could sleep for that number of seconds, then
#   keep going.  It might be helpful to calculate the number of requests
#   over a time interval before getting a 429, if the server does that with
#   a retry-after header, so we know how many we can do for each API.
#
def get_balance(address):
    
    # TODO: undo the blocking some time, if we receive a valid HTTP
    # header from a server with Retry-After set, if we get a HTTP/1.1 429.
    global bci_blocked
    global bitaps_blocked
    global btc_blocked

    # Where do we get the response.status_code for 429?
    # A valid response or in an exception?
    if not bci_blocked:
        return bci_balance(address)
    elif not bitaps_blocked:
        return bitaps_balance(address)
    elif not btc_blocked:
        return btc_balance(balance)
    else:
        print("Run out of options, blocked from Blockchain, BitAps and BTC.com")

    return -1

def bci_balance(address):
    global bci_blocked
    response = None
    try:
        response = requests.get("https://blockchain.info/rawaddr/{}".format(address), timeout=None)
        if response.status_code == 429:
            bci_blocked = True
            print("We're blocked from BCI.")
            return -1
        balance = 0
        try:
            balance = response.json()['final_balance']
        except:
            print("Probably a JSONDecodeError, resuming...")
            pass
        return int(balance)
    except (ConnectionError, RequestException, HTTPError, ProxyError, SSLError, Timeout, ConnectTimeout, ReadTimeout, InvalidHeader, ChunkedEncodingError, ContentDecodingError) as e:
        print("Exception caught: {}".format(e))
        # Should we really do this or keep trying?
        bci_blocked = True
        return -1

def bitaps_balance(address):
    global bitaps_blocked
    response = None
    try:
        response = requests.get("https://bitaps.com/api/address/{}".format(address), timeout=None)
        if response.status_code == 429:
            bitaps_blocked = True
            print("We're blocked from Bitaps.")
            return -1
        balance = 0
        try:
            balance = response.json()['balance']
        except:
            print("Probably a JSONDecodeError, resuming...")
            pass
        return int(balance)
    except (ConnectionError, RequestException, HTTPError, ProxyError, SSLError, Timeout, ConnectTimeout, ReadTimeout, InvalidHeader, ChunkedEncodingError, ContentDecodingError) as e:
        print("Exception caught: {}".format(e))
        # Should we really do this or keep trying?
        bitaps_blocked = True
        return -1

# balance = response.json()['data']['balance']
def btc_balance(address):
    global btc_blocked
    response = None
    try:
        response = requests.get("https://chain.api.btc.com/v3/address/{}".format(address), timeout=None)
        if response.status_code == 429:
            btc_blocked = True
            print("We're blocked from BTC.com.")
            return -1
        balance = 0
        try:
            balance = response.json()['data']['balance']
        except:
            print("Probably a JSONDecodeError, resuming...")
            pass
        return int(balance)
    except (ConnectionError, RequestException, HTTPError, ProxyError, SSLError, Timeout, ConnectTimeout, ReadTimeout, InvalidHeader, ChunkedEncodingError, ContentDecodingError) as e:
        print("Exception caught: {}".format(e))
        # Should we really do this or keep trying?
        btc_blocked = True
        return -1
    
def data_export(queue):
    while True:
        private_key = generate_private_key()
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)
        data = (private_key, address)
        queue.put(data, block = False)

def worker(queue):
    while True:
        if not queue.empty():
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
    
    bci_blocked = False
    bitaps_blocked = False
    btc_blocked = False

    try:
        pool = ThreadPool(processes = multiprocessing.cpu_count()*2)
        pool.map(thread, range(0, 10))
    except:
        pool.close()
        exit()
