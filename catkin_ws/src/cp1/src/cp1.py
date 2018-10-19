#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32



class MobileCP1(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        # Publisher
        self.pub = rospy.Publisher("/Rpi/pub", Int32, queue_size=1)

        # Subscriber
        self.sub = rospy.Subscriber("Rpi/sub", Int32, self.cb, queue_size=1)
            
    def cb(self, msg):
        print "message from Arduino is "+str(msg.data)
        self.read_input()

    def read_input(self):
        num = input('User\'s input is ')
        pub_msg = Int32()
        pub_msg.data = num
        self.pub.publish(pub_msg)

if __name__ == "__main__":
    rospy.init_node("cp1",anonymous=False)
    cp1 = MobileCP1()
    cp1.read_input()
    rospy.spin()
     	
