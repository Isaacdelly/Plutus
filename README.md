# Plutus Bitcoin Brute Forcer

A Bitcoin wallet collider that brute forces random wallet addresses

# Like This Project? Give It A Star

[![](https://img.shields.io/github/stars/Isaacdelly/Plutus.svg)](https://github.com/Isaacdelly/Plutus)

# Dependencies

<a href="https://www.python.org/downloads/">Python 3.11</a> or higher

Python modules listed in the <a href="/requirements.txt">requirements.txt<a/>

If you have a __Linux__ or __MacOS__ operating system, libgmp3-dev is required. If you have __Windows__ then this is not required. Install by running the command:
```
sudo apt-get install libgmp3-dev
```

# Installation

```
$ git clone https://github.com/Isaacdelly/Plutus.git plutus

$ cd plutus && pip3 install -r requirements.txt
```

# Quick Start

```
$ python3 plutus.py
```

# Proof Of Concept

A private key is a secret number that allows Bitcoins to be spent. If a wallet has Bitcoins in it, then the private key will allow a person to control the wallet and spend whatever balance the wallet has. So this program attempts to find Bitcoin private keys that correlate to wallets with positive balances. However, because it is impossible to know which private keys control wallets with money and which private keys control empty wallets, we have to randomly look at every possible private key that exists and hope to find one that has a balance.

This program is essentially a brute forcing algorithm. It continuously generates random Bitcoin private keys, converts the private keys into their respective wallet addresses, then checks the balance of the addresses. If a wallet with a balance is found, then the private key, public key and wallet address are saved to the text file `plutus.txt` on the user's hard drive. The ultimate goal is to randomly find a wallet with a balance out of the 2<sup>160</sup> possible wallets in existence. 

# How It Works

32 byte hexidecimal strings are generated randomly using the `os.urandom()` function and are used as our private keys.

The private keys are converted into their respective public keys using the `fastecdsa` python library. This is the fastest library to perform secp256k1 signing. If you run this on Windows then `fastecdsa` is not supported, so instead we use `starkbank-ecdsa` library to generate public keys. The public keys are converted into their Bitcoin wallet addresses using the `binascii` and `hashlib` standard libraries.

A pre-calculated database of every funded P2PKH Bitcoin address is included in this project. The generated address is searched within the database, and if it is found that the address has a balance, then the private key, public key and wallet address are saved to the text file `plutus.txt` on the user's hard drive.

This program also utilizes multiprocessing through the `multiprocessing.Process()` function in order to make concurrent calculations.

# Efficiency

It takes `0.002` seconds for this progam to brute force a __single__ Bitcoin address. 

However, through `multiprocessing.Process()` a concurrent process is created for every CPU your computer has. So this program can brute force a single address at a speed of `0.002 ÷ cpu_count()` seconds.

# Database FAQ

An offline database is used to find the balance of generated Bitcoin addresses. Visit <a href="/database/">/database</a> for information.

# Parameters

This program has optional parameters to customize how it runs:

__help__: `python3 plutus.py help` <br />
Prints a short explanation of the parameters and how they work

__time__: `python3 plutus.pt time` <br />
Brute forces a single address and takes a timestamp of how long it took - used for speed testing purposes

__verbose__: 0 or 1 <br />
`python3 plutus.py verbose=1`: When set to 1, then every bitcoin address that gets bruteforced will be printed to the terminal. This has the potential to slow the program down

`python3 plutus.py verbose=0`: When set to 0, the program will not print anything to the terminal and the bruteforcing will work silently. By default verbose is set to 0

__substring__: `python3 plutus.py substring=8`:
To make the program memory efficient, the entire bitcoin address is not loaded from the database. Only the last <__substring__> characters are loaded. This significantly reduces the amount of RAM required to run the program. if you still get memory errors then try making this number smaller, by default it is set to 8. This opens us up to getting false positives (empty addresses mistaken as funded) with a probability of 1/(16^<__substring__>), however it does NOT leave us vulnerable to false negatives (funded addresses being mistaken as empty) so this is an acceptable compromise.

By default the program runs using `python3 plutus.py verbose=0 substring=8` if nothing is passed.
  
# Expected Output

If a wallet with a balance is found, then all necessary information about the wallet will be saved to the text file `plutus.txt`. An example is:

>hex private key: 5A4F3F1CAB44848B2C2C515AE74E9CC487A9982C9DD695810230EA48B1DCEADD<br/>
>WIF private key: 5JW4RCAXDbocFLK9bxqw5cbQwuSn86fpbmz2HhT9nvKMTh68hjm<br/>
>public key: 04393B30BC950F358326062FF28D194A5B28751C1FF2562C02CA4DFB2A864DE63280CC140D0D540EA1A5711D1E519C842684F42445C41CB501B7EA00361699C320<br/>
>uncompressed address: 1Kz2CTvjzkZ3p2BQb5x5DX6GEoHX2jFS45<br/>

# Recent Improvements & TODO

<a href="https://github.com/Isaacdelly/Plutus/issues">Create an issue</a> so I can add more stuff to improve
