import subprocess

# Здесь вы можете указать путь к скрипту, который вы хотите вызвать
tare_weight = "tare_weight.py"
correct_speed = "Correct_speed.py"
laser_div = "laser_div.py"
interpolate = "interpolate.py"
inversie_csv = "inversie_csv.py"
relate_laser = "relate_laser.py"
# Вызываем скрипт с помощью subprocess
try:
    subprocess.run(["python3", tare_weight, "fast"], check=True)
    subprocess.run(["python3", correct_speed, "fast"], check=True)
    subprocess.run(["python3", laser_div, "fast"], check=True)
    subprocess.run(["python3", interpolate, '1', '10'], check=True)
    subprocess.run(["python3", interpolate, "back.csv"], check=True)
    subprocess.run(["python3", inversie_csv, "back_res.csv"], check=True)
    subprocess.run(["python3", relate_laser, "back_res_inv.csv", '1', '10'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Ошибка: {e}")

'''
Для использования поместить в папку где находятся все скрипты указанные в конвое
Так же должны находиться данные проходов в формате
10_0.csv
10_1.csv
9_0.csv
9_1.csv
...
1_0.csv
1_1.csv
а так же
back_0.csv
back_1.csv проход назад медленный
где первое число - номер эксперимента
второе номер датчика(0 - датчик силы, 1 - датчик скорости)
Для запуска написать
python3 conv.py
'''
