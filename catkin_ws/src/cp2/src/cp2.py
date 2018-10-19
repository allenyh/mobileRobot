#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray, String



class MobileCP2(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        # Publisher
        self.pub = rospy.Publisher("/Rpi/pub", Int16MultiArray, queue_size=1)

        # Subscriber
        self.sub = rospy.Subscriber("Rpi/sub", String, self.cb, queue_size=1)
            
    def cb(self, msg):
        print msg.data
        self.read_input()

    def read_input(self):
        speed_l = input('User\'s left is ')
        speed_r = input('User\'s right is ')
        pub_msg = Int16MultiArray()
        pub_msg.data = [speed_l, speed_r]
        self.pub.publish(pub_msg)

if __name__ == "__main__":
    rospy.init_node("cp2",anonymous=False)
    cp2 = MobileCP2()
    cp2.read_input()
    rospy.spin()
     	
