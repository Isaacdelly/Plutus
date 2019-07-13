import os
import pickle
import base58
import binascii

count = 0
int = 0
dbname = "%02d" % int
setDb = set()
maxCount = 1000000

DATABASE = r'db/'

reader = [
'balances-zcash-20190712-0052-h6khImgr.csv',
'balances-dashcore-20190712-0033-jHSAv2p2.csv',
'balances-litecoin-20190712-0020-xDAWPYGy.csv',
'balances-dogecoin-20190712-0057-EGLSWmzU.csv',
'balances-bitcoin-abc-20190712-0037-lPQxCcUE.part1.csv',
'balances-bitcoin-20190712-0000-TB9gUfaS.part1.csv',
'balances-bitcoin-abc-20190712-0037-lPQxCcUE.part2.csv',
'balances-bitcoin-20190712-0000-TB9gUfaS.part2.csv'
]# download from https://balances.syndevio.com/

print("write " + DATABASE + dbname + ".pickle")

def tocondensed(add_or_pk,n):
    return base58.b58decode(add_or_pk)[n:-4]

for file in reader:
    with open(file, 'r') as f_obj:
            for i, row in enumerate(f_obj):
                if (row.split(';')[0].startswith(('1','X','D','L'))):# ('Bitcoin','dashcore','dogecoin','litecoin')
                    ripemd_bin = tocondensed(row.split(';')[0],1)
                    ripemd_encoded = binascii.hexlify(ripemd_bin)
                    setDb.add(ripemd_encoded.decode())
                    count += 1
                if (row.split(';')[0].startswith('t1')):# ('zcash')
                    ripemd_bin = tocondensed(row.split(';')[0],2)
                    ripemd_encoded = binascii.hexlify(ripemd_bin)
                    setDb.add(ripemd_encoded.decode())
                    count += 1
                if (count >= maxCount):
                    fileDB = open(DATABASE + dbname + ".pickle", "wb")
                    pickle.dump(setDb, fileDB, protocol=4)
                    fileDB.close()
                    setDb = set()
                    count = 0
                    int += 1
                    dbname = "%02d" % int
                    print("\nwrite " + DATABASE + dbname + ".pickle")
            f_obj.close()

fileDB = open(DATABASE + dbname + ".pickle", "wb")
pickle.dump(setDb, fileDB, protocol=4)
fileDB.close()
setDb = set()

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
