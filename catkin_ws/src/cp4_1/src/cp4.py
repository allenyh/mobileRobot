#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray, String
import RPi.GPIO as gpio
import time
import thread


class MobileCP4(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        self.lightPin = 3
        self.irPin = 5

        self.leftTouchPin = 29
        self.rightTouchPin= 31
        self.middleTouchPin = 32

        self.lightSignal = 1
        self.irSignal = 1
        self.leftTouchSignal = 0
        self.rightTouchSignal = 0
        self.middleTouchSignal = 0

        self.first = True
 
        self.stage_count = 0
        self.stage = 0 #0 for finding light ball, 1 for finding gates
        self.recount = False
        self.timer = 0
        self.detecttime = 0.2 #0.0037 for 1500hz, 0.0017 for 600 hz
        self.ir_ratio_low = [0.27, 0.17] #0.17
        self.ir_ratio_high = [0.32, 0.22] #0.22
        self.gate = 0 #0 for 600hz, 1 for 1500hz
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.lightPin, gpio.IN)
        gpio.setup(self.irPin, gpio.IN)
        gpio.setup(self.leftTouchPin, gpio.IN)
        gpio.setup(self.rightTouchSignal, gpio.IN)
        gpio.setup(self.middleTouchPin, gpio.IN)
        
        # Publisher
        self.pub = rospy.Publisher("/Rpi/pub", Int16MultiArray, queue_size=1)

        # Subscriber
        #self.sub = rospy.Subscriber("Rpi/sub", String, self.cb, queue_size=1)

        try:
            thread.start_new_thread(updateLight)
            thread.start_new_thread(updateIR)
            thread.start_new_thread(updateTouch)
        except:
            rospy.signal_shutdown("unable to start thread")

        self.start_find()
            
    '''def cb(self, msg):
        if msg.data == "find":
            self.stage = 1
        elif msg.data == "reach":
            self.stage = 2 
        else:
            print msg.data'''

    def updateLight(self):
        self.lightSignal = gpio.input(self.lightPin)
        print self.lightSignal
        time.sleep(0.1)

    def updateIR(self):
        start = time.time()
        count = 0
        total_count = 0
        while (time.time() - ir_timer) <= self.detecttime:
            ir = gpio.input(self.irPin)
            total_count += 1.0
            if ir == 0:
                count += 1.0
        ratio = count / total_count
        if ratio >= self.ir_ratio_low[self.gate] and ratio <= self.ir_ratio_high[self.gate]:
            print "gate found"
        self.irSignal = 1
        time.sleep(0.1)

    def updateTouch(self):
        self.leftTouchSignal = gpio.input(leftTouchPin)
        self.rightTouchSignal = gpio.input(rightTouchPin)
        self.middleTouchSignal = gpio.input(middleTouchPin)
        print "left "

    def start_find(self):
        self.timer = time.time()
        while not rospy.is_shutdown():
            if self.stage == 0: # find ball, strategy: directly bypass the obstacle and circling for searching
                if self.first == True:
                    self.bypass_obs()
                else:
                    self.search()
   
    def bypass_obs(self):
        #walk staraight for xx sec, which is yy distance
        action = Int16MultiArray()
        action.data[0] = 5
        action.data[1] = 0
        self.pub.publish(action)
        time.sleep(0.3)

        #left turn 90 degree
        action = Int16MultiArray()
        action.data[0] = 0
        action.data[1] = 5
        self.pub.publish(action)
        time.sleep(0.2)

        #walk straight for aa sec, which is bb distance
        action = Int16MultiArray()
        action.data[0] = 5
        action.data[1] = 0
        self.pub.publish(action)
        time.sleep(0.2)

        #stop here
        action = Int16MultiArray()
        action.data[0] = 0
        action.data[1] = 0
        self.pub.publish(action)

    def search(self):
        #slow rotate for fixed degree and wait for few msec, repeat for x times
        for i in range(0, 10):
            if self.lightSignal == 1:# no detect of light
                action = Int16MultiArray()
                action.data[0] = 0
                action.data[1] = 5
                self.pub.publish(action)
                time.sleep(0.2)
            else:
                break



if __name__ == "__main__":
    rospy.init_node("cp4",anonymous=False)
    cp4 = MobileCP4()
    rospy.spin()
     	
