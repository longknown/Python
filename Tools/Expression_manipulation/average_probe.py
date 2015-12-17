#!/usr/bin/python
import sys

__author__ = 'Thomas'


def func(a, b):
    return map(lambda x1, x2: x1+x2, a, b)

fw = open('output', 'w')
exp_file = sys.argv[1]

id_exp = {}
with open(exp_file, 'r') as f:
    header = f.readline()
    fw.write(header)
    for line in f:
        line = line.rstrip('\n')
        elements = line.split()
        uniq_id = elements[0][:-2]
        exp_data = [float(x) for x in elements[1:]]
        if uniq_id not in id_exp:
            id_exp[uniq_id] = []
        id_exp[uniq_id].append(exp_data)

for i in id_exp:
    sum_data = reduce(func, id_exp[i])
    num = len(id_exp[i])
    average_data = [str(x/num) for x in sum_data]
    print_line = '\t'.join([i]+average_data)
    fw.write(print_line+'\n')
