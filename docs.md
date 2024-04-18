# Подробная документация

## tare_weight.py

### Назначение

Служит для перевода таблицы измерений тензодатчика вида:

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/679c1394-ad00-4ae5-9f25-ee70cbdf8cdd)

*26 это значение температуры - по умолчанию arduino uno выдаёт её значение какое-то количество раз перед тем как выдавать показания тензодатчика*

В таблицу сила в граммах от времени: 

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/3b5c0eb3-ebe6-4262-94cd-fe74a7809b61)

*В результате работы скрипта температура заменяется 0-ми, так как её значения малы по сравнению со значениями силы полученной с тензодатчика*

### Режимы работы

#### Fast

`python3 tare_weight.py fast `

применяет скрипт к файлам 1_0.csv, 2_0.csv ... 10_0.csv, back_0.csv 

результат: 1_0_tare.csv, 2_0_tare.csv, ..., 10_0_tare.csv, backk_0_tare.csv

#### Classic

`python3 tare_weight.py name1_0.csv name2_0.csv ... `

применяет скрипт к каждому файлу чьё название переданно на вход

результат: name1_0_tare.csv name2_0_tare.csv ...

*Файлы создаются в директории где находится скрипт автоматически*

### Коэффициенты тарировки

Требует наличия файла approx_rate.csv

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/02732e90-c98b-4a6a-a065-fbfc4d7f42db)

Содержащего коэффициенты k;b (смотрите раздел тарировка)

## Correct_speed.py

### Назначение

Служит для построения по измерениям скоростемера таблицы мгновенной скорости от времени и координаты от времени

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/8ae0350e-f0ac-40a6-b470-28b3a7829f1e)

Показания скоростемера 1_1.csv

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/bd68abb3-d5cf-4676-8e48-17b750a40ed8)

Скорость от времени 1_speed.csv

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/de6c64d4-2563-487f-bddb-62b4adb88116)

Координата от времени 1_coord.csv

### Режимы работы

#### Fast

`python3 Correct_speed.py fast`

Аналогичен режиму fast датчика силы, применяется к 1_1.csv, 2_1.csv ... 10_1.csv, back_1.csv 

Результат: 

1_speed.csv, 2_speed.csv ... 10_speed.csv, back_speed.csv 

1_coord.csv, 2_coord.csv ... 10_coord.csv, back_coord.csv 
