#!/usr/bin/env python
import sys
import os
import csv


def get_eval(s):
	if s == "5 - Complet de Acord":
		return 5
	elif s == "4 - ...":
		return 4
	elif s == "3 - ...":
		return 3
	elif s == "2 - ...":
		return 2
	else:
		return 1;

def get_h(s):
	# Students can choose between the following options:
	# We will consider the middle value.
	if s == "80% .. 100%":
		return 90
	elif s == "60% .. 80%":
		return 70
        elif s == "40% .. 60%":
		return 50
	elif s == "20% .. 40%":
		return 30
        else:
            return 10

def get_nota(s):
	if s == "sub 5":
		return 4
	return int(s)

def get_load(s):
	if s == "DA":
		return 2
	elif s == "NU":
		return 0
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
	return csv_data[0][:-4]

def get_prof(csv_data):
	return get_uniq_elem_at_column(csv_data, 2)

def get_lab(csv_data):
	return get_uniq_elem_at_column(csv_data, 3)

def empty_row(csv_data):
	return [""] * len(get_header(csv_data))

def get_stats(text, csv_data, f):
	# titular, asistent
	row = [text, len(csv_data)]

	row.append("")
	row.append("")
	# evaluare generala
	row.append(f(csv_data, get_eval, 4))
	# nota asteptata
	row.append(f(csv_data, float, 5))
	# incarcarea generala
	row.append(f(csv_data, get_eval, 6))
	# dotare locatie
	row.append(f(csv_data, get_eval, 7))
	# participare
	row.append(f(csv_data, get_h, 8))
	# cadrul didactic stapaneste
	row.append(f(csv_data, get_eval, 9))
	# metoda de expunere
	row.append(f(csv_data, get_eval, 10))
	# cursul a stimulat
	row.append(f(csv_data, get_eval, 11))
	# comportament cadru didactic
	row.append(f(csv_data, get_eval, 12))
	# materialele didactice suficiente pentru curs
	row.append(f(csv_data, get_eval, 13))
	# cadrul didactic stapaneste
	row.append(f(csv_data, get_eval, 14))
	# cadrul didactic sustine activitatea individuala
	row.append(f(csv_data, get_eval, 15))
	# cadrul didactic a raspuns intrebarilor
	row.append(f(csv_data, get_eval, 16))
	# comportament adecvat
	row.append(f(csv_data, get_eval, 17))
	# materiale didactice suficiente pentru aplicatii
	row.append(f(csv_data, get_eval, 18))
	# nr. ore saptamana pt teme
	row.append(f(csv_data, float, 19))
	# nr. + dificultate teme
	row.append(f(csv_data, get_eval, 20))
	# temele au ajutat la intelegerea materiei
	row.append(f(csv_data, get_eval, 21))

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

	filter_stats(get_prof, 2, csv_data[1:], writer)
	filter_stats(get_lab, 3, csv_data[1:], writer)

if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
	print "Usage: " + sys.argv[0] + " DIR_DATA"
	sys.exit(1)
os.chdir(sys.argv[1])

datasets = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".csv")]

for csv_file in datasets:
	gather_data(csv_file)
