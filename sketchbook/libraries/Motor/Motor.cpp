#include "Motor.h"
#include<Arduino.h>
Motor::Motor(){}

void Motor::set(int ina,int inb,int en){
  in1 = ina;
  in2 = inb;
  enable = en;
} 

void Motor::setup(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  analogWrite(enable, 0);
}

void Motor::setSpeed(int pwm){
  if(pwm > 0){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else if(pwm < 0){
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
  else{
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
  if(abs(pwm) > pwm_max)
    pwm = pwm_max;
  else if(abs(pwm) < pwm_min)
    pwm = pwm_min;
  else
    pwm = abs(pwm);
  analogWrite(enable, pwm);
}
