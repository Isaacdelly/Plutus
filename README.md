# Plutus Bitcoin Brute Forcer

A Bitcoin wallet collider that brute forces random wallet addresses

# Like This Project? Give It A Star

[![](https://img.shields.io/github/stars/Isaacdelly/Plutus.svg)](https://github.com/Isaacdelly/Plutus)

# Dependencies

<a href="https://www.python.org/downloads/">Python 3.6</a> or higher

Python modules listed in the <a href="/requirements.txt">requirements.txt<a/>
  
Minimum <a href="#memory-consumption">RAM requirements</a>

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

Bitcoin private keys allow a person to control the wallet that it correlates to. If a wallet has Bitcoins in it, then the private key will allow a person to spend whatever balance the wallet has.

This program is essentially a brute forcing algorithm. It continuously generates random Bitcoin private keys, converts the private keys into their respective wallet addresses, then checks the balance of the addresses. The ultimate goal is to randomly find a wallet with a balance out of the 2<sup>160</sup> possible wallets in existence. 

# How It Works

Private keys are generated randomly to create a 32 byte hexidecimal string using the cryptographically secure `os.urandom()` function.

The private keys are converted into their respective public keys using the `starkbank-ecdsa` Python module. Then the public keys are converted into their Bitcoin wallet addresses using the `binascii` and `hashlib` standard libraries.

A pre-calculated database of every P2PKH Bitcoin address with a positive balance is included in this project. The generated address is searched within the database, and if it is found that the address has a balance, then the private key, public key and wallet address are saved to the text file `plutus.txt` on the user's hard drive.

This program also utilizes multiprocessing through the `multiprocessing.Process()` function in order to make concurrent calculations.

# Efficiency

It takes `0.0032457721` seconds for this progam to brute force a __single__ Bitcoin address. 

However, through `multiprocessing.Process()` a concurrent process is created for every CPU your computer has. So this program can brute force addresses at a speed of `0.0032457721 ÷ cpu_count()` seconds.

# Database FAQ

Visit <a href="/database/">/database</a> for information

# Expected Output

Every time this program checks the balance of a generated address, it will print the result to the user. If an empty wallet is found, then the wallet address will be printed to the terminal. An example is:

>1Kz2CTvjzkZ3p2BQb5x5DX6GEoHX2jFS45

However, if a wallet with a balance is found, then all necessary information about the wallet will be saved to the text file `plutus.txt`. An example is:

>hex private key: 5A4F3F1CAB44848B2C2C515AE74E9CC487A9982C9DD695810230EA48B1DCEADD<br/>
>WIF private key: 5JW4RCAXDbocFLK9bxqw5cbQwuSn86fpbmz2HhT9nvKMTh68hjm<br/>
>public key: 04393B30BC950F358326062FF28D194A5B28751C1FF2562C02CA4DFB2A864DE63280CC140D0D540EA1A5711D1E519C842684F42445C41CB501B7EA00361699C320<br/>
>address: 1Kz2CTvjzkZ3p2BQb5x5DX6GEoHX2jFS45<br/>

# Memory Consumption

This program uses approximately 2GB of RAM per CPU. Because this program uses multiprocessing, some data gets shared between threads making it difficult to accurately measure RAM usage.

![Imgur](https://i.imgur.com/9Cq0yf3.png)

The memory consumption stack trace was made by using <a href="https://pypi.org/project/memory-profiler/">mprof</a> to monitor this program brute force 10,000 addresses on a 4 logical processor machine with 8GB of RAM. As a result, 4 child processes were created, each consuming 2100MiB of RAM (~2GB).

# Recent Improvements & TODO

- [X] Fixed typos/formatting

- [ ] Updated database

<a href="https://github.com/Isaacdelly/Plutus/issues">Create an issue</a> so I can add more stuff to improve
