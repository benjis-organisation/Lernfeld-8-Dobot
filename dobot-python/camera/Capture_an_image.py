import cv2

class FrameReadError(Exception):
    pass

# Funktion, um die Kamera zu initialisieren
def initialize_camera():
    cap = cv2.VideoCapture(0)
    return cap

# Funktion, um ein Bild zu erfassen
def capture_image(cap):

    cv2.namedWindow('Open Camera', cv2.WINDOW_NORMAL)

    for _ in range(2):
        ret, frame = cap.read()
        if not ret:
            raise FrameReadError("Failed to read frame")
        cv2.imshow('Open Camera', frame)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        exit(1)

    cv2.destroyWindow('Open Camera')

    cv2.imwrite('captured_image.jpg', frame)

    cv2.imshow('Image', frame)

    cv2.destroyAllWindows()