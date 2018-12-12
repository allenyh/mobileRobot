/*
 * mobile robots check point 4
 * first receive a pair of int number from rpi
 * which indicating speed for car
 * then transform it into pwm value and send to
 * l298n to propel the car
 */

#include <ros.h>
#include <std_msgs/Int16.h>
#include <std_msgs/String.h>
#include <Motor.h>

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

int stat = 0;
int turn_count = 0;
boolean start = false;
ros::NodeHandle  nh;
int stage = 1;
int pwm_l = 90;
int pwm_r = 100;
int pwm_l_old = 90;
int pwm_r_old = 100;
Motor m1;
Motor m2;
boolean left=LOW,right=LOW,middle=LOW;

void rotate();
void go_straight();
void turn();
void back_right();
void back_left();
void turn_ninty();
void tunr_mninty();

std_msgs::String car_stat;
ros::Publisher pub("/arduino/pub", &car_stat);

void messageCb(const std_msgs::Int16& msg)
{
  stat = msg.data;
}

ros::Subscriber<std_msgs::Int16> sub("/arduino/sub", messageCb );

void setup()
{
  m1.set(in1, in2, enA);
  m1.setup();
  m2.set(in4, in3, enB);
  m2.setup();
  
  pinMode(left_touch, INPUT);
  pinMode(right_touch, INPUT);
  pinMode(middle_touch, INPUT);
  
  nh.initNode();
  nh.advertise(pub);
  nh.subscribe(sub);
  delay(10);
  //pwm_l = 150;
  //pwm_r = 150;
}

void loop()
{
  left = digitalRead(left_touch);
  right = digitalRead(right_touch);
  middle = digitalRead(middle_touch);
  
  if(start == false)
  {
    if(left == HIGH)
      start = true;
  }
  else
  {
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
      car_stat.data = "find";
      pub.publish(&car_stat);
      stage = 2;
    }
    switch(stat){
      case 1:
        rotate();
        break;
      case 0:
        go_straight();
        break;
      case 2:
        turn();
        break;
    }
  }
  nh.spinOnce();
  delay(100);
}

void go_alittle(){
  m1.setSpeed(100);
  m2.setSpeed(115);
  delay(500);
}

void rotate(){
  m1.setSpeed(170);
  m2.setSpeed(0);
  delay(150);
  m1.setSpeed(0);
  delay(300);
  turn_count += 1;
  if(turn_count == 16)
  {
    go_alittle();
    turn_count = 0;
  }
}

void go_straight(){
  m1.setSpeed(95);
  m2.setSpeed(105);
}

void turn(){
  int car_speed = random(0,2);
  
  m1.setSpeed(-260 * car_speed + 130);
  m2.setSpeed(260 * car_speed - 130);
  delay(200);
  stat = 0;
}

void back_left()
{
  if(start == true)
  {
    m1.setSpeed(-100);
    m2.setSpeed(-100);
    delay(200);
    
    turn_mninty();
  }
}

void back_right()
{
  if(start == true)
  {
    m1.setSpeed(-100);
    m2.setSpeed(-100);
    delay(200);
    
    turn_ninty();
  }
}

void turn_ninty()
{
  m1.setSpeed(-200);
  m2.setSpeed(0);
  delay(400);
}

void turn_mninty()
{
  m1.setSpeed(0);
  m2.setSpeed(-200);
  delay(400);
}

