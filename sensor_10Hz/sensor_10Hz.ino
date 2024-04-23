volatile long IRQcount = 0;

//Bounce debounce_relay;
#define SERIAL_SPEED 115200

#define DELAY_CYCLES(n) __builtin_avr_delay_cycles(n)
#define CYCLES 256000*6 /*256000 - 62.5Hz*/
const int xPin = A7;    // pin that the sensor is attached to
const int ledPin = 13;
const int pulse_in = 7;
const int relay_in = 5;

int freq = 0;

String semicolon = ";";
int got;

void setup()
{
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  pinMode(pulse_in, INPUT);
  pinMode(relay_in, INPUT_PULLUP);
  
  delay(100);

  Serial.begin(SERIAL_SPEED);

  digitalWrite(ledPin, LOW);
  attachInterrupt(digitalPinToInterrupt(pulse_in), IRQcounter, RISING);
}

void IRQcounter() {
  IRQcount++;
}

void loop()
{   
  DELAY_CYCLES(CYCLES);
  //------------------------------------------------------------------
  cli();//disable interrupts
  freq = IRQcount;
  IRQcount = 0;
  sei();//enable interrupts  
  //------------------------------------------------------------------
  Serial.println(freq);
}
