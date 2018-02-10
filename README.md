# Plutus

Bitcoin Brute Forcer
<br/>

#

# Installation and Usage

<b>Python 3+ Required</b> 

<b>A Constant Internet Connection Is Required</b>

Installation: 

```
$ git clone https://github.com/Isaacdelly/Plutus

$ cd Plutus

$ pip install -r requirements.txt 
```

Run File: 

```
$ cd Plutus

$ python plutus.py
```

#

# Proof of Concept

This program is meant to analyze possible ways Bitcoin could be stolen. Because it is impossible to convert a wallet address back into its private key, this program goes the opposite way and generates a completely random private key, then converts it into its respective Bitcoin address. It then queries the calculated address for a balance and <a href="#expected-outputs">prints the result</a> to the user.

This program does this in a brute-force style, repeatedly generating and converting private keys, and querying balances. The ultimate goal is to randomly find a wallet with a balance out of the 2<sup>160</sup> possible wallets in existence. However unlikely, it is possible to eventually find a viable wallet. In the event that a wallet with a balance is found, the wallet's private key, public key, wallet address, and balance is stored in a text file for later use.

Although this project can be used maliciously, it is simply an exploration into the Bitcoin protocol and advanced encryption and hashing techniques using Python.

#

# How it Works

Private keys are generated randomly to create a 32 byte hexidecimal string using the cryptographically secure `os.urandom()` function.

The private keys are converted into their respective public keys. Then the public keys are converted into their Bitcoin wallet addresses using the `binascii`, `ecdsa`, and `hashlib` Python modules.

The wallet addresses are queried using <a href="https://bitcoinlegacy.blockexplorer.com/api-ref" target="_blank">Block Explorer API</a> to collect balance details.

If the wallet contains a balance, then the address, private key, public key, and balance are saved to a text file `plutus.txt` on the user's hard drive.

#

# Expected Outputs

<br><img align="center" src="https://media.giphy.com/media/xULW8mRFQ0WDxEDJ5K/giphy.gif"> <br><br>

If the wallet is empty, then the format `Wallet Address = 0` will be printed. An example is:

>1A5P8ix6XaoCqXmtXxBwwhp5ZkYsqra32C = 0

However, if a balance is found, then the output will include all necessary information about the wallet. A copy of the output will also be saved in a text file titled `plutus.txt` with all balances in Satoshi. An example is:

>address: 19pHF5CuWU3tsFX7HUZKurf5KqGufoCF1A<br>
>private key: 0087853d4e05902e9a08b29633b788b0f12f4293988ea8a0469a0080d5384ea2<br>
>WIF private key: KwEjsM4375oE9gW68xZembui4FwdpUXz5yrDF3nTQNm7es7LhzzK<br>
>public key: >046E4C8F608DCAF23EDD4DFFFF8BAB14F379C4D21DAC0E56F3AAA8743D29B08E68AA7C1E86A832F565E27F039BFE364E817E1A402139131F0889ABAB09330028A6<br>
>balance: 100000<br>

#

# Warnings

If you are receiving: 

>HTTP Error Code: (number)<br/>
>Retrying in 5 seconds

Or

>Unable to connect to API after several attempts<br>
>Retrying in 30 seconds

This program queries Block Explorer API for wallet balances making a HTTP request necessary for complete operation. If connection to the API is found to be unresponsive (failing to return a 200 HTTP status) the program will pause for 5 seconds and attempt to continue.

If you are receiving a lot of errors, visit <a href="https://bitcoinlegacy.blockexplorer.com/">Blockexplorer.com</a> to see if their API might be down.

This program also responds to 429 HTTP responses because of the high frequency of server requests. When a 429 is encountered, the program will continue without giving an error. However, if several 429's are received consecutively, the user will get the result `Unable to connect to API after several attempts` and will be forced to wait 30 seconds until the program continues again.

#

# Efficiency

This program is able to handle, generate, and query a private key in 0.5 seconds. However, because this program uses the internet for balance requests, a slower internet connection may impact time efficiency.

#
