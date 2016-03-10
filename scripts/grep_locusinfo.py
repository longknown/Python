#!/usr/bin/python
import sys

__author__ = 'Thomas'

locusfile = sys.argv[1]
infofile = sys.argv[2]

locuslist = []
with open(locusfile, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        locuslist.append(line)

output_content = ''
with open(infofile, 'r') as f2:
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        name = elements[2]
        if name in locuslist:
            output_content += line + '\n'

with open('grep_file', 'w') as f3:
    f3.write(output_content)