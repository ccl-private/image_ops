import numpy as np
import cv2
from openni import openni2  # , nite2
from openni import _openni2 as c_api

# Path of the OpenNI redistribution OpenNI2.so or OpenNI2.dll
dist = "/home/ccl/Apps/OpenNI-Linux-x64-2.3/Redist/"

# Initialize openni and check
openni2.initialize(dist)
if openni2.is_initialized():
    print("openNI2 initialized")
else:
    print("openNI2 not initialized")

# Register the device
dev = openni2.Device.open_any()

# Create the streams stream
rgb_stream = dev.create_color_stream()
depth_stream = dev.create_depth_stream()

# Check and configure the depth_stream -- set automatically based on bus speed
print('The rgb video mode is', rgb_stream.get_video_mode())  # Checks rgb video configuration
print('The depth video mode is', depth_stream.get_video_mode())  # Checks depth video configuration

rgb_stream.set_video_mode(c_api.OniVideoMode(
    pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=640, resolutionY=480, fps=30))
depth_stream.set_video_mode(c_api.OniVideoMode(
    pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX=640, resolutionY=480, fps=30))

# Start the streams
rgb_stream.start()
depth_stream.start()

depth_img = None


def point_and_shoot(event, x, y, flags, param):
    global depth_img
    if event == cv2.EVENT_LBUTTONDOWN:
        point = [(x, y)]
        print(point, depth_img[0, y, x])


# Initial OpenCV Window Functions
cv2.namedWindow("RGB Image")
cv2.namedWindow("Depth Image")
cv2.setMouseCallback("Depth Image", point_and_shoot)

# Use 'help' to get more info
# help(dev.set_image_registration_mode)


# get_rgb
def get_rgb():
    """
    Returns numpy 3L ndarray to represent the rgb image.
    """
    bgr = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(), dtype=np.uint8).reshape(480, 640, 3)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb


def get_depth():
    global depth_img
    depth = np.frombuffer(depth_stream.read_frame().get_buffer_as_uint16(), dtype=np.uint16).reshape(1, 480, 640)
    depth_img = depth.copy()
    depth_show = np.concatenate((depth, depth, depth), axis=0)
    depth_show = np.swapaxes(depth_show, 0, 2)
    depth_show = np.swapaxes(depth_show, 0, 1)
    depth_show = 255 - depth_show
    return depth_show


# main loop
s = 0
done = False
while not done:
    # RGB and depth img
    rgb = get_rgb()
    depth = get_depth()

    # Display the stream syde-by-side
    cv2.imshow("RGB Image", rgb)
    cv2.imshow("Depth Image", depth)
    key = cv2.waitKey(1)

    # Read keystrokes
    if key == ord('q'):  # terminate
        print("Q key detected!")
        done = True
    elif key == ord('s'):  # screen capture
        print("s key detected. Saving image {}".format(s))
        cv2.imwrite("ex2_" + str(s) + '.png', rgb)
        # s+=1 # uncomment for multiple captures

# end while

# Release resources
cv2.destroyAllWindows()
rgb_stream.stop()
openni2.unload()
print("Terminated")
