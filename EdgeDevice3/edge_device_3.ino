#include <Servo.h>

//varibales for all the actuators and sensors
//serial communication from dashboard
unsigned int dashboardreply = 0;

//sensors
int PIR_sensor = 2;
byte Photo_sensor = A0;

//sensor read variables
int PIR_sensor_state = 0;
int Photo_sensor_value = 0;

//actuators
int Red_LED = 4;
int Yellow_LED = 8;
int Blue_LED = 13;
int Buzzer = 7;

//servo motor
int Servo_motor_port = 9;
Servo Servo_motor;

//servo motor led replacement
int Servo_Motor_replacement_led = 10;

void setup(){
    Serial.begin(9600);

    //setup the pinmodes
    //sensors
    pinMode(PIR_sensor,INPUT);
    pinMode(Photo_sensor,INPUT);

    //actuators
    pinMode(Red_LED,OUTPUT);
    pinMode(Yellow_LED,OUTPUT);
    pinMode(Blue_LED,OUTPUT);
    pinMode(Buzzer,OUTPUT);

    //SERVO MOTOR
    Servo_motor.attach(Servo_motor_port);
    Servo_motor.write(0);

    //servomotor led replacement
    pinMode(Servo_Motor_replacement_led,OUTPUT);

    //set the power status led to high
    digitalWrite(Red_LED,HIGH);
}

void loop(){
    
    //read the current values of the sensors
    PIR_sensor_state = digitalRead(PIR_sensor);
    Photo_sensor_value = analogRead(Photo_sensor);
    delay(1000);
    
    //write into serial for serail communication
    Serial.print(PIR_sensor_state);
    Serial.print("x");//delimiter for data extraction later
    Serial.print(map(Photo_sensor_value,0,1023,100,0));
    Serial.println();//delimiter for data extraction later

    //start the if conditions
    //serial available check if there is any messages in the FIFO serial
    if(Serial.available() > 0){
        //change the srial data to int for the if conditions
        dashboardreply = Serial.parseInt();
        if (dashboardreply == 1)//if there is force feed button from dash board
        {           
            //set the processing LED to high
            digitalWrite(Yellow_LED,HIGH);

            //move the servo motor & led 
            for (int i = 0; i < 4; i++)
            {
                digitalWrite(Servo_Motor_replacement_led,HIGH);
                Servo_motor.write(180);
                delay(1000);
                Servo_motor.write(0);
                digitalWrite(Servo_Motor_replacement_led,LOW);
                delay(1000);
            }
            
            //play the buzzer
            for (int i = 0; i < 4; i++)
            {
                tone(7, 220, 100);
                delay(1000);
            }
            
            //set the finish pouring led to high and turn off processing led
            digitalWrite(Yellow_LED,LOW);
            digitalWrite(Blue_LED,HIGH);
            delay(5000);
            digitalWrite(Blue_LED,LOW);
        }
        else if (dashboardreply == 2)//if the user sets the feeding function to normal mode
        {
            //set the processing LED to high
            digitalWrite(Yellow_LED,HIGH);

            //move the servo motor
            for (int i = 0; i < 4; i++)
            {
                digitalWrite(Servo_Motor_replacement_led,HIGH);
                Servo_motor.write(180);
                delay(1000);
                Servo_motor.write(0);
                digitalWrite(Servo_Motor_replacement_led,LOW);
                delay(1000);
            }
            
            //play the buzzer
            for (int i = 0; i < 4; i++)
            {
                tone(7, 220, 100);
                delay(1000);
            }
            
            //set the finish pouring led to high and turn off processing led
            digitalWrite(Yellow_LED,LOW);
            digitalWrite(Blue_LED,HIGH);
            delay(5000);
            digitalWrite(Blue_LED,LOW);
        }
        else if (dashboardreply == 3)//if the user sets the feeding function to diet mode
        {//set the processing LED to high
            digitalWrite(Yellow_LED,HIGH);

            //move the servo motor
            for (int i2 = 0; i2 < 3; i2++)
            {
                digitalWrite(Servo_Motor_replacement_led,HIGH);
                Servo_motor.write(180);
                delay(1000);
                Servo_motor.write(0);
                digitalWrite(Servo_Motor_replacement_led,LOW);
                delay(1000);
            }
            
            //play the buzzer
            for (int i = 0; i < 3; i++)
            {
                tone(7, 220, 100);
                delay(1000);
            }
            
            //set the finish pouring led to high and turn off processing led
            digitalWrite(Yellow_LED,LOW);
            digitalWrite(Blue_LED,HIGH);
            delay(5000);
            digitalWrite(Blue_LED,LOW);
        }
    }
}

