import imutils
import numpy as np
import cv2

from pixelsortcv import pixelsort

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = imutils.auto_canny(gray, sigma=0.99)
    frame = pixelsort(frame, interval_function="none")  # , interval_function="threshold", lower_threshold=0.5)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
