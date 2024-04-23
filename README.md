# Что нужно знать для проведения испытаний буксировочного сопротивления

## Для начала

Скачайте все файлы к себе на компьютер

в директории со всеми файлами запустите команду

`pip install -r requirements.txt`

> [!NOTE]
> Может понадобиться sudo

## Считывание данных

### с датчиков силы и скорости

`python3 Read_ser.py 0 1 num`

0 - датчик силы, 1 - Датчик скорости, num - это номер эксперимента

Для остановки и сохранения значений в файл нажать "x"

### с лазерных дальномеров

Запускаем приложение udpserv на распбери пи

Для остановки и сохранения в файл зажать "Ctrl + C"

## Предобработка данных

### с датчиков силы и скорости

1_0.csv, 1_1.csv, 2_0.csv, 2_1.csv ... 10_0.csv, 10_1.csv, back_0.csv, back_1.csv

back - проход назад на минимальной скорости, данные 10 проходов должны иметь названия указанные выше

### с дальномеров

По умолчанию они называются как дата_время.csv, нужно их переименовать в соответствии с номерами экспериментов и получить

1.csv, 2.csv, ..., 10.csv, back.csv

## Тарировка 

### Датчик силы

#### серия взвешиваний гирь

- Датчик силы закрепляется горизонтально
- определяется вес m которй будет закреплен к датчику, в начале 0
- `python3 Read_ser.py 0 m` (нажать x чтобы остановить)
- Получаем файл m_0.csv, где m это масса
- Берем следующий вес с некоторым шагом m = m + шаг
- Повторяем пока не пройдём до максимально допустимого веса для датчика(например 1кг)

#### тарировочная прямая
результатам серии является несколько файлов

0_0.csv, 50_0.csv, 120_0.csv ... 1010_0.csv

В этих файлах вычисляется среднее значение 'сырой нагрузки' и ставится в соответствие к нагрузке указанной в названии файла

Получается n точек, где n число экспериментов в серии, и строится прямая апроксимирующая наши точки наилучшим с точки зрения среднеквадратичного отклонения или другой метрики значением

Имеем прямую вида y = kx + b, где за x возьмем 'истинные' значения, а y это сырые. Выразим истинные значения через сырые и получим

tar = (raw - b) / k

raw - данные с датчика, tar - данные с гирь

где k,b необходимые тарировочные коэффициенты

#### approx_rate.csv
в папке должен находиться файл который содержит в себе тарировочные коэффициенты и называется approx_rate.csv

approx_rate.csv выглядит так 

k;b

Далее он считывается программой которая для каждого файла с данными датчика силы переводит их в граммы

### Датчик скорости

#### Пересчёт данных

Немножко поговорим об устройстве - датчик скорости имеет wheel_pins = 3600 зубчиков равномерно расположенных в соответствие длины колеса wheel_length = 0.25132741 м

при прокрутке длины соотвествующей одному зубчику x_scale = wheel_length/wheel_pins посылается один импульс. Программа считывает число этих импульсов за промежуток времени time_del.

Далее число импульсов умножается на x_scale и делится на time_del 

Результатом является длина пройденная колесом за промежуток времени - что по определению и есть скорость колеса равно и скорость телеги(колесо толкается телегой и движется как её часть)

wheel_pins и wheel_length можно поменять в файле Correct_speed.py

### Лазерные дальномеры 

#### Уже в милиметрах

## Обработка данных

### Необходимые условия 

Если в директории есть 

файы с данными с именами

у лазеров 1.csv 2.csv ... 10.csv back.csv

у скоростемера 1_1.csv 2_1.csv ... 10_1.csv back_1.csv

у датчика силы 1_0.csv 2_0.csv ... 10_0.csv back_0.csv

### Запуск

`python3 conv.py `

### результаты

1_res_rel.csv, 2_res_rel.csv ... 10_res_rel.csv

Это сводные таблицы содержащие показания всех датчиков в каждом эксперименте синхронизированные по времени

показания лазеров в них строится относительно показаний лазеров при проходе модели корабля на небольшой скорости

### Время выполнения

для серии экспериментов может быть в районе 20-30 минут

# [Подробная документация](docs.md)













