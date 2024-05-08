#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32, String


class_index=-1
confidence=0
class_index_input=-1

def callback(data):
    #rospy.loginfo("Received data: %d", data.data)
    class_index_input=data.data
    print("class index inputed:",class_index_input)

def confidence_callback(msg):
    confidence = msg.data
    print("confidence",confidence)

def class_index_callback(msg):
    
    class_index=msg.data
    print("class detected:",class_index)
 


def listener():
    rospy.init_node('confidence_subscriber', anonymous=True)
    rospy.Subscriber('/detected_confidence', String, confidence_callback)
    rospy.Subscriber('/detected_class_index', Int32, class_index_callback)
   
    rospy.Subscriber('bin_data_0', Int32, callback)
    rospy.Subscriber('bin_data_1', Int32, callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
        
        
    except rospy.ROSInterruptException:
        pass
        
        
        
        

