import csv
import sys

laser_stern = '26193'
laser_nose = '26194'

def data_from_csv(csvfile):
    '''
    считывает таблицу из csv файла в двумерный массив
    '''
    with open(csvfile, newline='') as csvfile:
        rd = csv.reader(csvfile, delimiter=';')
        data = []
        for row in rd:
            if not any(map(lambda x: x.isalpha(), row[0])):
                data.append(row)
        return data
        
def arr_to_csv(arr, csvfile):
    '''
    Записывает таблицу в csv меняя местами 0 и 1 столбец
    так чтобы первыми в таблице были показания лазера
    вторыми время
    третьими успешность записи (1 если успешно)
    четвертыми номер лазера
    '''
    with open(csvfile, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=';')
        for row in arr:
            wr.writerow([row[1], row[0], row[2], row[3]])

# в случае использования с python3 conv.py
'''
если принимает значение fast, то применяется к файлам
1.csv
2.csv
...
10.csv
back.csv
Разделяет показания лазеров для того, чтобы с ними нормально работать
Результат
1_26194.csv
1_26193.csv
...

Файлы с разделенными показаниями лазеров
26193 корма
26194 нос
'''
fast_list = [f"{i}.csv" for i in range(1, 11)]
fast_list.append('back.csv')

if sys.argv[-1] == 'fast':
    for file in fast_list:
        devices = {laser_nose:[], laser_stern:[]}     
        table = data_from_csv(file)

        for row in table:
            if row[-2] == '1':
                devices[row[-1]].append(row)
            
            
        arr_to_csv(devices[laser_nose], f"{file.split('.')[0]}_{laser_nose}.csv")
        arr_to_csv(devices[laser_stern], f"{file.split('.')[0]}_{laser_stern}.csv")
# иначе принимает на вход python3 laser_div.py 1.csv 2.csv ....
# и для каждого поданого файла создает разделенные
else:    
    for i in range(1, len(sys.argv)):
        devices = {laser_nose:[], laser_stern:[]}     
        table = data_from_csv(sys.argv[i])

        for row in table:
            if row[-2] == '1':
                devices[row[-1]].append(row)
            
            
        arr_to_csv(devices[laser_nose], f"{sys.argv[i].split('.')[0]}_{laser_nose}.csv")
        arr_to_csv(devices[laser_stern], f"{sys.argv[i].split('.')[0]}_{laser_stern}.csv")
