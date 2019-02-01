import math
import mmh3
import pickle
import os

from bitarray import bitarray

DATABASE = r'database/JAN_09_2019/'
BLOOM_FILTER_NAME = 'filter.bf'


class BloomFilter:

    def __init__(self, n_of_elements, error_rate):
        self.size = n_of_elements
        self.error_rate = error_rate
        self.n_of_bits = self._compute_n_of_bits()
        self.bit_array = bitarray(self.n_of_bits)
        self.hash_count = self._get_n_of_hashes()

    def add(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.n_of_bits
            self.bit_array[result] = 1

    def lookup(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.n_of_bits
            if self.bit_array[result] == 0:
                return False
        return True

    def _compute_n_of_bits(self):
        return int(math.ceil(self.size * abs(math.log(self.error_rate)) / math.pow(math.log(2), 2)))

    def _get_n_of_hashes(self):
        return int(math.ceil((self.n_of_bits / self.size) * math.log(2)))

    def __str__(self):
        return "Bloom filter stats: bits= {}, hashes= {}, err_rate= {}".format(self.n_of_bits, self.hash_count, self.error_rate)

    def serialize(self):
        with open(BLOOM_FILTER_NAME, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def deserialize():
        with open(BLOOM_FILTER_NAME, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def convert_db_to_bloom_filter(path = DATABASE, n_of_elements=25000000, error_rate=0.00001):
        bf = BloomFilter(n_of_elements, error_rate)
        count = len(os.listdir(path))
        for c, p in enumerate(os.listdir(path)):
            with open(path + p, 'rb') as file:
                print('\rConverting database to bloom filter: ' + str(c + 1) + '/' + str(count), end='')
                addresses = pickle.load(file)
                for address in addresses:
                    bf.add(address)
        bf.serialize()
