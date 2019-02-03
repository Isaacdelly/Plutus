# Database FAQ

This database is a serialized <a href="https://github.com/hiway/python-bloom-filter">bloom filter</a> of all Bitcoin addresses with a positive balance.

The database was created using a third-party program: <a href="https://github.com/graymauser/btcposbal2csv">btcposbal2csv</a> which generates a csv file of all Bitcoin addresses with a positive balance. The csv file gets converted into a set, then the set gets converted into a bloom filter object, which then gets serialized into a `.pickle` file. When the program runs, the file gets deserialized back into a bloom filter object and gets used for a balance query.

The name of the file is the date when the database was last updated in month_day_year format. The database will be updated every 3-6 months.

### How Many Addresses Does The Database Have?

There are ~23 million Bitcoin addresses in the database. This is also the total number of Bitcoin addresses with a balance that exist in the blockchain.
