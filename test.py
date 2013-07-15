import csv
from sys import argv

script, file = argv

with open(file, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        print ', '.join(row)
