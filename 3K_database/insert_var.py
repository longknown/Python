#!/usr/bin/python

import sys
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

varfile = sys.argv[1]
table = sys.argv[2]

# MySQL database handling
db = mdb.Connect('localhost', 'root', 'piao2551', '3K_SNP', charset='utf8')
cursor = db.cursor()

f = file(varfile)

while True:
    line = f.readline()
    if len(line) == 0:
        break

    line = line.rstrip('\n')

    # Split the TAB-delimited table into specific columns
    column = line.split('\t')
    uniq_id = column[0]
    var_name = column[1]
    other_name = column[2]
    orig_country = column[3]
    cul_group = column[4]
    SRA_acce = column[5]

    # Insert the data into database
    try:
        cursor.execute('insert into %s values(NULL, "%s", "%s", "%s", "%s", "%s", "%s");' % \
        (table, uniq_id, var_name, other_name, orig_country, cul_group, SRA_acce))
        db.commit()
    except db.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

db.close()
f.close()
