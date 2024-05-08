#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

def bin_selector():
    rospy.init_node('bin_selector_node', anonymous=True)
    
    pub_0 = rospy.Publisher('bin_data_0', Int32, queue_size=10)
    pub_1 = rospy.Publisher('bin_data_1', Int32, queue_size=10)
    
    rate = rospy.Rate(10)  # 10 Hz
    
    while not rospy.is_shutdown():
        user_input = int(input("Enter 0 or 1: "))  # Convert input to integer
        if user_input == 0:
            pub_0.publish(0)
        elif user_input == 1:
            pub_1.publish(1)
        else:
            rospy.logwarn("Invalid input. Please enter 0 or 1.")
        rate.sleep()

if __name__ == '__main__':
    try:
        bin_selector()
    except rospy.ROSInterruptException:
        pass

