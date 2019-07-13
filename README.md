# Plutus Bitcoin and altcoins Brute Forcer

A Bitcoin and altcoins wallet collider that brute forces random wallet RipeMD-160	addresses

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

A private key is a secret number that allows Bitcoins and altcoin to be spent. If a wallet has Bitcoins or altcoin in it, then the private key will allow a person to control the wallet and spend whatever balance the wallet has. So this program attempts to find private keys that correlate to wallets with positive balances. However, because it is impossible to know which private keys control wallets with money and which private keys control empty wallets, we have to randomly look at every possible private key that exists and hope to find one that has a balance.

This program is essentially a brute forcing algorithm. It continuously generates random private keys, converts the private keys into their respective ripemd160 addresses, then checks the balance of the addresses. If a wallet with a balance is found, then the private key, public key and wallet address are saved to the text file `plutus.txt` on the user's hard drive. The ultimate goal is to randomly find a wallet with a balance out of the 2<sup>160</sup> possible wallets in existence. 

# How It Works

Private keys are generated randomly to create a 32 byte hexidecimal string using the cryptographically secure `os.urandom()` function.

The private keys are converted into their respective public keys using the `starkbank-ecdsa` Python module. Then the public keys are converted into their Bitcoin wallet addresses using the `binascii` and `hashlib` standard libraries.

A pre-calculated database of every P2PKH Bitcoin address with a positive balance is included in this project. The generated address is searched within the database, and if it is found that the address has a balance, then the private key, public key and wallet address are saved to the text file `plutus.txt` on the user's hard drive.

This program also utilizes multiprocessing through the `multiprocessing.Process()` function in order to make concurrent calculations.

# Efficiency

It takes `0.0032457721` seconds for this progam to brute force a __single__  address. 

However, through `multiprocessing.Process()` a concurrent process is created for every CPU your computer has. So this program can brute force addresses at a speed of `0.0032457721 ÷ cpu_count()` seconds.

# Database FAQ

An offline database is used to find the balance of generated Bitcoin addresses. Visit <a href="/database/">/database</a> for information.

# Expected Output

Every time this program checks the balance of a generated address, it will print the result to the user. If an empty wallet is found, then the wallet address will be printed to the terminal. An example is:

>91b24bf9f5288532960ac687abb035127b1d28a5

However, if a wallet with a balance is found, then all necessary information about the wallet will be saved to the text file `plutus.csv`. An example is:

>1 91b24bf9f5288532960ac687abb035127b1d28a5

# Memory Consumption

This program uses approximately 2GB of RAM per CPU. Because this program uses multiprocessing, some data gets shared between threads making it difficult to accurately measure RAM usage.

![Imgur](https://i.imgur.com/9Cq0yf3.png)

The memory consumption stack trace was made by using <a href="https://pypi.org/project/memory-profiler/">mprof</a> to monitor this program brute force 10,000 addresses on a 4 logical processor machine with 8GB of RAM. As a result, 4 child processes were created, each consuming 2100MiB of RAM (~2GB).

# Recent Improvements & TODO

- [X] Fixed typos/formatting

- [ ] Updated database

<a href="https://github.com/Isaacdelly/Plutus/issues">Create an issue</a> so I can add more stuff to improve
