import serial
import csv
import time
import datetime
import sys
import keyboard
from threading import Thread

BAUDR = 115200
system = 'Linux'
port_prefixs = {'Linux': '/dev/tty/ACM', 'Windows': 'COM'}
post_prefix = post_prefixs[system]

'''
Инструкция для использования

python3 Read_ser.py 1 0 10
Начнётся считвание
далее при нажатии клавиши x(икс)
считывание прекращается и создаются два файла в директории
результат работы скрипта
10_1.csv, 10_0.csv


какой порт отвечает за какой датчик определяется при подключении и можно посмотреть в arduino IDE
В ней есть меню порты где указано например
arduino leonardo(скоростемер) /dev/tty/ACM0
arduino uno(датчик силы) /dev/tty/ACM1


'''
class com:
    '''Класс отвечает за создание и работу портов'''
    def __init__(self, port, baud, num_of_experiment):
        '''
        name: str - название создаваемого csv файла
        пример: name = 10, port = 0, название файла 10_0.csv
        Указывается при запуске скрипта из командной строки
        
        '''
        self.port = port
        self.baud = baud
        # Для работы на Linux и Raspberry pi поменять COM на /dev/tty/ACM{}
        self.ser = serial.Serial(f'{post_prefix}{self.port}', baudrate=baud)
        self.res = []
        self.num_of_experiment = num_of_experiment

    
    def read_port(self):
        '''
        метод для считывания данных из порта self.port указанного при инициализации обьекта.
        '''
        self.ser.flush()
        while True:
            try:
                if keyboard.is_pressed("x"):
                    break
            except:
                break
            # readline отвечает за считывание строки из порта
            string = self.ser.readline()
            # если какое-то исключение повторить декодировку
            try:
                newrow = string.decode('utf-8').rstrip().split(";")
            except:
                newrow = string.decode('utf-8').rstrip().split(";")
            newrow.append(datetime.datetime.now())
            # вывод данных в консоь
            print(newrow)

            # добавление строки к результирующей таблице
            self.res.append(newrow)
            
            

    def toCsv(self):
        '''
        метод отвечает за запись считанных данных в csv 
        '''
        with open(f'{self.name}_{self.port}.csv', 'w', newline='') as csvfile:
            testwriter = csv.writer(csvfile, delimiter=';')
            for d in self.res:
                testwriter.writerow(d)

    def write_at_port(self, string):
        '''
        метод был предназначен для регуляции частоты считывания, но в последнем варианте не используется
        посылает сигнал датчику чтобы он начал работу
        сейчас не обязателен
        '''
        self.ser.write(str(string).encode())

def correct_speed(res):
    for r in res:
        r[3] = int(r[3]) * 0.009375


num_of_experiment = sys.argv[-1]
ports_num = sys.argv[1:-1]

# создание обьектов класса порт, с заданным BAUDRATE, названием файла sys.argv[-1] и названием портов sys.argv[i]
coms = [com(i, BAUDR, num_of_experiment) for i in ports_num]

# создание потоков с командой считывания для каждого порта
threads = [Thread(target=coms[i].read_port, args=()) for i in range(len(coms))]

# запуск каждого потока
for t in threads:
    t.start()
time.sleep(2)

# не обязательно
for c in coms:    
    c.write_at_port(sys.argv[-1])
#

# присоединение потоков к main
for t in threads:
    t.join()

# не обязательно    
for c in coms:    
    c.write_at_port(0)
#
#correct_speed(coms[-1].res)

# Запись в файлы данных с каждого созданного порта
for c in coms:    
    c.toCsv()

'''
Код предназначенный для считывания данных с портов и записи в csv файлы
'''
