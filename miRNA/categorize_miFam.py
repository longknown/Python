#!/usr/bin/python
import sys

# Define monocots and dicots species
monocots = ['sbi', 'sof', 'tae', 'zma', 'bdi', 'ttu', 'ata', 'hvu', 'far', 'ssp', 'egu']
dicots = ['ath', 'bna', 'bol', 'bra', 'cpa', 'gma', 'lja', 'mtr', 'vun', 'ghb',
          'ghr', 'gra', 'ptc', 'sly', 'vvi', 'pvu', 'mdm', 'aqc', 'peu', 'csi',
          'ccl', 'crt', 'ctr', 'rco', 'gar', 'aly', 'ahy', 'gso', 'bgy', 'bcy',
          'tcc', 'rgl', 'cme', 'amg', 'aau', 'ssl', 'dpr', 'nta', 'stu', 'mes',
          'cca', 'lus', 'pgi', 'hbr', 'han', 'hci', 'htu', 'hex', 'har', 'hpe',
          'hpa', 'ppe', 'ama']

class miFam:
    '''Represents a miFam, this class i) all family members; ii) whether osa-MIR exists;
    iii) whether only osa-MIR exists; iv) monocot exists; v) whether dicot exists'''

    def __init__(self, fname):
       self.name = fname
       self.miMembers = []
       self.exist_osa = False
       self.only_osa = 0
       self.exist_monocot = False
       self.exist_dicot = False
       self.population = 0

    def add_member(self, miRNA):
        self.miMembers.append(miRNA)
        self.population += 1
        if miRNA[0:3] == 'osa':
            self.exist_osa = True
            if self.only_osa == 0:
                self.only_osa = 1
        elif miRNA[0:3] in monocots:
            self.exist_monocot = True
            self.only_osa = -1
        elif miRNA[0:3] in dicots:
            self.exist_dicot = True
            self.only_osa = -1

    def __print__(self):
        print self.name + ':'
        print 'population: ' + str(self.population)
        for i in self.miMembers:
            print i
        print '//'

miF_file = sys.argv[1]
print_option = sys.argv[2]
miF_list = []  # To store elements which are miFam type
f1 = file(miF_file)
Fam_num = 0

while True:
    line = f1.readline()
    if len(line) == 0:
        break
    elements = line.rstrip('\n').split()
    if elements[0] == 'ID':
        miF = miFam(elements[1])
        miF_list.append(miF)
    elif elements[0] == 'MI':
        (miF_list[Fam_num]).add_member(elements[2])
    elif elements[0] == '//':
        Fam_num += 1

if print_option == '1':
    print 'Rice Specific miRNA families:'
    for i in miF_list:
        if i.only_osa == 1:
            i.__print__()
            print '\n'
elif print_option == '2':
    print 'only Monocot conserved rice miRNA families:'
    for i in miF_list:
        if i.exist_osa and i.exist_monocot and not i.exist_dicot:
            i.__print__()
            print '\n'
elif print_option == '3':
    print 'only Dicot conserved rice miRNA families:'
    for i in miF_list:
        if i.exist_dicot & i.exist_osa:
            i.__print__()
            print '\n'
elif print_option == '4':
    print 'Monocot & dicot conserved rice miRNA families:'
    for i in miF_list:
        if i.exist_osa & i.exist_dicot & i.exist_monocot:
            i.__print__()
            print '\n'
elif print_option == '5':
    print 'All rice miRNA families:'
    for i in miF_list:
        if i.exist_osa:
            i.__print__()
