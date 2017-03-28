
#include <SoftwareSerial.h>

SoftwareSerial mySerial(11, 10); // RX, TX

int LED = 13;


void setup(){
  pinMode(LED, OUTPUT);
  Serial.begin(9600); //gyro

  mySerial.begin(9600); //BT
  mySerial.println("Hello, world?");

}

void loop(){
  if (mySerial.available()) {
    Serial.write(mySerial.read());
  }
  if (Serial.available()) {
    mySerial.write(Serial.read());
  }
}

