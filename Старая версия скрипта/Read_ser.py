import serial
import csv
import time
import datetime
import sys
import keyboard
from threading import Thread
N = 15000
BAUDR = 115200

class com:
    def __init__(self, port, baud, name):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(f'/dev/ttyACM{self.port}', baudrate=baud)
        self.res = []
        self.name = name
        
    def read_port(self):
        self.ser.flush()
        while True:
            try:
                if keyboard.is_pressed("x"):
                    break
            except:
                break
            #time.sleep(1/self.hz)
            string = self.ser.readline()
            try:
                newrow = string.decode('utf-8').rstrip().split(";")
            except:
                newrow = string.decode('utf-8').rstrip().split(";")
            newrow.append(datetime.datetime.now())
            print(newrow)
            self.res.append(newrow)
            
            

    def toCsv(self):
        with open(f'{self.name}_{self.port}.csv', 'w', newline='') as csvfile:
            testwriter = csv.writer(csvfile, delimiter=';')
            for d in self.res:
                testwriter.writerow(d)
    def write_at_port(self, string):
        self.ser.write(str(string).encode())

def correct_speed(res):
    for r in res:
        r[3] = int(r[3]) * 0.009375

            
coms = [com(int(sys.argv[i]), BAUDR, sys.argv[-1]) for i in range(1, len(sys.argv) - 1)]

threads = [Thread(target=coms[i].read_port, args=()) for i in range(len(coms))]


for t in threads:
    t.start()
time.sleep(2)

for t in threads:
    t.join()
    

#correct_speed(coms[-1].res)
for c in coms:    
    c.toCsv()
