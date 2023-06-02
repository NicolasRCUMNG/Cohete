#include <Servo.h>

Servo servoMotor;
int SENSOR=2;

//int LED=3;
int ESTADO;
void setup(){
  
  Serial.begin(9600);
  servoMotor.attach(9);
  pinMode(SENSOR,INPUT);
}

void loop(){

  
  ESTADO=digitalRead(SENSOR);
  
  if (ESTADO==LOW)
  delay(1000);
  else 
  {
    //servoMotor.write(90);
    //delay(100);
    servoMotor.write(0);
    delay(500);
    servoMotor.write(90);
    delay(500);
    exit(0);
  }
  
}
