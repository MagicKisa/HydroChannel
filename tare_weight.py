import sys
import csv
import time
import datetime


def date_to_seconds(date):
    #Переводит локальное время в секунды 
    try:
        t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    t = (t-datetime.datetime(1970,1,1)).total_seconds()
    return t

def tare(filename):
    '''
    требует посчитанный approx_rate.csv в формате
    тарированное значение = (нетарированное значение - approx_rates[1]) / approx_rates[0]
    approx_rates должен содержать два числа разделенные точкой с запятой

    для файла filename создает файл с суффиксом _tare содержащий тарированные значения силы
    '''
    with open(filename, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        arr = [row for row in data]
        
    with open("approx_rate.csv", newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=';')
        rates = [row for row in data]
        rates = [float(col) for col in rates[0]]
        
    with open(f'{filename.split(".")[0]}_tare.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=';')
        stamp = date_to_seconds(arr[0][1])
        for row in arr:
            try:
                #row[0] = int(row[0]) * 0.0004944 - 2142.4
                row[0] = (int(row[0]) - rates[1]) / rates[0]  
            except ValueError:
                row[0] = 0
            #row[1] = date_to_seconds(row[1]) - stamp
            wr.writerow(row)

# если запустить python3 tare_weight.py fast то при наличии всех файлов экспериментов 1..10 и back посчитает для всех тарированные файлы и сохранит
            
if sys.argv[-1] == 'fast':
    for i in range(1, 11):
        tare(f"{i}_0.csv")
    tare("back_0.csv")
# если запустить в формате python3 tare_weight.py 1_0.csv 2_0.csv 3_0.csv ... посчитает для каждого включенного файла тарированные значения
else:
    for i in range(1, len(sys.argv)):
        tare(sys.argv[i])


