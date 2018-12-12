#include <Motor.h>

//define motor pin
#define in1 2
#define in2 5
#define enA 3
#define in3 7
#define in4 8
#define enB 6

//define sensor pin
#define left_touch 10
#define right_touch 9
#define middle_touch 4
#define light A0

void motor_stop();
void back_right();
void back_left();
void turn_ninty();
void go_straight();

//variables for motors
//ros::NodeHandle  nh;
int pwm_l = 0;
int pwm_r = 0;
Motor m1;
Motor m2;
boolean walk = false;

//variables for sensors
boolean left=LOW,right=LOW,middle=LOW;
int li=0;
boolean start = false, detected = false;
unsigned long run_timer;

void setup()
{
  Serial.begin(9600);
  m1.set(in1, in2, enA);
  m1.setup();
  m2.set(in4, in3, enB);
  m2.setup();
  
  //nh.initNode();
  
  pinMode(left_touch, INPUT);
  pinMode(right_touch, INPUT);
  pinMode(middle_touch, INPUT);
  pinMode(light, INPUT);
  Serial.println("start");
}

void loop()
{
  left = digitalRead(left_touch);
  right = digitalRead(right_touch);
  middle = digitalRead(middle_touch);
  li = analogRead(light);
  Serial.print("light : ");
  Serial.println(li);
  if(start == false)
  {
    if(left == HIGH)
      start = true;
  }
  else
  {
    if(li < 200)
    {
      go_straight();
      if(middle == HIGH)
      {
        start = false;
        motor_stop();
      }
    } 
    else
    {
      if(walk == false)
      {
        walk = true;
        go_straight();
        run_timer = millis();
      }
      else if(millis() - run_timer >=3000)
      {
        turn_ninty();
        walk = false;
      }
      if(left == HIGH)
      {
        back_left();
      }
      else if(right == HIGH)
      {
        back_right();
      }
      else if(middle == HIGH)
      {
        start = false;
        motor_stop();
      }
    }
  }
  delay(50);
}

void motor_stop()
{
  m1.setSpeed(0);
  m2.setSpeed(0);
}

void back_left()
{
  if(start == true)
  {
    m1.setSpeed(-100);
    m2.setSpeed(-100);
    delay(100);
    
    turn_mninty();
  }
}

void back_right()
{
  if(start == true)
  {
    m1.setSpeed(-100);
    m2.setSpeed(-100);
    delay(100);
    
    turn_ninty();
  }
}

void turn_ninty()
{
  m1.setSpeed(-100);
  m2.setSpeed(0);
}

void turn_mninty()
{
  m1.setSpeed(0);
  m2.setSpeed(-100);
}

void go_straight()
{
  m1.setSpeed(100);
  m2.setSpeed(120);
}
