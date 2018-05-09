#!/usr/bin/env python
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import rospy
import sys
import math


#Point()  #Don't declare this here. Any modification of the global would affect every point in the list if I try to use just one.

'''
TODO
Publish static sphere list
ADD a frame publisher?
'''
'''
Calculate pixel density
determine list of points in shape
drill is a lists of points (or dict of point:size pairs)
at each time step, check whether each point on the drill is within range of any point in the shape and .remove that point from the shape if so.
'''


def main():
    frequency = 10
    NUMPTS = 250
    xlength = 1
    ylength = 1
    zlength = 1
    ltotal = xlength + ylength + zlength    #3
    lpoints = int(NUMPTS/ltotal)            #9
    xpts = int(float(xlength)/ltotal * lpoints)         #3
    ypts = int(float(ylength)/ltotal * lpoints)
    zpts = int(float(zlength)/ltotal * lpoints)
    xinc = float(xlength)/(xpts-1)                 #0.5
    yinc = float(ylength)/(ypts-1)
    zinc = float(zlength)/(zpts-1)
    step = 1 # Should be calculated from the number of points and desired size
    time = 0.0
    timestep = 0.0
    radius = .1


    bit = [Point()]         #bit[0] represents the drill point. It will be updated with each timestep and points in the cube too close to it will be removed.
    bit[0].x= time - 1.0
    bit[0].y= 0
    bit[0].z = 1


    #init publisher
    pub = rospy.Publisher("visualization_marker", Marker, queue_size=10)
    rospy.init_node('cube_pub')
    rate = rospy.Rate(frequency)  #Publish rate



    #Prep Message
    msg = Marker()  #Only ever need one message to publish
    msg.header.frame_id = "base"
    msg.ns = "ns"
    #msg.id = 0     #implicit
    msg.type = Marker.SPHERE_LIST  #7
    #msg.action = Marker.ADD

    msg.pose.orientation.w = 1.0
    msg.scale.x = 0.05   #x axis scale
    msg.scale.y = 0.05   #y axis scale
    msg.scale.z = 0.05   #z axis scale
    msg.color.a = 1.0
    msg.color.r = 1.0

    #Prep Message 2
    msg2 = Marker()  #Only ever need one message to publish
    msg2.header.frame_id = "base"
    msg2.ns = "ns"
    msg2.id = 1     #implicit
    msg2.type = Marker.SPHERE_LIST  #7
    #msg2.action = Marker.ADD

    msg2.pose.orientation.w = 1.0
    msg2.scale.x = 0.05   #x axis scale
    msg2.scale.y = 0.05   #y axis scale
    msg2.scale.z = 0.05   #z axis scale
    msg2.color.a = 1.0
    msg2.color.g = 1.0

    msg2.points.append(bit[0])      #Should just be equals in the end


    i = 0
    x = y = z = 0

    # for point in range(0, NUMPTS):
    #     msg.points.append(Point())
    #     msg.points[i].x = i
    #     i+=1


    # for incrementx in range(0,xlength+1, step):
    #     for incrementy in range(0,ylength+1, step):
    #         for incrementz in range(0,zlength+1, step):
    #             msg.points.append(Point())
    #             msg.points[i].x = incrementx
    #             msg.points[i].y = incrementy
    #             msg.points[i].z = incrementz
    #             i+=1


    for pointx in range(0,xpts):     #[0,1,2]
        for pointy in range(0,ypts):
            for pointz in range(0,zpts):
                msg.points.append(Point())
                msg.points[i].x = x
                msg.points[i].y = y
                msg.points[i].z = z
                z += zinc
                i += 1
            y += yinc
            z=0
        x += xinc
        y=0

    # print xpts
    # print msg
    # sys.exit(0)

# points to iterate through = side length/side total * numpts/side total
# increment for coordinates = first at 0, increment by side length/(points to iterate through - 1)



#points is a list of Point messages
#can use list.append(Point()) and then access that point by index


#Number of points per side is independent of length. The distribution of points will always be the same, it's just the increment that changes.
#Minimum of 4 points in a layer of a cube
# Allow user to input lengthof sides and resolution per cm^3. Calculate the appropriate number of points.




    #loop
    while (not rospy.is_shutdown() and time < 3):
        #Stamp Message
        msg.header.stamp = rospy.Time.now()
        msg2.header.stamp = rospy.Time.now()



        #publish message
        pub.publish(msg)
        pub.publish(msg2)
        rate.sleep()


        # Increment Time
        time += 1./frequency

        # Update Drill Position
        bit[0].x = time - 1.0     # x = t - 1


        # Update Cube List
        templist = []
        for point in msg.points:
            for edge in bit:
                if distance(point, edge) < radius:
                    templist.append(point)
                    break

        for point in templist:
            msg.points.remove(point)






# Run commands
# rosrun tf static_transform_publisher 0 0 0 0 0 0 world base 100
# rviz
# roscore
# ./generator.py  OR  rosrun mill_visualizer_v1 generator.py


def distance(point, edge):
    '''
    Determine the distance between the Point() messages point and edge.
    '''

    sqrdsum = math.pow(point.x-edge.x, 2) + math.pow(point.y-edge.y, 2) + math.pow(point.z-edge.z, 2)
    distance = math.sqrt(sqrdsum)
    return distance









if __name__ == '__main__':
    main()