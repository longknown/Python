#!/usr/bin/python
import MySQLdb as mdb
import sys
__author__ = 'Thomas'

reload(sys)
sys.setdefaultencoding('utf-8')


def search_snp(cur, chr_id, start, end):
    '''
    :param cur: The cursor of the database;
    :param chr_id: chromosome id
    :param start: starting position (int)
    :param end: ending position (int)
    :return: returns an array of SELECT * FROM cover_regions WHERE chr_id="chr04" AND _start<=5620010 AND _end>=5626000;SNP
    '''
    if end < start:
        print 'Error Query: end < start'
        return None
    command = 'SELECT * FROM SNP WHERE chr_id="%s" AND position BETWEEN %s AND %s;' % (chr_id, start, end)
    cur.execute(command)
    rows = cur.fetchall()
    return rows

query_f = sys.argv[1]
# The query file format: job_name(miRNA name), chr_id, start, end
if len(sys.argv) > 2:
    out_fn = sys.argv[2]
    out_f = open(out_fn, 'w')
else:
    out_f = sys.stdout

con = mdb.connect('localhost', 'root', 'piao2551', '3000osaSNP')
with con:
    cur = con.cursor()
    with open(query_f, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            elements = line.split()
            job = elements[0]
            chr_id = elements[1]
            printout = ''
            for i in xrange(2, len(elements), 2):
                start = int(elements[i])
                end = int(elements[i+1])
                test_cover_cmd = 'SELECT * FROM cover_regions WHERE chr_id="%s" AND _start<=%s AND _end>=%s;' %\
                                 (chr_id, start, end)
                cur.execute(test_cover_cmd)
                if len(cur.fetchall()) == 0:
                    download_start = (start / 5000) * 5000 + 1
                    download_end = (end / 5000 + 1) * 5000
                    print 'Sorry, the query region is not available!'
                    print line
                    print 'Please download genomic regions from oryzasnp.org/iric-portal'
                    print '%s [%s, %s]\n' % (chr_id, download_start, download_end)
                    continue
                result = search_snp(cur, chr_id, start, end)
                for row in result:
                    row_list = list(row)
                    row_list = [str(i) for i in row_list]
                    row_list.insert(0, job)
                    printout += '\t'.join(row_list) + '\n'
            out_f.write(printout)
out_f.close()
