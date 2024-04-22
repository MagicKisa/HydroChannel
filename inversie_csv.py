import sys
import csv

coord_col = 0
time_col = -1

def inverse(filename):
    with open(filename, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        arr = [row for row in data]
        
    with open(f'{filename.split(".csv")[0]}_inv.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=';')
        end1 = float(arr[-1][coord_col])
        end2 = float(arr[-1][time_col])
        for i in range(len(arr)):
            arr[len(arr) - 1 - i][coord_col] = end1- float(arr[len(arr) - 1 - i][coord_col])
            arr[len(arr) - 1 - i][time_col] = end2 - float(arr[len(arr) - 1 - i][time_col])
            wr.writerow(arr[len(arr) - 1 - i])
            
inverse(sys.argv[1])
