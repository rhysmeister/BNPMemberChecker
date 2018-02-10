import pymysql.cursors, json, argparse


count=0
set_of_last_names = set()

parser = argparse.ArgumentParser(description='Check a text file against a database of BNP Members.')
parser.add_argument('--file', type=str, default="members.txt", help='The list of BNP Members. Should be one name per line. Format is assumed to be <first_name> <middle name> <last name>. Middle names is optional and is ignored in the check. If an extact match is not found we perform an initial check with the first name and last name. This is indicated in the output')
parser.add_argument('--host', type=str, default="localhost")
parser.add_argument('--username', type=str, default="root")
parser.add_argument('--password', type=str, default="secret")
parser.add_argument('--db', type=str, default="bnp")
parser.add_argument('--table', type=str, default="members")
args = parser.parse_args()

# Connect to the database
connection = pymysql.connect(host=args.host,
                             user=args.username,
                             password=args.password,
                             db=args.db,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:



    with connection.cursor() as cursor:
	fp = open(args.file, 'r')
	line = fp.readline()
	while line:
		try:
			first_name, last_name = line.strip().split(" ")
		except ValueError as excep:
			# Try again with middle name
			try:
				first_name, middle_name, last_name = line.strip().split(" ")
			except ValueError as excep:
				print("ValueError on {0}".format(line))
        	# Read a single record
		set_of_last_names.add(last_name.replace("'", "\\'"))
        	sql = "SELECT * FROM {0} WHERE `first_name`=%s AND last_name=%s".format(args.table)
        	cursor.execute(sql, (first_name, last_name))
		result = cursor.fetchone()
		# Try First Initial
		if result is None:
			initial = first_name[0]
                	sql = "SELECT * FROM {0} WHERE first_name = '{1}.' AND CHAR_LENGTH(first_name) <=2 AND last_name='{2}'".format(args.table, initial, last_name.replace("'", "\\'"))
                	cursor.execute(sql)
                	result = cursor.fetchone()
		count += 1
		if count % 10 == 0:
			print("Processed {0} rows".format(count));
		if result is not None:
        		print(result)
		line = fp.readline()

finally:
    connection.close()
