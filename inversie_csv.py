import sys
import csv


def inverse(filename):
    with open(filename, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        arr = [row for row in data]
        
    with open(f'{filename.split(".csv")[0]}_inv.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=';')
        end1 = float(arr[-1][0])
        end2 = float(arr[-1][3])
        for i in range(len(arr)):
            arr[len(arr) - 1 - i][0] = end1- float(arr[len(arr) - 1 - i][0])
            arr[len(arr) - 1 - i][5] = end2 - float(arr[len(arr) - 1 - i][5])
            wr.writerow(arr[len(arr) - 1 - i])
            
inverse(sys.argv[1])