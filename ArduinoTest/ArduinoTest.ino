int motor1=4;
int motor2=5;
int resolution=100;  //This is what one pixel in the image corresponds to for the motor 
import <Stepper.h>  //fix code later 
void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  pinMode(motor1,OUTPUT);
  pinMode(motor2,OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    if(Serial.read()==int('l')){
      analogWrite(motor1,resolution);
    }
    else{
      
      analogWrite(motor2,resolution);
    }
    Serial.print("d")
  }
}
