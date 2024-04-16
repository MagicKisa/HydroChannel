import time
import datetime
import csv
import sys

class Data:
    '''
    класс созданный для реализации полиморфизма и вычитания лазеров по координате
    '''
    def __init__(self, data, laser1=3, laser2=4, coord=0):
        '''
        на вход подаются данные и номера столбцов содержащие laser1 и laser2 в _res.csv, по умолчаниюю 3-4
        '''
        self.coord = coord
        self.laser1 = laser1
        self.laser2 = laser2 
        self.data = data
        
    def __sub__(self, other):
        '''
        Позволяет вычесть из столбца другой интерполируя по координате уменьшаемого
        пример:
        на одной скорости
        laser coord
        1      0
        2      1
        3      2
        на другой скорости
        laser coord
        2      -1
        4       1
        6       3
        Результат вычитания
        laser coord
        -2      0
        -2      1
        -2      2

        для вычисления относительного изменения расстояния от лазера до цели при разных скоростях
        Other - тот относительно кого считается
        
        '''
        extand = []
        for i in range(len(self.data) - 1):
            j = 0
            while j < len(other.data) and other.data[j][other.coord] < self.data[i][self.coord]:
                j += 1
            if j < len(other.data) and j > 0:
                self[i][self.laser1] -=  other[j - 1][other.laser1] + (other[j][other.laser1] - other[j - 1][other.laser1]) * (self[i][self.coord] -
                other[j - 1][other.coord]) / (other[j][other.coord] - other[j - 1][other.coord])
                self[i][self.laser2] -= other[j - 1][other.laser2] + (other[j][other.laser2] - other[j - 1][other.laser2]) * (self[i][self.coord] -
                other[j - 1][other.coord]) / (other[j][other.coord] - other[j - 1][other.coord])
        return self
    def __getitem__(self, item):
        return self.data[item]
    def __len__(self):
        return len(self.data)
        
def data_from_csv(csvfile):
    with open(csvfile, newline='') as csvfile:
        rd = csv.reader(csvfile, delimiter=';')
        data = []
        for row in rd:
            if not any(map(lambda x: x.isalpha(), row[0])):
                data.append(row)
        return data
def to_float(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return data
        

def relate_file(rel_file, *files):
    y = Data(to_float(data_from_csv(rel_file)), laser1=1, laser2=2)
    for file in files:
        x = Data(to_float(data_from_csv(file)), laser1=1, laser2=2)
        x = x - y

        with open(f'{file.split(".csv")[0]}_rel.csv', 'w', newline='') as csvfile:
            wr = csv.writer(csvfile, delimiter=';')
            for row in x:
                wr.writerow(row)

nums = (int(sys.argv[2]), int(sys.argv[3])) #номера экспериментов которые хотим отнести
rel = sys.argv[1] #показания к которым будем относить

fs = [f'{i}_res.csv' for i in range(nums[0], nums[1] + 1)]

relate_file(rel, *fs)
