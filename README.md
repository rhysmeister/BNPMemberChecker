# BNPMemberChecker
A simple tool to check a list of names against a leaked list of BNP Members

# Description

This is a simple tool to check a text file of names against a MySQL database containing the names of BNP Members.

The BNP, or British National Party, is a right-wing facist organisation.

About the data: https://wikileaks.org/wiki/British_National_Party_membership_and_contacts_list,_2007-2008

About the BNP https://en.wikipedia.org/wiki/British_National_Party

# Setup

1. Create a database in MySQL called 'bnp' - mysql> CREATE DATABASE bnp;
2. Extract the archive - linux> unzip bnp-members.sql.zip
3. Load the data from the sql dump - linux> mysql bnp -u user -p < bnp-members.sql
4. Install PyMySQL - linux> python -m pip install PyMySQL
5. Install Pandas - linux> python -m pip install tabulate
6. Run the tool - python bnp.py

# Additional

You may wish to create some indexes on the database to improve performance.

```
CREATE INDEX idx_fn_ln ON members (first_name(100), last_name(100));
```
For fulltext feature...
```
 CREATE FULLTEXT INDEX idx_ft ON bnp.members (first_name, last_name, other);
```
 # Usage
```
usage: bnp [-h] [--file FILE] [--host HOST] [--username USERNAME]
           [--password PASSWORD] [--db DB] [--table TABLE]
           [--tablefmt TABLEFMT] [--fulltext] [--text TEXT] [--json JSON]
           [--debug]

Check a text file against a database of BNP Members. If you only have one name
then check manually. This tool will never be as good as a human at matching
names.

optional arguments:
  -h, --help           show this help message and exit
  --file FILE          The list of names to check against the BNP dataset.
                       Should be one name per line. Format is assumed to be
                       <first_name> <middle name> <last name>. Middle names is
                       optional and is ignored in the check. If an extact
                       match is not found we perform an initial check with the
                       first name and last name. This is indicated in the
                       output
  --host HOST          MySQL hostname
  --username USERNAME  MySQL username
  --password PASSWORD  MySQL password
  --db DB              MySQL database
  --table TABLE        MySQL table
  --tablefmt TABLEFMT  Output table format
  --fulltext           Perform an additional fulltext search on the dataset
  --text TEXT          Text to use with the fulltext search feature. Useful
                       for adhoc searching of the dataset.
  --json JSON          JSON file containing a list of dictionaries to check
                       against the BNP member database. See README for format
                       details.
  --debug              Output debugging information
```
# JSON Support

JSON Support has been added and supports the following data format...

[
 {
   "name": "Dr Who",
   "id": "123456",
   "administrator": false
 },
 {
   "name": "Betty Boo",
   "id": "654321",
   "administrator": false
 },
 {
   "name": "Joe Bloggs",
   "id": "123450",
   "administrator": false
 }
 ]

 This data can be extracted from quite simply from the Facebook graph API (i.e. Groups)

http://www.json-xls.com/how-to-export-facebook-group-members-to-excel
https://developers.facebook.com/tools/explorer

This data should be saved to a file. Then the process can use this data with the following command.

./bnp --json /path/to/data.json
