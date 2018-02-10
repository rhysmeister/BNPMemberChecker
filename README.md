# BNPMemberChecker
A simple tool to check as list of names against a leaked list of BNP Members

# Description

This is a simple took to check a text file of names against a MySQL database containing the names of BNP Members.

The BNP or British National Party, is a right-wing facist organisation.

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

You may wqish to create some indexes on the database to improve performance.

CREATE INDEX idx_fn_ln ON members (first_name(100), last_name(100));

For fulltext feature...

 CREATE FULLTEXT INDEX idx_ft ON bnp.members (first_name, last_name, other);
