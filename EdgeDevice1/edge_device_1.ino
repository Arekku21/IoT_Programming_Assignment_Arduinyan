#include <SharpIR.h>
#include <Servo.h>


Servo myservo;

SharpIR sensor( SharpIR::GP2Y0A41SK0F, A0 );

int servo = 4;               
int led_red = 13;
int led_yellow = 12;
int Button = 9;            
String Door;


void setup() {
  pinMode(servo, OUTPUT);
  pinMode(led_red, OUTPUT);
  pinMode(led_yellow, OUTPUT);
  pinMode(Button, INPUT);
  myservo.attach(servo);   
  myservo.write(0);
  Serial.begin (9600);
  
}
void loop() {

  int distance = sensor.getDistance();
  delay(1000); // slow down serial port 
  Door = Serial.readStringUntil('\n');
  
  if (distance < 10){
    digitalWrite(led_yellow, HIGH);
    digitalWrite(led_red, LOW);
    myservo.write(20);
    Serial.print(distance);
    Serial.print(" Detected ");
    Serial.print("Open ");
    Serial.println();
    delay(2000);
  }else if(digitalRead(Button)==HIGH){
    digitalWrite(led_yellow, HIGH);
    digitalWrite(led_red, LOW);
    myservo.write(20);
    Serial.print("0");
    Serial.print(" Button ");
    Serial.print("Open ");
    Serial.println();
    
    delay(2000);
  }else if(Door == "Open"){
    digitalWrite(led_yellow, HIGH);
    digitalWrite(led_red, LOW);
    myservo.write(20);
    Serial.print("0");
    Serial.print(" Online ");
    Serial.print("Open ");
    Serial.println();
    delay(2000);
  }else{
    digitalWrite(led_yellow, LOW);
    digitalWrite(led_red, HIGH);
    myservo.write(100);
    Serial.print(distance);
    Serial.print(" Nothing ");
    Serial.print("Close ");
    Serial.println();
  
  }
}
