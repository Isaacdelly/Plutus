import csv
import bloom_filter
import pickle

print('reading csv file into set')
temp = set()
with open('database.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            if row[0]:
                temp.add(row[0])
        except IndexError:
            continue

print('set -> BF')
filter = bloom_filter.BloomFilter(max_elements=len(temp), error_rate=0.0000001)
for i in temp:
    filter.add(i)
    
print('serializing BF')
with open('database.pickle', 'wb') as handle:
    pickle.dump(filter, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
print('testing')
with open('database.pickle', 'rb') as handle:
    t = pickle.load(handle)
    
print("TEST: " + str(t == filter))
