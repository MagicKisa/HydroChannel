import csv
import sys
import time
import datetime
# число зубчиков на датчике скорости
wheel_pins = 3600
# длина колеса датчика скорости
wheel_length = 0.25132741
x_scale = wheel_length / wheel_pins

arr = []


def correct_speed(res):
    '''
    переводит скорость из импульсов в секунды
    берется два соседних значения импульсов, из одного вычитается другое, делится на промежуток времени и умножается на масштабный коэффициент посчитаный выше
    '''
    x = float(res[0][0])
    res[0].append(x)
    for i in range(1, len(res)):
        time_del = date_to_seconds(res[i][1]) - date_to_seconds(res[i - 1][1])
        x += float(res[i][0])
        res[i].append(x * x_scale)
        res[i][0] = float(int(res[i][0]) * x_scale / time_del) * 1.0171 - 0.00005
        
def date_to_seconds(date):
    # Переводит локальное время в секунды 
    try:
        t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    t = (t-datetime.datetime(1970,1,1)).total_seconds()
    return t
    
def seconds_to_date(seconds):
    # Переводит секунды в локальное время( МСК +3 UTC )
    utc_epoch = 3 * 3600
    seconds -= utc_epoch
    return datetime.datetime.fromtimestamp(seconds).strftime("%Y-%m-%d %H:%M:%S.%f")


# эта процедура нужна для работы conv.py, применяет эту функцию к 1_1.csv, 2_1.csv ... 10_1.csv а так же back.csv
'''Если скрипт запускается как
python3 Correct_speed fast то работает эта часть
входные данные (ищутся в папке где находится скрипт автоматически)
1_1.csv
2_1.csv
...
10_1.csv
back_1.csv
выходные данные
1_speed.csv
1_coord.csv
2_speed.csv
2_coord.csv
...
back_speed.csv
back_coord.csv
'''
fast_list = [f"{i}_1.csv" for i in range(1, 11)]
fast_list.append('back_1.csv')
if sys.argv[-1] == 'fast':
    for file in fast_list:
        with open(file, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=';')
            arr = [row for row in data]
        correct_speed(arr)
        notcsv = open(f'{file.split("1.")[0]}speed.csv', 'w', newline='')
        coord_csv = open(f'{file.split("1.")[0]}coord.csv', 'w', newline='')
        stamp = date_to_seconds(arr[0][1])
        for r in arr:
            wr = csv.writer(notcsv, delimiter=';')
            wr2 = csv.writer(coord_csv, delimiter=';')
            wr.writerow([r[0], r[1]])
            wr2.writerow([r[2], r[1]])
            
        notcsv.close()
        coord_csv.close()

else:       
    for i in range(1, len(sys.argv)):
        with open(sys.argv[i], newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=';')
            arr = [row for row in data]
        correct_speed(arr)
        m = max(round(float(r[0]),2) for r in arr)
        notcsv = open(f'{sys.argv[i].split("1.")[0]}speed.csv', 'w', newline='')
        coord_csv = open(f'{sys.argv[i].split("1.")[0]}coord.csv', 'w', newline='')
        stamp = date_to_seconds(arr[0][1])
        for r in arr:
            wr = csv.writer(notcsv, delimiter=';')
            wr2 = csv.writer(coord_csv, delimiter=';')
            #wr.writerow([r[0], date_to_seconds(r[1]) - stamp])
            #wr2.writerow([r[2], date_to_seconds(r[1]) - stamp])
            wr.writerow([r[0], r[1]])
            wr2.writerow([r[2], r[1]])
            
        notcsv.close()
        coord_csv.close()
'''Если скрипт запускается как
python3 Correct_speed 1_1.csv 2_1.csv 3_1.csv ... 
то работает эта часть
результат - создание файлов с пересчитанными импульсами в скорость для каждого переданного файла
то есть при наличии в папке
1_1.csv
2_1.csv
3_1.csv
создадутся
1_speed.csv
файл содержит в себе осцилограммы скорости на первом проходе
1_coord.csv
файл содержит в себе координату телеги от времени на первом проходе
2_speed.csv
2_coord.csv
3_speed.csv
3_coord.csv
и т д


'''         
