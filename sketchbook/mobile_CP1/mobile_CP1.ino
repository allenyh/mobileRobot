/*
 * mobile robots check point 1
 * first receive a int number from rpi
 * then multiply it by 2 and return
 */

#include <ros.h>
#include <std_msgs/Int32.h>

ros::NodeHandle  nh;
int num;
boolean send_flag = true;

void messageCb(const std_msgs::Int32& msg){
  num = msg.data * 2;
  send_flag = false;
}

std_msgs::Int32 send_num;

ros::Subscriber<std_msgs::Int32> sub("/arduino/sub", messageCb );


ros::Publisher pub("/arduino/pub", &send_num);

void setup()
{
  Serial.begin(57600);
  Serial.println("start");
  nh.initNode();
  nh.advertise(pub);
  nh.subscribe(sub);
}

void loop()
{
  if(send_flag != true){
    send_num.data = num;
    pub.publish(&send_num);
    send_flag = true;
  }
  nh.spinOnce();
  delay(1);

}

