#!/usr/bin/python
'''
Abolished idea!
'''
__author__ = 'thomas'
import MySQLdb as mdb

con = mdb.connect('localhost', 'root', 'piao2551', '3K_SNP')
with con:
    cur = con.cursor()
    for i in xrange(1, 13):
        chr_id = 'chr{:02d}'.format(i)
        sql = 'CREATE TABLE IF NOT EXISTS '
