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

**ВАЖНО при экспериментах на телеге стартовать с одного места**

### Режимы работы

#### Fast

`python3 Correct_speed.py fast`

Аналогичен режиму fast датчика силы, применяется к 1_1.csv, 2_1.csv ... 10_1.csv, back_1.csv 

Результат: 

1_speed.csv, 2_speed.csv ... 10_speed.csv, back_speed.csv 

1_coord.csv, 2_coord.csv ... 10_coord.csv, back_coord.csv 

#### Classic

`python3 Correct_speed.py name1_1.csv name2_1.csv ...`

Применяет Correct_speed.py к каждому переданному файлу

### При изменении аппаратуры

При смене датчика/колеса код нужно изменить. https://github.com/MagicKisa/HydroChannel/blob/master/Correct_speed.py 

Переходим в файл Correct_speed.py и меняем константы указанные на скриншоте

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/1782ec5a-1557-4e10-9d48-7d4b03fd1901)

wheel_pins - число зубчиков в шт

wheel_length - длина колеса в метрах

**Больше ничего менять не нужно**

## laser_div.py

### Назначение

Служит для разделения файла name.csv содержащего показания лазерных дальномеров 

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/8f3021a9-42a5-4b5f-aedf-12d3559c99b4)

на два файла name_26193.csv, name_26194.csv каждый из которых содержит показания своего дальномера

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/5930fef9-160b-42ed-af98-6952e3e378f3) ![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/fdbfb07e-5c56-4666-9ada-8e371fdf7681)

26193, 26194 - номера дальномеров riftek определяются на заводе изготовителе и указываются при записи в файл с помощью `udpserv`

### Режимы работы

#### Fast

`python3 laser_div.py fast`

Применяется к 1.csv, 2.csv ... 10.csv, back.csv 

Результат: 

1_26193.csv, 2_26193.csv ... 10_26193.csv, back_26193.csv 

1_26194.csv, 2_26194.csv ... 10_26194.csv, back_26194.csv 

#### Classic

`python3 laser_div.py name1.csv name2.csv ...`

Применяет laser_div.py к каждому переданному файлу

Результат:

name1_26193.csv, name2_26193.csv...

name1_26194.csv, name2_26194.csv

### При смене номеров лазеров 

Нужно заменить в коде '26194' -> номер нового лазера на носу корабля laser_nose

'26193' -> номер нового лазера на корме корабля laser_stern

## interpolate.py

### Назначение

Служит для синхронизации данных скорости, силы, координаты и лазерных дальномеров за один эксперимент в одном файле.

При этом проблема синхронизации решается с помощью линейной интерполяции данных

При вызове

`python3 interpolate.py 1 1`

Результат:

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/2c656963-b64b-4604-ba0f-4816928e335d) 

Столбцы слева-направо 

координаты(м относительно точки старта)-лазеркорма(мм)-лазернос(мм)-скорость(м/с)-сила(граммы)-время(в секундах с начала эксперимента)

### Режимы работы

#### back

При получении на вход back.csv

`python3 interpolate.py back.csv`

Сводит в одну таблицу показания датчиков при проходе назад

#### Интервал

При задании номера первого эксперимента и последнего

`python3 interpolate.py 1 10`

Для каждого эксперимента из этого интервала сводит в таблицу файлы измерений

### Требования

Время в каждом файле должно быть записано в последней колонке в фомате "%Y-%m-%d %H:%M:%S.%f"

Данные которые нужны для финальной таблицы должны находиться в первой колонке(нулевой, если подсчёт вести с нуля)

Во всех csv файлах разделителем является точка с запятой

## inversie_csv.py

### Назначение

Этот скрипт предназначен для того, чтобы из координат и времени обратного прохода получить координаты и время как в прямом.

**Небольшое пояснение**: Все эксперименты проводятся в одну сторону, кроме последнего - back. На этом проходе координата x соответствует конец_прохода - x в других экспериментах.

Аналогично и со временем.

### Применение

`python3 inversie_csv.py back_res.csv`

Результат:

back_res_inv.csv

Этот скрипт можно применить к любому файлу, но в условиях данной задачи он применяется к back_res.csv

### Скриншоты

Начало и конец back_res.csv

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/9bc8b91d-d834-4934-84fc-69e495be443e)

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/abaf0097-8d53-4a7f-8521-7930c6f24c60)

Начало и конец back_res_inv.csv

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/218f63e6-755f-4125-8e70-a1db5fa950f9)

![image](https://github.com/MagicKisa/HydroChannel/assets/105859497/9861bd27-dce3-4360-91f3-c55980afe31e)





