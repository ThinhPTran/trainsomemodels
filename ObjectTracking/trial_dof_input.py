from email.mime import image
import cv2 as cv
import numpy as np
from PIL import Image

# The video feed is read in as a VideoCapture object
# cap = cv.VideoCapture("trial_1.mp4")
image_pr = cv.imread('image_pr.png')
#Use input = 0 if you want to use input directly from your webcam
#cap = cv.VideoCapture(0)
# ret = a boolean return value from getting the frame, first_frame = the first frame in the entire video sequence
# ret, first_frame = image_pr.read()
# Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
prev_gray = cv.cvtColor(image_pr, cv.COLOR_BGR2GRAY)
# Creates an image filled with zero intensities with the same dimensions as the frame
mask = np.zeros_like(image_pr)
# Sets image saturation to maximum
mask[..., 1] = 255

#while(cap.isOpened()):
image_cr = cv.imread('image_cr.png')
# ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
# ret, frame = image_cr.read()
# Opens a new window and displays the input frame
# Converts each frame to grayscale - we previously only converted the first frame to grayscale
gray = cv.cvtColor(image_cr, cv.COLOR_BGR2GRAY)
cv.imshow("current image", gray)
cv.waitKey(0)
cv.destroyAllWindows()
# Calculates dense optical flow by Farneback method
# https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowfarneback
flow = cv.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
# Computes the magnitude and angle of the 2D vectors
magnitude, angle = cv.cartToPolar(flow[..., 0], flow[..., 1])
# Sets image hue according to the optical flow direction
mask[..., 0] = angle * 180 / np.pi / 2
# Sets image value according to the optical flow magnitude (normalized)
mask[..., 2] = cv.normalize(magnitude, None, 25, 255, cv.NORM_MINMAX)
# Converts HSV to RGB (BGR) color representation
rgb = cv.cvtColor(mask, cv.COLOR_HSV2BGR)
#rgb.shape
#cv.imwrite('image_dof.png',rgb[:9446400].reshape(820, 1920))
cv.imshow("DOF output", rgb)
cv.waitKey(0)
cv.destroyAllWindows()
# Opens a new window and displays the output frame
# cv.imshow("dense optical flow", rgb)
# Frames are read by intervals of 1 millisecond. The programs breaks out of the while loop when the user presses the 'q' key

# cv.destroyAllWindows()