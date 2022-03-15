import cv2
import numpy as np

def get_frame(cap, scaling_factor):
    # Read the current frame from the video capture object
    _, frame = cap.read()

    # Resize the image 
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    return frame


# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100, 
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize = (15, 15), 
                   maxLevel = 2, 
                   criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))



if __name__ == '__main__':
    #Define the video capture object
    cap = cv2.VideoCapture(0)

    # Define the scaling factor for the images
    scaling_factor = 0.5

    # Take first frame and find corners in it
    old_frame = get_frame(cap, scaling_factor)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_RGB2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    #print("p0\n"); 
    #print(p0);

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)

    count = 0; 

    # Keep reading the frames from the webcam until the user hits the 'ESC' key
    while True:
        # Grab the current frame
        frame = get_frame(cap, scaling_factor)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

#        print("p0 shape\n"); 
#        print(p0.shape)
#        print("good_new shape\n"); 
#        print(good_new.shape)
#        print("good_new old\n"); 
#        print(good_old.shape)

        # draw the tracks
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (int(a),int(b)), (int(c), int(d)), color[i].tolist(),2)
            frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

        img = cv2.add(frame,mask)

        cv2.imshow('frame', img)

        if (count == 500):
            print("Write files")
            cv2.imwrite("../../Image/old_frame.jpg", old_frame)
            cv2.imwrite("../../Image/frame.jpg", frame)

        count = count + 1

        old_gray = frame_gray.copy()
        old_frame = frame.copy()
        p0 = good_new.reshape(-1,1,2)


        # Check if the user hit the 'ESC' key
        c = cv2.waitKey(5)
        if c == 27:
            break

    # Close all the window
    cv2.destroyAllWindows()
    cap.release()
