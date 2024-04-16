import time
import datetime
import csv
import sys


class Measure:
    '''
    Класс для измерений, в нём реализован полиморфизм для того, чтобы можно было интерполировать данные по координате с помощью операции сложения
    '''
    def __init__(self, data, data_col=0, time_col=-1):
        '''
        Для инициализации подаются данные, номер колонки с данными и номер колонки со временем - для интерполяции
        '''
        self.time_col = time_col
        self.data = data
        self.data_col = data_col
        
    def update_data(self):
        '''
        переводит время в секунды, а данные в числовой тип
        '''
        for row in self.data:
            row[self.time_col] = date_to_seconds(row[self.time_col])
        self.data = data_to_float(self.data)
        return self
            
    def __add__(self, other):
        '''
        Функция реализующая полиморфизм обьединяет показания правой таблицы(other) с левой, подстраиваясь под время левой таблицы
        то есть для правой таблицы все значения линейно пересчитываются под временные значения левой
        пример
        слева
        данные время
        1      0
        2      1
        3      2
        справа
        данные
        4      -1
        8       1
        12      3
        результат
        данные1 данные2 время
        1       6        0
        2       8        1
        3       10       2
        
        '''
        extand = []
        for i in range(len(self.data) - 1):
            j = 0
            while j < len(other.data) and other.data[j][other.time_col] < self.data[i][self.time_col]:
                j += 1
            if j < len(other.data) and j >= 0:
                interpolate_data = other[j - 1][other.data_col] + (other[j][other.data_col] - other[j - 1][other.data_col]) * (self[i][self.time_col] -
                other[j - 1][other.time_col]) / (other[j][other.time_col] - other[j - 1][other.time_col])
                row = [col for col in self.data[i]]
                row.pop(self.time_col)
                row.append(interpolate_data)
                row.append(self[i][self.time_col])
                extand.append(row)
        return Measure(extand, 0, -1)
    
    
        
    def __getitem__(self, item):
        '''
        при обращении self[0] возвращает self.data[0]
        '''
        return self.data[item]
    def __len__(self):
        '''
        при обращении len(table) возвращает len(table.data)
        '''
        return len(self.data)
    def to_date(self):
        '''
        переводит временнную колонку из секунд в дату
        '''
        for row in self.data:
            row[self.time_col] = seconds_to_date(row[self.time_col])
        return self

def data_from_csv(csvfile):
    '''
    функция для чтения данных из csv; в двумерный масив
    так же функция пропускает все не числовые строки и читает только числа
    '''
    with open(csvfile, newline='') as csvfile:
        rd = csv.reader(csvfile, delimiter=';')
        data = []
        for row in rd:
            if not any(map(lambda x: x.isalpha(), row[0])):
                data.append(row)
        return data
        
def data_to_float(data):
    '''
    переводит таблицу в числовой тип данныъ
    '''
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return data
    
def date_to_seconds(date):
    #Переводит локальное время в секунды 
    try:
        t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        t = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    t = (t-datetime.datetime(1970,1,1)).total_seconds()
    return t
    
def seconds_to_date(seconds):
    #Переводит секунды в локальное время( МСК +3 UTC )
    utc_epoch = 3 * 3600
    seconds -= utc_epoch
    return datetime.datetime.fromtimestamp(seconds).strftime("%Y-%m-%d %H:%M:%S.%f")
def Measure_from_csv(filename, data_col=0, time_col=1):
    '''
    Создает обьект класса измерений на основе файла и переводит время в секунды и значения в числа
    '''
    data = data_from_csv(filename)
    return Measure(data, data_col, time_col).update_data()

"""   
data = data_from_csv("3.csv")    
with open('tenzo.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile, delimiter=';')
    for i in data:
        wr.writerow([i[0], date_to_seconds(i[1])])
        
with open('speedo.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile, delimiter=';')
    for i in data:
        wr.writerow([float(i[0]) * 0.001, date_to_seconds(i[1]) + 0.3])
"""
     
     
"""name = input("Введите название файла с измерениями тензодатчика")
while name != 'stop':
    d = int(input("Введите номер колонки с данными (нумерация с нуля)"))
    t = int(input("Введите номер колонки с временем (нумерация с нуля)"))
    a.append(Measure_from_csv(name, d, t))
    name = input("Введите название ещё одного файла с измерениями датчика (stop для остановки)")
  """  


def create_res(num_of_ex):
    '''
    на вход получает номер эксперимента
    выдает сводную таблицу интерполированную ко времени измерения координат
    то есть результирующий файл

    coord корма нос скорость сила время

    при входе
    1
    и наличии в директории
    1_coord.csv
    1_26193.csv
    1_26194.csv
    1_speed.csv
    1_0_tare.csv
    результатом будет
    1_res.csv
    '''
    a = [] #массив измерений 
    a.append(Measure_from_csv(f'{num_of_ex}_coord.csv'))
    a.append(Measure_from_csv(f'{num_of_ex}_26193.csv'))
    a.append(Measure_from_csv(f'{num_of_ex}_26194.csv'))
    a.append(Measure_from_csv(f'{num_of_ex}_speed.csv'))
    a.append(Measure_from_csv(f'{num_of_ex}_0_tare.csv'))
    extand = a[0]
    for i in range(1, len(a)):
        extand = extand + a[i]

    with open(f'{num_of_ex}_res.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, delimiter=';')
        extand.to_date()
        try:
            stamp = date_to_seconds(extand[0][extand.time_col])
        except IndexError:
            print(extand.data)
        for row in extand:
            row[extand.time_col] = date_to_seconds(row[extand.time_col]) - stamp
            wr.writerow([col for col in row])

            
# при python3 interpolate back.csv создает результирующий файл для прохода назад
if sys.argv[1] == 'back.csv':
    create_res('back')
# при python3 interpolate a b
# где a, b целые числа - создает результирующие файлы экспериментов от a до b
# например python3 interpolate 1 10 создаст 1_res.csv 2_res.csv ... 10_res.csv
else:
    for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        create_res(i)
