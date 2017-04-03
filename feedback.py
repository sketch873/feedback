#!/usr/bin/env python
import sys
import os
import csv

def get_h(s):
	# Students can choose between the following options:
	# 1-3, 4-6, 7-9, 10-12, 13-15, 16+
	# We will consider the middle value.
	if s == "1-3":
		return 2
	if s == "4-6":
		return 5
	if s == "7-9":
		return 8
	if s == "10-12":
		return 11
	if s == "13-15":
		return 14
	return 17

def get_nota(s):
	if s == "sub 5":
		return 4
	return int(s)

def get_load(s):
	if s == "DA":
		return 2
	return 1

def get_uniq_elem_at_column(csv_data, c):
	uniq = set([])
	for line in csv_data:
		uniq.add(line[c])
	return list(uniq)

def average_at_column(csv_data, f, c):
	s = 0
	num = 0
	for line in csv_data:
		s += f(line[c])
		num += 1.0
	return round(s/num, 2)

def min_at_column(csv_data, f, c):
	minimum = f(csv_data[0][c])
	for line in csv_data:
		if f(line[c]) < minimum:
			minimum = f(line[c])
	return minimum 

def max_at_column(csv_data, f, c):
	maximum = f(csv_data[0][c])
	for line in csv_data:
		if f(line[c]) > maximum:
			maximum = f(line[c])
	return maximum

def get_header(csv_data):
	csv_data[0][0] = "categorie"
	csv_data[0][1] = "count"
	return csv_data[0]

def get_prof(csv_data):
	return get_uniq_elem_at_column(csv_data, 0)

def get_lab(csv_data):
	return get_uniq_elem_at_column(csv_data, 1)

def empty_row(csv_data):
	return [""] * len(get_header(csv_data))

def get_stats(text, csv_data, f):
	# titular, asistent
	row = [text, len(csv_data)]
	# nr. ore
	row.append(f(csv_data, get_h, 2))
	# eval. gen
	row.append(f(csv_data, int, 3))
	# nota asteptata
	row.append(f(csv_data, get_nota, 4))
	# incarcare
	row.append(f(csv_data, get_load, 5))
	# prezenta curs
	row.append(f(csv_data, int, 6))
	# prezenta lab
	row.append(f(csv_data, int, 7))
	# preg c
	row.append(f(csv_data, int, 8))
	# preg l
	row.append(f(csv_data, int, 9))
	# expl clare c
	row.append(f(csv_data, int, 10))
	# expl clare l
	row.append(f(csv_data, int, 11))
	# rasp clare c
	row.append(f(csv_data, int, 12))
	# rasp clare l
	row.append(f(csv_data, int, 13))
	# interes c
	row.append(f(csv_data, int, 14))
	# interes l
	row.append(f(csv_data, int, 15))
	# comport c
	row.append(f(csv_data, int, 16))
	# comport l
	row.append(f(csv_data, int, 17))
	# expl supl c
	row.append(f(csv_data, int, 18))
	# expl supl l
	row.append(f(csv_data, int, 19))
	# materiale c
	row.append(f(csv_data, int, 20))
	# materiale l
	row.append(f(csv_data, int, 21))
	# nr teme
	row.append(f(csv_data, int, 22))
	# indepl ob
	row.append(f(csv_data, int, 23))
	return row

def filter_stats(f, f_id, csv_data, writer):
	p = f(csv_data)
	for e in p:
		a = [row for row in csv_data if row[f_id] == e]
		row = get_stats(e, a, average_at_column)
		writer.writerow(row)

		

def gather_data(csv_file):
	csv_data = []
	with open(csv_file, 'rb') as csv_fd:
		reader = csv.reader(csv_fd)
		for line in reader:
			if line[0].startswith("Obs.:") or line[0] == "":
				break
			else:
				csv_data.append(line)
	csv_result_file = csv_file.rsplit('.', 1)[0] + "-prelucrat.csv"
	csv_result_fd = open(csv_result_file, 'wb')
	writer = csv.writer(csv_result_fd, quoting=csv.QUOTE_ALL)

	print "Generate results in " + sys.argv[1] + "/" + csv_result_file

	writer.writerow(get_header(csv_data))

	row = get_stats("Minim", csv_data[1:], min_at_column)
	writer.writerow(row)

	row = get_stats("Mediu", csv_data[1:], average_at_column)
	writer.writerow(row)

	row = get_stats("Maxim", csv_data[1:], max_at_column)
	writer.writerow(row)

	filter_stats(get_prof, 0, csv_data[1:], writer)
	filter_stats(get_lab, 1, csv_data[1:], writer)
	
if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
	print "Usage: " + sys.argv[0] + " DIR_DATA" 
	sys.exit(1)
os.chdir(sys.argv[1])

datasets = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".csv")]

for csv_file in datasets:
	gather_data(csv_file)
