import requests
# For some weird exceptions that might occur
from requests.exceptions import *
import json
import sys

def get_balance(address):
	
	global blocked
	global global_counter

	# Where do we get the response.status_code for 429?
	# A valid response or in an exception?
	if not blocked:
		response = None
		try:
			response = requests.get("https://blockchain.info/rawaddr/{}".format(address), timeout=0.005)
			global_counter += 1
			if response.status_code == 429:
				blocked = True
				print("We're blocked after {} requests.".format(global_counter))
				for key, value in response.headers.iteritems():
					print("\t{} : {}".format(key, value))
				return -1
			balance = 0
			try:
				balance = response.json()['final_balance']
			except:
				print("Probably a JSONDecodeError, resuming...")
				pass
			return int(balance)
		except (ConnectionError, RequestException, HTTPError, ProxyError, SSLError, Timeout, ConnectTimeout, ReadTimeout, InvalidHeader, ChunkedEncodingError, ContentDecodingError) as e:
			print("Some exception caught: {}".format(e))
			for key, value in response.headers.iteritems():
    				print("\t{} : {}".format(key, value))
			return -1


if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print("Usage: {} FileWithBitcoinAddresses")
		exit(1)

	blocked = False
	address_file = sys.argv[1]
	addrs = []
	global_counter = 0

	with open(address_file, 'r') as fp:
		addrs = [a.rstrip() for a in fp.readlines()]

	for a in addrs:
		bal = get_balance(a)
		if bal < 0:
			print("Hrm...")
			exit(1)
		else:
			print("Balance of {} is {}".format(a, bal))
