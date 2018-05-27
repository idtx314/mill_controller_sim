#!/usr/bin/env python
import rospy
import tf




def main():

    # Init
    rospy.init_node('transform_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(100)  #Publish rate

    # Broadcast frames
    while not rospy.is_shutdown():
        br.sendTransform((0.0, 0.0, 0.0),
                         (0, 0, 0, 1),
                         # (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w),
                         rospy.Time.now(),
                         "base",
                         "world")
        rate.sleep()









if __name__ == '__main__':
    main()
