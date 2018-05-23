from geometry_msgs.msg import Point

class simpleBit:
    # TODO
    # Add custom distance list with default values
    # generate points automatically

    # A list of the points representing the bit
    points = [Point(),Point(),Point(),Point(),Point(),Point()]

    # Positions of each point in the root point reference frame
    relations =[Point(
                    x = 0.0,
                    y = 0.0,
                    z = 0.0),
                Point(
                    x = 0.1,
                    y = 0.0,
                    z = 0.0),
                Point(
                    x = 0.0,
                    y = 0.1,
                    z = 0.0),
                Point(
                    x = -0.1,
                    y = 0.0,
                    z = 0.0),
                Point(
                    x = 0.0,
                    y = -0.1,
                    z = 0.0),
                Point(
                    x = 0.0,
                    y = 0.0,
                    z = -0.1)
    ]

    # A function that inits the point at the given starting position, or at 0,0,0 as default
    def __init__(self, x=0, y=0, z=0):
        #Make a list of points of length = len(input)+1,
        #store the relations separately
        self.update_bit(x, y, z)


    def update_bit(self, x, y, z):

        # Set the position of the root point
        self.points[0].x = x
        self.points[0].y = y
        self.points[0].z = z

        # Cycle through the other points in the bit and update them based on the new location of the root point
        for index in range(1,len(self.points)):
            self.points[index].x = self.points[0].x + self.relations[index].x
            self.points[index].y = self.points[0].y + self.relations[index].y
            self.points[index].z = self.points[0].z + self.relations[index].z


    # A function that moves the entire bit based on inputfor a single point
    # Input: x, y, z, yaw, pitch, roll update
    # Output: updates self.points to correctly represent the new position

    # A function that returns the position of the bit
    # Input: None
    # Output: A list of points representing the bit. This is useless
