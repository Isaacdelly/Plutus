# Database FAQ

This database is a serialized <a href="https://github.com/hiway/python-bloom-filter">bloom filter</a> of all Bitcoin addresses with a positive balance.

The database was created using a third-party program: <a href="https://github.com/graymauser/btcposbal2csv">btcposbal2csv</a> which generates a csv file of all Bitcoin addresses with a positive balance. The csv file was converted into a set, then the set was converted into a bloom filter object, which was then serialized into a `.pickle` file. When the program runs, the file gets deserialized back into a bloom filter object and is used for a balance query.

The name of the file is the date when the database was last updated in month_day_year format. The database will be updated every 3-6 months.

### How Many Addresses Does The Database Have?

The database currently holds XXX Bitcoin addresses. This is also the total number of Bitcoin addresses with a balance that exist in the blockchain.

### How Is The Bloom Filter Configured?

The bloom filter object is initialized with a XX error rate and XX bit size.

### How Can I Verify This Information?

Before running the program, remove the hashtag on <a href="https://github.com/Isaacdelly/p/blob/master/plutus.py#L100">Line 100</a>. This will print the represented object and verify the information on this page.
