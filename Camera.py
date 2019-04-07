import cv2
import numpy as np
x = 0
y = 0

lower_red = np.array([150, 100, 10])
upper_red = np.array([180, 255, 255])

cap = cv2.VideoCapture(0)

while cap:
    _, frame = cap.read()

    #bgr -> hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_red, upper_red)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    #rec = cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)

    #new code

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    #cv2.imshow("res", res)
    #cv2.imshow("Rectangle", rec)

    #escape to exit
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
