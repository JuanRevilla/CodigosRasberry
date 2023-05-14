#

import cv2
import numpy as np
from leejson import extraexy
from cotrol import muevebola
paso = 0
x, y = extraexy('positions.json')


# define the minimum and maximum HSV values for the ball color
# you can adjust these values based on your ball color
lower_hsv = np.array([0, 100, 100])
upper_hsv = np.array([20, 255, 255])

# set up the camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# load the chessboard image and define the size of the chessboard
chessboard = cv2.imread('chessboard.png')
chessboard_size = (7, 7)

# find the corners of the chessboard
ret, corners = cv2.findChessboardCorners(cv2.cvtColor(chessboard, cv2.COLOR_BGR2GRAY), chessboard_size, None)

# set up the calibration parameters
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
obj_points = np.zeros((np.prod(chessboard_size), 3), np.float32)
obj_points[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
img_points = corners.reshape(-1, 2)

# calibrate the camera
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([obj_points], [img_points], chessboard.shape[:-1], None, None)

# start capturing frames from the camera
while True:
    # read a frame from the camera
    ret, frame = camera.read()
    
    # undistort the frame using the calibration parameters
    undistorted = cv2.undistort(frame, mtx, dist, None)
    
    # convert the frame to HSV color space
    hsv = cv2.cvtColor(undistorted, cv2.COLOR_BGR2HSV)
    
    # threshold the frame to get the binary mask for the ball
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    
    # find contours in the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # if there is at least one contour, track the ball
    if len(contours) > 0:
        # find the largest contour
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        
        # compute the centroid of the largest contour
        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        paso=muevebola(cx,cy,x[paso],y[paso])

        # draw a circle at the centroid of the ball
        cv2.circle(undistorted, (cx, cy), 10, (0, 255, 0), -1)
        
    # display the frame
    cv2.imshow('frame', undistorted)
    
    # wait for a key press and check if it's the ESC key
    if cv2.waitKey(1) == 27:
        break


# release the camera and close the window
camera.release()
cv2.destroyAllWindows()