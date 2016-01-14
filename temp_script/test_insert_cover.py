#!/usr/bin/python
import MySQLdb as mdb
import sys

__author__ = 'thomas'

con = mdb.connect('localhost', 'root', 'piao2551', '3000osaSNP')
filename = sys.argv[1]

with con:
    cur = con.cursor()
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            elements = line.split('-')
            chrid = elements[0]
            _start = int(elements[1])
            _end = int(elements[2])
            interval_cmd = 'SELECT * FROM cover_regions WHERE chr_id="%s" ORDER BY _start;' % chrid
            cur.execute(interval_cmd)
            insert_region_base = 'INSERT INTO cover_regions (chr_id, _start, _end) VALUES '
            region_list = []
            for row in cur.fetchall():
                region_list.append(row)
            if len(region_list) != 0:
                for row in region_list:
                    if _end < row[2]-1:
                        break
                    elif _start <= row[3]+1:
                        _start = min(_start, row[2])
                        _end = max(_end, row[3])
                        delete_cmd = 'DELETE FROM cover_regions WHERE regionNO="%s";' % row[0]
                        cur.execute(delete_cmd)
                    else:
                        continue
            insert_cmd = insert_region_base + '("%s", %s, %s)' % (chrid, _start, _end)
            cur.execute(insert_cmd)
