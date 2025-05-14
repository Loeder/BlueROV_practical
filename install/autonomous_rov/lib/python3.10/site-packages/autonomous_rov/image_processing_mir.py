#!/usr/bin/env python
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import CompressedImage
import cv2
# import camera_parameters as cam

# Contents of camera_parameters.py #################################
# camera parameters
u0 = 320
v0 = 240
lx = 455
ly = 455
kud =0.00683 
kdu = -0.01424     
    
# convert a pixel coordinate to meters given linear calibration parameters
def convert2meter(pt,u0,v0,lx,ly):
    return (float(pt[0])-u0)/lx, (float(pt[1])-v0)/ly

# convert a pixel coordinate to meters using defaut calibration parameters
def convertOnePoint2meter(pt):
    global u0,v0,lx, ly
    return (float(pt[0])-u0)/lx, (float(pt[1])-v0)/ly

# convert a list of pixels coordinates to meters using defaut calibration parameters
def convertListPoint2meter (points):
    global u0,v0,lx, ly
    
    if(np.shape(points)[0] > 1):
        n = int(np.shape(points)[0]/2)
        point_reshaped = (np.array(points).reshape(n,2))
        point_meter = []
        for pt in point_reshaped:
            pt_meter = convert2meter(pt,u0,v0,lx,ly)
            point_meter.append(pt_meter)
        point_meter = np.array(point_meter).reshape(-1)
        return point_meter

###############################################################

# display point and text in an image>
# param image : the image to overlay
# param pt : array that represents the 2D point in pixel 
# param r : red intensity
# param g : green intensity
# param b : blue intensity
# OPT param text : text to display near to the point, default empty
# OPT param scale : dot circle scale default 1
# OPT param offsetx : x offset of the text wrt the dot default 5
# OPT param offsety : y offset of the text wrt the dot default 5
def overlay_points(image, pt, r, g, b, text="", scale=1, offsetx=5, offsety=5):
    cv2.circle(image, (int(pt[0]), int(pt[1])), int(4 * scale + 1), (b, g, r), -1)
    position = (int(pt[0]) + offsetx, int(pt[1]) + offsety)
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, (b, g, r, 255), 1)


# Function that is called at every image frame
# by the image subscriber
# output the position in meter of 
# the point to track
def cameracallback(image_data):
    # get image data
    np_arr = np.frombuffer(image_data.data, np.uint8)  # Changed from np.fromstring to np.frombuffer
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # get image size
    image_height, image_width, image_channels = image_np.shape
    print(image_height, image_width, image_channels)

    # display image data
    cv2.namedWindow("image")

    # broadcast center of the buoy
    # default coordinates in pixels
    desired_point = [image_width / 2, image_height / 2]

    current_point = [50, 50]
    #=================================#
    # TODO 1. track the buoy  :       #
    # insert your code here           #
    # to set the right current point  #
    #=================================#

    # display on the image
    overlay_points(image_np, current_point, 0, 255, 0, 'current tracked buoy')

    # display on the image
    overlay_points(image_np, desired_point, 255, 0, 0, 'desired point')

    # convert the point into meter
    current_point_meter = cam.convertOnePoint2meter(current_point)
    print('current points in meter', current_point_meter)
    current_point_msg = Float64MultiArray(data=current_point_meter)
    pub_tracked_point.publish(current_point_msg)

    desired_point_meter = cam.convertOnePoint2meter(desired_point)
    print('desired point in meter', desired_point_meter)
    desired_point_msg = Float64MultiArray(data=desired_point_meter)
    pub_tracked_point.publish(desired_point_msg)

    cv2.imshow("image", image_np)
    cv2.waitKey(2)


# Subscribers
class ImageProcessingNode(Node):
    def __init__(self):
        super().__init__('image_processing_mir')
        self.get_logger().info('image processing launched')

        # Initialize publishers
        self.pub_tracked_point = self.create_publisher(Float64MultiArray, "tracked_point", 1)
        self.pub_desired_point = self.create_publisher(Float64MultiArray, "desired_point", 1)

        # Initialize subscriber to video stream, either BlueRov or webcam
        # image_topic_name = self.declare_parameter('cam_name', 'uasb_cam/image/compressed').value
        # image_topic_name = self.declare_parameter('cam_name', 'bluerov2/camera/image').value
        image_topic_name = self.declare_parameter('cam_name', 'webcam/image_raw').value 

        self.create_subscription(
            CompressedImage,
            image_topic_name,
            cameracallback,
            1
        )


def main(args=None):
    rclpy.init(args=args)
    image_processing_node = ImageProcessingNode()

    # Keep the node running
    rclpy.spin(image_processing_node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
