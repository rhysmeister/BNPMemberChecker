import pymysql.cursors, json

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='bnp',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
count=0
set_of_last_names = set()

try:

    with connection.cursor() as cursor:
	fp = open('/Users/rhyscampbell/Documents/clause_one_members_20180207.txt', 'r')
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
        	sql = "SELECT * FROM `members` WHERE `first_name`=%s AND last_name=%s"
        	cursor.execute(sql, (first_name, last_name))
		result = cursor.fetchone()
		# Try First Initial 
		if result is None:
			initial = first_name[0]
                	sql = "SELECT * FROM members WHERE first_name = '{0}.' AND CHAR_LENGTH(first_name) <=2 AND last_name='{1}'".format(initial, last_name.replace("'", "\\'"))
                	cursor.execute(sql)
                	result = cursor.fetchone()
		count += 1
		if count % 10 == 0:
			print("Processed {0} rows".format(count));
		if result is not None:
        		print(result)
		line = fp.readline()
	ln_str = "','".join(map(str, set_of_last_names))
	sql = "SELECT last_name, COUNT(*) as cnt FROM members WHERE last_name IN ('{0}') GROUP BY last_name ORDER BY last_name".format(ln_str)
	print(sql)
	cursor.execute(sql)
	print(cursor.fetchall())
finally:
    connection.close()
