#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray, String
import RPi.GPIO as gpio
import time
import thread
import random


class MobileCP4(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        self.lightPin = 3
        self.irPin = 5

        self.leftTouchPin = 29
        self.rightTouchPin= 31
        self.middleTouchPin = 33

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
        self.detecttime = 0.1 #0.0037 for 1500hz, 0.0017 for 600 hz
        self.ir_ratio_low = [0.27, 0.15] #0.15
        self.ir_ratio_high = [0.32, 0.22] #0.22
        
        self.gate = rospy.get_param("~gate") #0 for 600hz, 1 for 1500hz
        self.abc = rospy.get_param("~abc")
        print "abc=" + str(self.abc)
        print "gate freq: " + str(900 * self.gate + 600) +"Hz"

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.lightPin, gpio.IN)
        gpio.setup(self.irPin, gpio.IN)
        gpio.setup(self.leftTouchPin, gpio.IN)
        gpio.setup(self.rightTouchPin, gpio.IN)
        gpio.setup(self.middleTouchPin, gpio.IN)
        
        # Publisher
        self.pub = rospy.Publisher("/Rpi/pub", Int16MultiArray, queue_size=1)

        # Subscriber
        #self.sub = rospy.Subscriber("Rpi/sub", String, self.cb, queue_size=1)

        #try:
        threadLight = thread.start_new_thread(self.updateLight, ())
        threadIR = thread.start_new_thread(self.updateIR, ())
        threadTouch = thread.start_new_thread(self.updateTouch, ())
        rospy.loginfo("thread all start")
        #except:
            #rospy.loginfo("shutdown")
            #rospy.signal_shutdown("unable to start thread")

        self.start_find()
            
    '''def cb(self, msg):
        if msg.data == "find":
            self.stage = 1
        elif msg.data == "reach":
            self.stage = 2 
        else:
            print msg.data'''

    def updateLight(self):
        while True:
            self.lightSignal = gpio.input(self.lightPin)
            if self.stage == 0:
                print "light:" + str(self.lightSignal)
            time.sleep(0.1)

    def updateIR(self):
        while True:
            ir_timer = time.time()
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
                self.irSignal = 0
            else:
                self.irSignal = 1
            
            if self.stage == 1:
                print "ratio: " + str(ratio)
                print "ir: " + str(self.irSignal)

            time.sleep(0.1)

    def updateTouch(self):
        while True: 
            self.leftTouchSignal = gpio.input(self.leftTouchPin)
            self.rightTouchSignal = gpio.input(self.rightTouchPin)

            if self.stage == 1:
                if self.leftTouchSignal == 1 or self.rightTouchSignal == 1:
                    self.stage = 0

            self.middleTouchSignal = gpio.input(self.middleTouchPin)
            if self.middleTouchSignal == 1:
                self.stage = 1
            #print "left :" + str(self.leftTouchSignal) + " right :" + str(self.rightTouchSignal) + " middle :" + str(self.middleTouchSignal)
            time.sleep(0.2)

    def start_find(self):
        wait_sec = 3
        for i in range(wait_sec):
            print "start in " + str(wait_sec-i) + " secs"
            time.sleep(1)
        rospy.loginfo("start find")
        self.timer = time.time()
        while not rospy.is_shutdown():
            if self.stage == 0: # find ball, strategy: directly bypass the obstacle and circling for searching
                rospy.loginfo("stage 0")
                if self.first == True:
                    rospy.loginfo("first")
                    self.bypass_obs()
                    self.first = False
                else:
                    if self.leftTouchSignal == 1 or self.rightTouchSignal == 1:
                        self.avoid()
                    if self.lightSignal != 0:
                        rospy.loginfo("search light")
                        self.search('light')
                    else:
                        self.rush()
            else:
                rospy.loginfo("stage 1")
                if self.leftTouchSignal == 1 or self.rightTouchSignal == 1:
                    self.avoid()
                    self.stage = 0
                if self.irSignal != 0:
                    rospy.loginfo("search ir")
                    self.search('ir')
                else:
                    self.rush()

                
   
    def bypass_obs(self):
        if self.abc == 'a' or self.abc == 'c':
            #walk staraight for 3.2 sec, which is yy distance
            action = Int16MultiArray()
            action.data = [8,0]
            self.pub.publish(action)
            time.sleep(3)
            action = Int16MultiArray()
            if self.abc == 'c': # left turn 90 degree
                action.data = [0,6]
            else: # right turn 90 degree
                action.data = [0,-6]
            self.pub.publish(action)
            time.sleep(0.5)
            #walk straight for 1 sec, which is bb distance
            action = Int16MultiArray()
            action.data = [6,0]
            self.pub.publish(action)
            time.sleep(2.5)
        else:
            #left turn 45 degree
            action = Int16MultiArray()
            action.data = [0,8]
            self.pub.publish(action)
            time.sleep(0.36)

            #walk straight for 1.5 sec
            action = Int16MultiArray()
            action.data = [6,0]
            self.pub.publish(action)
            time.sleep(2)

            #walk counterclockwise for 2 sec
            action = Int16MultiArray()
            action.data = [6,-1]
            self.pub.publish(action)
            time.sleep(2.5)

        #stop here
        action = Int16MultiArray()
        action.data = [0,0]
        self.pub.publish(action)

    def search(self, signal):

        direction = random.randint(0,1)

        # slowly rotate for fixed degree and wait for few msec, repeat for x times
        sig = ""
        for i in range(0, 10):
            if signal == 'light':
                sig = self.lightSignal
            else:
                sig = self.irSignal  

            if self.leftTouchSignal == 1 or self.rightTouchSignal == 1:
                self.avoid()

            if sig == 1:# no detection
                action = Int16MultiArray()
                action.data = [3,24*direction - 12]
                self.pub.publish(action)
                time.sleep(0.1)

                action = Int16MultiArray()
                action.data = [0,0]
                self.pub.publish(action)
                time.sleep(0.23)
            else:
                break
        #if no detection after rotating for 10 times, walk forward a little
        action = Int16MultiArray()
        action.data = [8,0]
        self.pub.publish(action)
        time.sleep(0.7)

    def rush(self):
        print "rush"
        action = Int16MultiArray()
        action.data = [10,0]
        self.pub.publish(action)
        time.sleep(0.3)
    
        if self.leftTouchSignal == 1 or self.rightTouchSignal == 1:
            self.avoid()
    
    def avoid(self):
        # move backward a little
        action = Int16MultiArray()
        action.data = [-10,0]
        self.pub.publish(action)
        time.sleep(0.15)
       
        # rotate either clockwise or counterclockwise, randomly
	direction = random.randint(0,1)
        action = Int16MultiArray()
        action.data = [0, 20 * direction - 10]
        self.pub.publish(action)
        time.sleep(0.15)



if __name__ == "__main__":
    rospy.init_node("cp4",anonymous=False)
    cp4 = MobileCP4()
    rospy.spin()
     	
