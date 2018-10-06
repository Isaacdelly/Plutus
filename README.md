# Plutus Bitcoin Brute Forcer

An automated bitcoin wallet collider that brute forces random wallet addresses within the 2<sup>160</sup> range<br/>

#

# Improvements & TODO

- [x] Improve multiprocessing

- [x] Fix HTTP errors

- [x] Install dependencies when the project starts

- [ ] Create a GUI

- [ ] Find an alternative to an API for balance requests

<br/>

Create an <a href="https://github.com/Isaacdelly/Plutus/issues">issue</a>, so I can add more stuff to improve

#

# Installation & Usage

<b>Python 3+ Required</b>

<b>A Constant Internet Connection Is Required</b>

Installation:
```
git clone https://github.com/Isaacdelly/Plutus.git Plutus
```

Usage:
```
cd Plutus

python plutus.py
```

#

# Proof Of Concept

This program is meant to analyze possible ways Bitcoin could be stolen. Because it is impossible to convert a wallet address back into its private key, this program goes the opposite way and generates a completely random private key, then converts it into its respective Bitcoin address. It then queries the calculated address for a balance and prints the result to the user.

This program does this in a brute-force style, repeatedly generating and converting private keys, and querying balances. The ultimate goal is to randomly find a wallet with a balance out of the 2160 possible wallets in existence. In the event that a wallet with a balance is found, the wallet's private key, public key, wallet address, and balance is stored in a text file `plutus.txt`.

Although this project can be used maliciously, it is simply an exploration into the Bitcoin protocol and advanced encryption and hashing techniques using Python.

#

# How It Works

Private keys are generated randomly to create a 32 byte hexidecimal string using the cryptographically secure `os.urandom()` function.

The private keys are converted into their respective public keys. Then the public keys are converted into their Bitcoin wallet addresses using the `binascii`, `ecdsa`, and `hashlib` Python modules.

The wallet addresses are queried using <a href="https://bitcoinlegacy.blockexplorer.com/api-ref" target="_blank">Block Explorer API</a> to collect balance details.

If the wallet contains a balance, then the private key, public key, wallet address, and balance are saved to a text file `plutus.txt` on the user's hard drive.

This program also utilizes multiprocessing through the `ThreadPool()`, `Process()`, and `pool.map()` functions. Multiprocessing maximizes the usage of your computer's cores, and consumes 100% of your computer's CPU.

#

# Expected Output

If the wallet is empty, then the format `Wallet Address = 0` will be printed. An example is:

>1A5P8ix6XaoCqXmtXxBwwhp5ZkYsqra32C = 0

However, if a balance is found, then the output will include all necessary information about the wallet. A copy of the output will also be saved in a text file titled `plutus.txt` with all balances in Satoshi. An example is:

>address: 1JGM6sREUwt5paFEfHNuzvRy7nXtQdaamn<br/>
>private key: 6694e2d40e786839d48b1b699ab9c318514dc0a0f27f2ccaf7f9f32224ead3a8<br/>
>WIF private key: 5JbTtbihnAnNbBtqZKmkWbrDUeei1bCamqKPrHJ49vQx1CT8oUQ<br/>
>public key: 04475C43E9E58637630E10DB01F2FF38C64430E07E272E4C82C877653B8AF15720E4F98F66B49BB4E91B36D4C08FC4F2E13F0A5079DFCEB1821FA05A9F9F30F361<br/>
>balance: 10000000<br/>

#

# Efficency

On my tested machine, this program is able to brute force `4 wallets a second`, utilizing 100% of my computer's processing power.
