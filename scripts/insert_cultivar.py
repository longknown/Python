#!/usr/bin/python
import MySQLdb as mdb
from snp import cultivars
__author__ = 'thomas'

con = mdb.connect('localhost', 'root', 'piao2551', '3000osaSNP')
with con:
    cur = con.cursor()
    for i in cultivars:
        cmd = 'INSERT INTO cultivar_accession VALUES ("%s");' % i
        cur.execute(cmd)
    con.commit()
