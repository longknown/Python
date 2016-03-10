#!/usr/bin/python
import MySQLdb as mdb
'''
This module is a sub-function to grasp the haplotype and corresponding cultivar data from the local machine.
It will be called in the main.py, and finally produce a file containing the haplotype pattern and cultivar set.
'''

__author__ = 'thomas'


def _grasp_pattern(hap_list):  # This function takes the list of 'Haplotype' Module as parameter;
    con = mdb.connect(host='localhost', user='root', passwd='piao2551', db='3000osaSNP')
    cul_set = []

    with con:
        cur = con.cursor()
        # obtain the cultivars
        cul_sql = 'SELECT * FROM cultivar ORDER BY name ASC;'
        cur.execute(cul_sql)
        for row in cur.fetchall():
            cul_set.append(row[0])
