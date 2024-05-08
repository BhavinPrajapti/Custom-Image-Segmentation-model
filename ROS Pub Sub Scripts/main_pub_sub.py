#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String, Int32
from cv_bridge import CvBridge
import cv2
import math
from ultralytics import YOLO
import threading

bridge = CvBridge()
model = YOLO('best-seg.pt')
lock = threading.Lock()

def image_callback(msg):
    try:
        frame = bridge.imgmsg_to_cv2(msg, "bgr8")
        detected_classes = []
        confidences = []

        with lock:
            results = model(frame, save=False, conf=0.6)

            for result in results:
                boxes = result.boxes.cpu().numpy()
                for box in boxes:
                    r = box.xyxy[0].astype(int)
                    cv2.rectangle(frame, r[:2], r[2:], (255, 255, 255), 2)

                    cls = box.cls
                    class_names = ['Bin_red', 'Bin_yellow']
                    output_index = int(cls[0])
                    detected_class = class_names[output_index]
                    detected_classes.append(detected_class)

                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    confidences.append(confidence)

        annotated_frame = results[0].plot()

        cv2.imshow("Annotated Frame", annotated_frame)
        cv2.waitKey(1)

        # Publish the detected class names as a ROS String message
        class_msg = ", ".join(detected_classes)
        class_pub.publish(class_msg)

        # Publish the confidences as a ROS String message
        confidence_msg = ", ".join(f"{conf:.2f}" for conf in confidences)
        confidence_pub.publish(confidence_msg)

        class_indices = [0 if cls == 'Bin_red' else 1 for cls in detected_classes]

        for index in class_indices:
            index_msg = Int32()
            index_msg.data = index
            class_index_pub.publish(index_msg)

        annotated_msg = bridge.cv2_to_imgmsg(annotated_frame, "bgr8")
        annotated_pub.publish(annotated_msg)

    except Exception as e:
        print(e)

def listener():
    rospy.init_node('image_subscriber', anonymous=True)
    rospy.Subscriber('/webcam', Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        class_pub = rospy.Publisher('/detected_class', String, queue_size=1)
        confidence_pub = rospy.Publisher('/detected_confidence', String, queue_size=1)
        class_index_pub = rospy.Publisher('/detected_class_index', Int32, queue_size=1)
        annotated_pub = rospy.Publisher('/annotated_webcam', Image, queue_size=1)
        listener()
    except rospy.ROSInterruptException:
        pass

