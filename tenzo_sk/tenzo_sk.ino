#include <GyverHX711.h>
GyverHX711 sensor(A1, A0, HX_GAIN128_A);
// HX_GAIN128_A - канал А усиление 128
// HX_GAIN32_B - канал B усиление 32
// HX_GAIN64_A - канал А усиление 64
#include "DHT.h"
#define DHTPIN 2 // Тот самый номер пина, о котором упоминалось выше
// Одна из следующих строк закоментирована. Снимите комментарий, если подключаете датчик DHT11 к arduino
DHT dht(DHTPIN, DHT11); //Инициация датчика
String semicolon = ";";
int counter = 0;
void setup() {
  Serial.begin(115200);
  dht.begin();
  // если тарирование при первом запуске -
  // нужно выждать готовность датчика
  delay(5000);
}

void loop() {
  if (counter < 50) {
    counter++;
    Serial.println(dht.readTemperature());
  }
  // чтение только по доступности! if available
  else if (sensor.available()) {
    Serial.println(sensor.read()); 
  }
}
