#!/usr/bin/env python
import sys
import os
import csv

def get_uniq_elem_at_column(csv_data, c):
	uniq = set([])
	for line in csv_data[1:]:
		uniq.add(line[c])
	return list(uniq)

def average_at_column(csv_data, c):
	s = 0
	num = 0
	for line in csv_data[1:]:
		s += int(line[c])
		num += 1.0
	return round(s/num, 2)

def get_prof(csv_data):
	return get_uniq_elem_at_column(csv_data, 0)

def get_lab(csv_data):
	return get_uniq_elem_at_column(csv_data, 1)

def gather_data(csv_file):
	csv_data = []
	with open(csv_file, 'rb') as csv_file:
		reader = csv.reader(csv_file)
		for line in reader:
			if line[0].startswith("Obs.:") or line[0] == "":
				break
			else:
				csv_data.append(line)
	p = get_prof(csv_data)
	l = get_lab(csv_data)
	print p
	print l
	print average_at_column(csv_data, 3)

if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
	print "Usage: " + sys.argv[0] + " DIR_DATA" 
	sys.exit(1)
os.chdir(sys.argv[1])

datasets = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".csv")]

for csv_file in datasets:
	gather_data(csv_file)
