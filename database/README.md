# Database FAQ

This database is a serialized `set()` of all Bitcoin addresses with a positive balance.

The database was created using a third-party program: <a href="https://github.com/graymauser/btcposbal2csv">btcposbal2csv</a> which generates a csv file of all Bitcoin addresses with a positive balance. The csv file was converted into a set and the set was serialized into several `.pickle` files each holding 1,000,000 Bitcoin addresses. When the program runs, the files in the database get deserialized and combined to be used for a balance query.

The name of the database folder is the date when the database was last updated in month_day_year format. The database will be updated every 3-6 months.

### How Many Addresses Does The Database Have?

The database currently holds `22,514,712 Bitcoin addresses`. This is also the total number of Bitcoin addresses with a balance that exist in the blockchain.

This can be verified by removing the hashtag on <a href=https://github.com/Isaacdelly/p/blob/master/plutus.py#L113>Line 113</a> before running the program. This will print the size of the database.

### Why Are There So Many Files?

There are multiple `.pickle` files because GitHub limits file uploads to 100 MB. The single serialized file is too large, so it was split into multiple files each under 100 MB in order to be uploaded to GitHub.
