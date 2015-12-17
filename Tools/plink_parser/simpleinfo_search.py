#!/usr/bin/python
__author__ = 'Thomas'

import MySQLdb as mdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def search_snp(cur, chr_id, start, end):
    '''
    :param cur: The cursor of the database;
    :param chr_id: chromosome id
    :param start: starting position (int)
    :param end: ending position (int)
    :return: returns an array of SNP
    '''
    if end < start:
        print 'Error Query: end < start'
        return None
    command = 'SELECT * FROM SNP WHERE chr_id="%s" AND position BETWEEN %s AND %s;' % (chr_id, start, end)
    cur.execute(command)
    rows = cur.fetchall()
    return rows

query_f = sys.argv[1]
# The query file format: jobname(miRNA name), chr_id, start, end
if len(sys.argv) > 2:
    out_fn = sys.argv[2]
    out_f = open(out_fn, 'w')
else:
    out_f = sys.stdout

con = mdb.connect('localhost', 'root', 'piao2551', '3K_SNP')
with con:
    cur = con.cursor()
    with open(query_f, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            elements = line.split()
            job = elements[0]
            chr_id = elements[1]
            start = int(elements[2])
            end = int(elements[3])
            result = search_snp(cur, chr_id, start, end)
            printout = ''
            for row in result:
                row_list = list(row)
                row_list = [str(i) for i in row_list]
                row_list.insert(0, job)
                printout += '\t'.join(row_list) + '\n'
            out_f.write(printout)
out_f.close()
