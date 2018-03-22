#include <SoftwareSerial.h>

SoftwareSerial ss(12, 13);

char c;

void setup()
{
  Serial.begin(115200);
  Serial.println("HELLO");
  ss.begin(9600);
}

void loop()
{
  ss.listen();

  while (ss.available()) {
    c = ss.read();
    Serial.write(c);
  }
  while (Serial.available()) {
    c = Serial.read();
    ss.write(c);
  }
  delay(500);
}
