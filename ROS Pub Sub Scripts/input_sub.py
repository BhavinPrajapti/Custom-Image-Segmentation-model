#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

def callback(data):
    rospy.loginfo("Received data: %d", data.data)

def data_subscriber():
    rospy.init_node('data_subscriber_node', anonymous=True)
    
    rospy.Subscriber('bin_data_0', Int32, callback)
    rospy.Subscriber('bin_data_1', Int32, callback)
    
    rospy.spin()

if __name__ == '__main__':
    data_subscriber()

