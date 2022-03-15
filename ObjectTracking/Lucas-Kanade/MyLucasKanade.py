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

    oldx = 320.0
    oldy = 180.0

    # print(p0)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)

    count = 0; 

    # Keep reading the frames from the webcam until the user hits the 'ESC' key
    while True:
        # Grab the current frame
        frame = get_frame(cap, scaling_factor)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        nWx = 15
        nWy = 15

        Gx = np.zeros([nWy,nWx], dtype=np.float32)
        Gy = np.zeros([nWy,nWx], dtype=np.float32)
        Gt = np.zeros([nWy,nWx], dtype=np.float32)
        A = np.zeros([2,2], dtype=np.float32)
        b = np.zeros([2,1], dtype=np.float32)
        x = np.zeros([2,1], dtype=np.float32)

        #print(old_gray.shape)
        #print("oldy", oldy)
        #print("oldx", oldx)

        p0x = int(oldx)
        p0y = int(oldy)



        for i in range(0,nWy):
            for j in range(0,nWx):
                Gx[i,j] =  float(frame_gray[p0y+i-1, p0x+j]) - float(frame_gray[p0y+i-1, p0x+j-2])/2.0
                Gy[i,j] = - float(frame_gray[p0y+i, p0x+j-1]) + float(frame_gray[p0y+i-2, p0x+j-1])/2.0
                Gt[i,j] = float(frame_gray[p0y+i-1, p0x+j-1]) - float(old_gray[p0y+i-1, p0x+j-1])

        #print("Gx: ", Gx)
        #print("Gy: ", Gy)
        #print("Gt: ", Gt)

        for i in range(0,nWy):
            for j in range(0,nWx):
                A[0,0] = A[0,0] + Gx[i,j]*Gx[i,j]
                A[0,1] = A[0,1] + Gx[i,j]*Gy[i,j]
                A[1,0] = A[1,0] + Gy[i,j]*Gx[i,j]
                A[1,1] = A[1,1] + Gy[i,j]*Gy[i,j]
                b[0,0] = b[0,0] - Gx[i,j]*Gt[i,j]
                b[1,0] = b[1,0] - Gy[i,j]*Gt[i,j]

        #print("A: ", A)
        #print("b: ", b)

        x = np.zeros([2,1])
        #x = np.linalg.lstsq(A,b, rcond=None)[0]

        #print("speed: ", x)

        #check = A@x

        #print("check: ", check)

        if np.abs(A[0,0]) > 0.0 and np.abs(A[1,0]) > 0.0:
            #print("Try to solve x")
            x = np.linalg.solve(A,b)
            print("x: ", x)
            newx = oldx + x[0,0]
            newy = oldy + x[1,0]
        else:
            print("Can't find x")
            newx = oldx
            newy = oldy

        a = int(newx)
        b = int(newy)
        c = int(oldx)
        d = int(oldy)

        #print("new: ", newx, newy)

        mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 10, color[i].tolist(), -1)

        img = cv2.add(frame,mask)

        cv2.imshow('frame', img)

        #if (count == 500):
        #    print("Write files")
        #    cv2.imwrite("../../Image/old_frame.jpg", old_frame)
        #    cv2.imwrite("../../Image/frame.jpg", frame)

        count = count + 1

        old_gray = frame_gray.copy()
        old_frame = frame.copy()
        oldx = newx
        oldy = newy

        # Check if the user hit the 'ESC' key
        c = cv2.waitKey(5)
        if c == 27:
            break

    # Close all the window
    cv2.destroyAllWindows()
    cap.release()
