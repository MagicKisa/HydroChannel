import sys
import csv
import math

'''
скрипт для того, чтобы в эксель данные читались как числа
не работает и не использутеся
'''

def correct_csv(filename, *rows):
    with open(f'{filename}.csv', newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        arr = [row for row in data]
        
    with open(f'{filename}_cor.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=';')
        for row in arr:
            wr.writerow([math.floor(float(row[int(i)])) for i in rows])
            
correct_csv(sys.argv[1], sys.argv[2])
