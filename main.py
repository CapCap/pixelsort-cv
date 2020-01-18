import imutils
import numpy as np
import cv2

from pixelsortcv import pixelsort

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # print(frame.shape) # (720, 1280, 3)

    # frame = pixelsort(frame, interval_function="none")  # , interval_function="threshold", lower_threshold=0.5)

    window_size = 25
    i = 0
    for x in range(0, frame.shape[0], window_size):
        #i += 1
        for y in range(0, frame.shape[1], window_size):
            frame[x:x + window_size, y:y + window_size].sort(i % 2 == 0)
            i += 1

    window_size *= 2
    i = 0
    for x in range(0, frame.shape[0], window_size):
        i += 1
        for y in range(0, frame.shape[1], window_size):
            frame[x:x + window_size, y:y + window_size].sort(i % 2 == 0)
            i += 1

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
