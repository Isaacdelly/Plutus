import os
import csv
import pickle

count = 0
int = 0
dbname = "%02d" % int
setDb = set()
maxCount = 1000000

DATABASE = r'db/'

f_obj = open("addresses_with_balance.csv", "r")
reader = csv.DictReader(f_obj, delimiter=',')

print("write " + DATABASE + dbname + ".pickle")

for line in reader:
    if (line["address"].startswith('1')):
        setDb.add(line["address"])
        count += 1
        print("\r" + str(count) + " " + str(line["address"]), end="")
    if (count >= maxCount):
        fileDB = open(DATABASE + dbname + ".pickle", "wb")
        pickle.dump(setDb, fileDB, protocol=4)
        fileDB.close()
        setDb = set()
        count = 0
        int += 1
        dbname = "%02d" % int
        print("\nwrite " + DATABASE + dbname + ".pickle")

fileDB = open(DATABASE + dbname + ".pickle", "wb")
pickle.dump(setDb, fileDB, protocol=4)
fileDB.close()
setDb = set()
f_obj.close()

print("\n")

# To verify the database size, remove the # from the line below
database = [set() for _ in range(5)]
count = len(os.listdir(DATABASE))
half = count // 2
quarter = half // 2
for c, p in enumerate(os.listdir(DATABASE)):
    print('\rreading database: ' + str(c + 1) + '/' + str(count), end = ' ')
    with open(DATABASE + p, 'rb') as file:
        if c + 1 == 21:
            database[4] = database[4] | pickle.load(file)
            continue
        if c < half:
            if c < quarter: database[0] = database[0] | pickle.load(file)
            else: database[1] = database[1] | pickle.load(file)
        else:
            if c < half + quarter: database[2] = database[2] | pickle.load(file)
            else: database[3] = database[3] | pickle.load(file)
print('DONE')

print('database size: ' + str(sum(len(i) for i in database))); quit()
