#!/usr/bin/python
__author__ = 'thomas'
from snp import cultivars
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'piao2551', '3K_SNP')
with con:
    cur = con.cursor()
    for i in cultivars:
        command = 'INSERT INTO cultivar VALUES ("%s");' % i
        cur.execute(command)
