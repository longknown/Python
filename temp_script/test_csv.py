#!/usr/bin/python
import sys
import csv

fn = sys.argv[1]

with open(fn) as f:
    reader = csv.DictReader(f)
    print reader.fieldnames
    print type(reader.fieldnames)
