#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16, String
import RPi.GPIO as gpio
import time


class MobileCP4(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        self.lightpin = 3
        self.irpin = 5
        self.stage_count = 0
        self.gate_count = 0
        self.gate_found = False
        self.stage = 0 #0 for finding light ball, 1 for finding gates
        self.recount = False
        self.timer = 0
        self.detecttime = 0.2 #0.0037 for 1500hz, 0.0017 for 600 hz
        self.ir_ratio_low = [0.27, 0.17] #0.17
        self.ir_ratio_high = [0.32, 0.22] #0.22
        self.gate = 0 #0 for 600hz, 1 for 1500hz
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.lightpin, gpio.IN)
        gpio.setup(self.irpin, gpio.IN)
        
        # Publisher
        self.pub = rospy.Publisher("/Rpi/pub", Int16, queue_size=1)

        # Subscriber
        self.sub = rospy.Subscriber("Rpi/sub", String, self.cb, queue_size=1)

        self.start_find()
            
    def cb(self, msg):
        if msg.data == "find":
            self.stage = 1
        elif msg.data == "reach":
            self.stage = 2 
        else:
            print msg.data

    def start_find(self):
        self.timer = time.time()
        while not rospy.is_shutdown():
            light = gpio.input(self.lightpin)
            print "light"
            print light
            if self.stage == 0: # track light ball
                print "stage: 0"
                if light == 1: # no light detected
                    if (time.time()-self.timer > 3): # time out
                         print "timeout"
                         action = Int16()
                         action.data = 2
                         self.pub.publish(action)
                         self.timer = time.time()
                else: # light detected
                    print "ball found"
                    action = Int16()
                    action.data = 0
                    self.pub.publish(action)
            
           
            elif self.stage == 1: # find gate
                print "stage: 1"
                #if light == 1: #lost light ball
                #    self.stage_count += 1
                #    if self.stage_count == 10: 
                #        print "lost ball"
                #        self.stage = 0
                #        self.stage_count = 0
                #        continue
                ir_timer = time.time()
                count = 0
                total_count = 0
                while (time.time() - ir_timer) <= self.detecttime:
                    ir = gpio.input(self.irpin)
                    total_count += 1.0
                    if ir == 0:
                        count += 1.0
                ratio = count / total_count
                print ratio
                action = Int16()
                if ratio >= self.ir_ratio_low[self.gate] and ratio <= self.ir_ratio_high[self.gate]:
                    print "gate found"
                    action.data = 0
                    self.gate_found = True
                else:
                    if self.gate_found == True:
                        self.gate_count += 1
                        if self.gate_count == 5:
                            self.gate_count = 0
                            self.gate_found = False
                    action.data = 1
                self.pub.publish(action)

            time.sleep(0.1) 


if __name__ == "__main__":
    rospy.init_node("cp4",anonymous=False)
    cp4 = MobileCP4()
    rospy.spin()
     	
