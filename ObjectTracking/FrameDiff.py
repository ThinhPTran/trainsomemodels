import cv2

# Compute the frame differences
def frame_diff(prev_frame, cur_frame, next_frame):
    # Difference between the current frame and the next frame
    diff_frames_1 = cv2.absdiff(next_frame, cur_frame)
    # Difference between the current frame and the previous frame
    diff_frames_2 = cv2.absdiff(cur_frame, prev_frame)

    # Compute the bitwise-AND between the two difference frames and return it.
    return cv2.bitwise_and(diff_frames_1, diff_frames_2)

# Define a function to grab the current frame from the webcam.
def get_frame(cap, scaling_factor):
    # Read the current frame from the video capture object
    _, frame = cap.read()
    # Resize the frame based on the scaling factor and return it.
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    # Convert the image to grayscale and return it
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    return gray

if __name__=='__main__':

    # Define the video capture object
    cap = cv2.VideoCapture(0)

    # Define the scaling factor for the images
    scaling_factor = 0.5

    # Grab the current frame
    prev_frame = get_frame(cap, scaling_factor)
    cur_frame = get_frame(cap, scaling_factor)
    next_frame = get_frame(cap, scaling_factor)

    # Keep reading the frames from the webcam until the user hits the 'ESC' key
    while True:
        # Display the frame difference
        cv2.imshow('Object Movement', frame_diff(prev_frame, cur_frame, next_frame))

        # Update the frame variables
        prev_frame = cur_frame
        cur_frame = next_frame
        next_frame = get_frame(cap, scaling_factor)

        # Check if the user hit the 'Esc' key
        key = cv2.waitKey(10)
        if key == 27:
            break


    # Close all the windows
    cv2.destroyAllWindows()
