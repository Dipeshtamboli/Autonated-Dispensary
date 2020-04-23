#include <SoftwareSerial.h>
#include <Servo.h>

const int stepPin1 = 10;
const int dirPin1 = 11;
const int stepPin2 = 2;
const int dirPin2 = 3;
const int stepTime = 12;

SoftwareSerial BT(A5, A4); //RX, TX from Arduino POV

Servo servo;
const int initPos = 0;
const int pickUpPos = 170;

void getInput();
void moveMotors(char);
void pick();

void setup() {  
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);

  servo.attach(9);
  servo.write(initPos);

  Serial.begin(9600);
  BT.begin(9600);
}

void loop() {
  getInput();
  while(Serial.available() == 0);
  char inChar = '\0';
  while(inChar != 'x') {
    inChar = (char)Serial.read();
    moveMotors(inChar);
  }
}

void getInput() {
  String inString = "";
  while(inString == "") {
    while(BT.available()) {
      inString += (char)BT.read();
  //    Serial.println("Just after receiving input: "+ inString);
      delay(50);
    }
    if(inString != "") {
      Serial.print(inString);
    }
  }
}

void moveMotors(char inChar) {
  if(inChar == 'r') {
    digitalWrite(dirPin1, HIGH);
    digitalWrite(stepPin1, HIGH);
    delay(stepTime);
    digitalWrite(stepPin1, LOW);
    delay(stepTime);
  }
  if(inChar == 'l') {
    digitalWrite(dirPin1, LOW);
    digitalWrite(stepPin1, HIGH);
    delay(stepTime);
    digitalWrite(stepPin1, LOW);
    delay(stepTime);
  }
  if(inChar == 'u') {
    digitalWrite(dirPin2, HIGH);
    digitalWrite(stepPin2, HIGH);
    delay(stepTime);
    digitalWrite(stepPin2, LOW);
    delay(stepTime);
  }
  if(inChar == 'd') {
    digitalWrite(dirPin2, LOW);
    digitalWrite(stepPin2, HIGH);
    delay(stepTime);
    digitalWrite(stepPin2, LOW);
    delay(stepTime);
  }
  if(inChar == 'p') {
    pick();
  }
  if(inChar == 'x') {
    drop();
  }
  Serial.print('k');
}
void pick() {
  servo.write(pickUpPos);
  delay(1000);
}

void drop() {
  servo.write(initPos);
  delay(1000);
}
