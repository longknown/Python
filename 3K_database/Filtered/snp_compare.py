#!/usr/bin/python

import sys

pedfile = sys.argv[1]

f = file(pedfile)
line_n = 0
while True:
    line_n += 1
    line = str(f.readline())
    if len(line) == 0:
        break

    ls = line.split()

    col_n = 7
    flag = 0
    while True:
        if col_n >= len(ls):
            break
        if ls[col_n-1] != ls[col_n]:
            print str(col_n) + '\t' + str(col_n+1)
            flag = 1
        col_n += 2
    if flag == 1:
        print str(line_n) + '\n\n\n'
