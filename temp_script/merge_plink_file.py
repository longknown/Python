#!/usr/bin/python
__author__ = 'Thomas'

import sys
import os

path = sys.argv[1]
for i in os.listdir(path):
    if i[-3:] == 'map':
        header = i[:-4]
        print header+'.ped', header+'.map'