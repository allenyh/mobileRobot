/*
 * mobile robots check point 2
 * first receive a pair of int number from rpi
 * which indicating speed for car
 * then transform it into pwm value and send to
 * l298n to propel the car
 */

#include <ros.h>
#include <std_msgs/Int16MultiArray.h>
#include <std_msgs/String.h>
#include <Motor.h>

#define in1 4
#define in2 5
#define enA 3
#define in3 7
#define in4 8
#define enB 6

ros::NodeHandle  nh;
int pwm_l = 0;
int pwm_r = 0;
int pwm_l_old = 0;
int pwm_r_old = 0;
Motor m1;
Motor m2;

void messageCb(const std_msgs::Int16MultiArray& msg){
  pwm_l = msg.data[0];
  pwm_r = msg.data[1];
}


ros::Subscriber<std_msgs::Int16MultiArray> sub("/arduino/sub", messageCb );

std_msgs::String speed_change;
ros::Publisher pub("/arduino/pub", &speed_change);

void setup()
{
  m1.set(in1, in2, enA);
  m1.setup();
  m2.set(in4, in3, enB);
  m2.setup();
  
  nh.initNode();
  nh.advertise(pub);
  nh.subscribe(sub);
  delay(10);
  //pwm_l = 150;
  //pwm_r = 150;
}

void loop()
{
  if(pwm_l != pwm_l_old || pwm_r != pwm_r_old){
    m1.setSpeed(pwm_l * 0.8);
    m2.setSpeed(pwm_r * 1.24);
    delay(50);
    m1.setSpeed(pwm_l);
    pwm_l_old = pwm_l;
    pwm_r_old = pwm_r;
    speed_change.data = "speed has changed";
    pub.publish(&speed_change);
  }
  nh.spinOnce();
  delay(10);

}

