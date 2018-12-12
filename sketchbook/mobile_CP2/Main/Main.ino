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

int radius = 6.5
int wheel_space = 15 

int v = 0;
int omega = 0;
int v_old = 0;
int omega_old = 0;
float gain = 1.0;
float trim = 0;
float k = 15;
int pwm_l;
int pwm_r;
Motor m1;
Motor m2;

void messageCb(const std_msgs::Int16MultiArray& msg){
  v = msg.data[0];
  omega = msg.data[1];
}


ros::Subscriber<std_msgs::Int16MultiArray> sub("/arduino/sub", messageCb );

//std_msgs::String speed_change;
//ros::Publisher pub("/arduino/pub", &speed_change);

void setup()
{
  m1.set(in1, in2, enA);
  m1.setup();
  m2.set(in4, in3, enB);
  m2.setup();
  
  nh.initNode();
  //nh.advertise(pub);
  nh.subscribe(sub);
  delay(10);
}

void loop()
{
  if(v != v_old || omega != omega_old){

    pwm_l = (gain + trim) * (v + 0.5 * omega) * k
    pwm_r = (gain - trim) * (v - 0.5 * omega) * k

    m1.setSpeed(pwm_l);
    m2.setSpeed(pwm_r);
    pwm_l_old = pwm_l;
    pwm_r_old = pwm_r;
  }
  nh.spinOnce();
  delay(10);

}

