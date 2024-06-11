import cv2
import time

class FrameReadError(Exception):
    pass

def initialize_camera():
     # Initialize the camera
    cap = cv2.VideoCapture(0)
    return cap

def capture_image(cap):
    # Create a window
    
    cv2.namedWindow('Open Camera', cv2.WINDOW_NORMAL)

    # Display the window for 10 seconds
    for _ in range(2):
        ret, frame = cap.read()
        if not ret:
            raise FrameReadError("Failed to read frame")
        cv2.imshow('Open Camera', frame)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    
    # Capture an image
    ret, frame = cap.read()

    # Check if the image capture was successful
    if not ret:
        print("Failed to capture image")
        exit(1)

    # Close the window
    cv2.destroyWindow('Open Camera')

    # Save the image
    cv2.imwrite('captured_image.jpg', frame)

    # Display the image
    cv2.imshow('Image', frame)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()