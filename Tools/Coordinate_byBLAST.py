#!/usr/bin/python
import sys
import subprocess

seqfile = sys.argv[1]
db_name = sys.argv[2]

with open(seqfile, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        mirna = elements[0]
        seq = elements[1]
        fa_content = '>' + mirna + '\n' + seq
        with open('query.fa', 'w') as fw:
            fw.write(fa_content)
        cmds = ['blastn', '-query', 'query.fa', '-db', db_name, '-out', mirna+'.html', '-html']
        subprocess.call(cmds)
