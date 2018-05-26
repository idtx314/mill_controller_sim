#!/usr/bin/env python
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import bitlib
import rospy
import sys
import math


#Point()  #Don't declare this here. Any modification of the global would affect every point in the list if I try to use just one.

'''
TODO
ADD a tf frame publisher?
Take list of lists or string as input
use input to set the positions of x,y,z based on time
'''

'''
Calculate pixel density
determine list of points in shape
drill is a lists of points (or dict of point:size pairs)
at each time step, check whether each point on the drill is within range of any point in the shape and .remove that point from the shape if so.
'''




def main(arg):
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



    bit = bitlib.simpleBit(-1.0, 0.1, 1.0)         #create a bit instance at -1.0, 0.1, 1.0


    # Init publisher
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
    msg.color.b = 1.0

    #Prep Message 2 for drill bit
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

    msg2.points = bit.points      #Should just be equals in the end

    #Prep Message 3 for removed points
    msg3 = Marker()  #Only ever need one message to publish
    msg3.header.frame_id = "base"
    msg3.ns = "ns"
    msg3.id = 2     #implicit
    msg3.type = Marker.SPHERE_LIST  #7
    #msg3.action = Marker.ADD

    msg3.pose.orientation.w = 1.0
    msg3.scale.x = 0.05   #x axis scale
    msg3.scale.y = 0.05   #y axis scale
    msg3.scale.z = 0.05   #z axis scale
    msg3.color.a = 1.0
    msg3.color.g = 1.0
    msg3.color.r = 1.0
    msg3.color.b = 1.0

    i = 0
    x = y = z = 0


    # Generate Shape
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
    while (not rospy.is_shutdown() and time < 4):
        #Stamp Message
        msg.header.stamp = rospy.Time.now()
        msg2.header.stamp = rospy.Time.now()
        msg3.header.stamp = rospy.Time.now()



        #publish message
        pub.publish(msg)
        pub.publish(msg2)
        pub.publish(msg3)
        rate.sleep()


        # Increment Time
        time += 1./frequency

        # Update Drill Position
        if time < 2.0:
            bit.update_bit(bit.points[0].x + 1.0/frequency, bit.points[0].y + 0.0/frequency, bit.points[0].z + 0.0/frequency) # x=t-1
        elif time < 2.8:
            bit.update_bit(bit.points[0].x - 1.0/frequency, bit.points[0].y + 1.0/frequency, bit.points[0].z + 0.0/frequency)
        else:
            bit.update_bit(bit.points[0].x + 1.0/frequency, bit.points[0].y + 0.0/frequency, bit.points[0].z + 0.0/frequency)


        # TODO Move this function into the bit? The bit knows its own specifications, so if you pass it the object it could remove points and then optionally return the list of points it removed
        # Make a list of points too close to the drill
        templist = []
        for point in msg.points:
            for edge in bit.points:
                if distance(point, edge) < radius:
                    templist.append(point)
                    break

        # Remove points from the cube and add them to the trash list
        for point in templist:
            msg.points.remove(point)
            msg3.points.append(point)







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
    if(len(sys.argv) == 2):
        main(sys.argv[1])
    else:
        print "Usage: inputsim.py <input list>"
