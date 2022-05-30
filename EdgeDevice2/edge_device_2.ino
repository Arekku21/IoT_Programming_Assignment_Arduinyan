#include <GP2Y0A02YK0F.h>

//Distance Sensor Variables
GP2Y0A02YK0F irSensor;
int distance;

int LED_alarm = 12;
int buzzer = 13;

//Push button Variables
int LED_switch = 2;
int push_button = 4;

int button_state = 0;

String toggle_switch;

void setup()
{
  pinMode(LED_alarm, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(LED_switch, OUTPUT);
  pinMode(push_button, INPUT);
  
  Serial.begin(9600);
  irSensor.begin(A0);  
}

void loop()
{
  //When RPC request from dashboard comes in, toggle the switch state.
  toggle_switch = Serial.readString();
   
  if(toggle_switch == "Toggle" && button_state == 0){ 
    digitalWrite(LED_switch, HIGH);
    button_state = 1;
  }else if (toggle_switch == "Toggle" && button_state == 1){
    digitalWrite(LED_switch, LOW);
    button_state = 0;
  }
  
  //When psuh button is pressed, toggle the switch state.
  if(digitalRead(push_button) == 1 && button_state == 0){
      digitalWrite(LED_switch, HIGH);
      button_state = 1;
  } 
  else if (digitalRead(push_button) == 1 && button_state == 1) {
      digitalWrite(LED_switch, LOW);
      button_state = 0;
  }
  
  if(digitalRead(LED_switch) == HIGH){
      distance = irSensor.getDistanceCentimeter();
      Serial.print("On ");
      Serial.print(distance);
      if(distance <= 30){
        Serial.print(" On ");
        Alarm_Working();
      } else {
        Serial.print(" Off ");
        digitalWrite(LED_alarm, LOW);
        digitalWrite(buzzer, LOW);
      }
      Serial.println();
         
  } else if (digitalRead(LED_switch) == LOW){
      digitalWrite(LED_alarm, LOW);
      digitalWrite(buzzer, LOW);
      Serial.println("Off 0 Off ");
  }
  
  delay(1000);
}

void Alarm_Working(){
    digitalWrite(LED_alarm, LOW);
    digitalWrite(buzzer, LOW);
    delay(100);
    digitalWrite(LED_alarm, HIGH);
    digitalWrite(buzzer, HIGH);
    delay(300);
    digitalWrite(LED_alarm, LOW);
    digitalWrite(buzzer, LOW);
    delay(100);
}
