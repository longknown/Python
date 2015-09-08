#!/usr/bin/python

import sys

pedfile = str(sys.argv[1])

f = file(pedfile)
output = '/Users/Thomas/Academy/3K_SNP/filtered/familyID'

f1 = file(output, 'w')
while True:
    line = str(f.readline())
    if len(line) == 0:
        break

    column1 = line.split()[0]
    print column1
    f1.write(column1+'\r')

f.close()
f1.close()
