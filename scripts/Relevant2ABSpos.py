#!/usr/bin/python
import sys

from scripts.Fuse_intervals import Interval, IntervalSet

__author__ = 'Thomas'


def getabspos(start, end, temp_its, ori):
    # core function: obtain the absolute genomic coordination out of the relevant pos;\
    # params: start, end for relevant position in the cDNA sequence; temp_its for IntervalSet of the absolute
    #       coordination, ori for the strand orientation
    # returns IntervalSet

    blocklist = []  # [absolute Interval, relevant Interval]
    temp_end = 0
    if ori == '+':
        its = temp_its.items
    else:
        its = temp_its.items[::-1]

    # build a corresponding relevant Interval set
    for i in its:
        temp_start = temp_end + 1
        length = i.end - i.start
        temp_end = temp_start + length
        temp_interval = Interval(temp_start, temp_end)
        blocklist.append(temp_interval)
    # if the query region longer than the cdna region, both ends would be modified
    if start < 1:
        start = 1
    if end > blocklist[-1].end:
        end = blocklist[-1].end

    for index, node in enumerate(blocklist):
        if node.start <= start <= node.end:
            if ori == '-':
                ind_end = index
                abs_end = node.start - start + its[index].end
            else:
                ind_start = index
                abs_start = start - node.start + its[index].start
        if node.start <= end <= node.end:
            if ori == '-':
                ind_start = index
                abs_start = node.end - end + its[index].start
            else:
                ind_end = index
                abs_end = end - node.start + its[index].start
    if ind_start == ind_end:
        temp_interval = Interval(abs_start, abs_end)
        output_its = IntervalSet(temp_interval)
    else:
        temp_interval1 = Interval(abs_start, its[ind_start].end)
        output_its = IntervalSet(temp_interval1)
        temp_interval2 = Interval(its[ind_end].start, abs_end)
        output_its.insert(temp_interval2)
        for i in xrange(ind_start+1, ind_end):
            output_its.insert(its[i])
    return output_its


queryfile = sys.argv[1]
gffile = sys.argv[2]

querylist = []
idlist = []
with open(queryfile, 'r') as f1:
    for line in f1:
        line = line.rstrip('\n')
        elements = line.split()
        gene_name = elements[0]
        rele_start = int(elements[1])
        rele_end = int(elements[2])
        if gene_name not in idlist:
            idlist.append(gene_name)
        push_item = [gene_name, rele_start, rele_end]
        querylist.append(push_item)

cdna = {}  # key: spliced gene name; value: interval sets.
with open(gffile, 'r') as f2:
    block_flag = 'mRNA'  # 'mRNA' is the starting flag for a specific .gff file block
    pick_flag = 'exon'  # 'exon' is the what we pick as the component of the cDNA
    for line in f2:
        line = line.rstrip('\n')
        elements = line.split()
        if len(elements) != 9:
            continue
        line_flag = elements[2]
        temp_id = elements[-1].split(';')[0].split(':')[0].split('=')[1]
        if temp_id not in idlist:
            continue
        if line_flag == block_flag:
            ori = elements[6]  # strand orientation
            temp_its = IntervalSet()
            cdna[temp_id] = [temp_its, ori]
        elif line_flag == pick_flag:
            temp_start = int(elements[3])
            temp_end = int(elements[4])
            temp_interval = Interval(temp_start, temp_end)
            cdna[temp_id][0].insert(temp_interval)
        else:
            continue

for query in querylist:
    name = query[0]
    rele_start = query[1]
    rele_end = query[2]
    out_its = getabspos(rele_start, rele_end, cdna[name][0], cdna[name][1])
    out_its.print_intervalset()
