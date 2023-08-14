import cv2
import mediapipe as mp
import time
import numpy as np
from collections import deque

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

# define the upper and lower boundaries for a color to be considered "blue"
blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

# define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

# initialize deques to store different colors in different arrays
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]

# initialize an index variable for each of the colors
bindex = 0
gindex = 0
rindex = 0
yindex = 0

# colours in BGR format
colours = [(0, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (0, 255, 255, 255)]
colourIndex = 0

# create a blank white image
# get size of cap.read()
success, temp = cap.read()
xpix = temp.shape[0]
ypix = temp.shape[1]

paintWindow = np.zeros((xpix, ypix, 3)) + 255
# make paintWindow transparent
paintWindow = paintWindow.astype('uint8')
paintWindow = cv2.cvtColor(paintWindow, cv2.COLOR_BGR2BGRA)
paintWindow[:, :, 3] = 0

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    results = hands.process(imgRGB)

    # add the same paint interface to the camera feed captured through the webcam (for ease of usage)
    img = cv2.rectangle(img, (40, 1), (140, 65), (122, 122, 122), -1)
    img = cv2.rectangle(img, (160, 1), (255, 65), colours[0], -1)
    img = cv2.rectangle(img, (275, 1), (370, 65), colours[1], -1)
    img = cv2.rectangle(img, (390, 1), (485, 65), colours[2], -1)
    img = cv2.rectangle(img, (505, 1), (600, 65), colours[3], -1)
    cv2.putText(img, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

    # add a caption that says press 'q' to quit
    cv2.putText(img, "Press 'cmd q' to quit / 'cmd s' to save", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)

    # determine which pixels fall within the blue boundaries and then blur the binary image
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            # only draw if index finger is up
            if handLms.landmark[8].y < handLms.landmark[6].y:

                for id, lm in enumerate(handLms.landmark):
                    #print(id,lm)
                    h, w, c= img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)

                    if id==8:
                        cv2.circle(img, (cx,cy),25,(255,0,255),cv2.FILLED)

                        # if the finger is in the colour area, change the colour
                        if 40 <= cx <= 140: # Clear All
                            bpoints = [deque(maxlen=512)]
                            gpoints = [deque(maxlen=512)]
                            rpoints = [deque(maxlen=512)]
                            ypoints = [deque(maxlen=512)]

                            bindex = 0
                            gindex = 0
                            rindex = 0
                            yindex = 0

                            paintWindow[67:, :, :] = 255
                        if cx > 160 and cx < 255 and cy > 1 and cy < 65: # black
                            colourIndex = 0
                        elif cx > 275 and cx < 370 and cy > 1 and cy < 65: # Green
                            colourIndex = 1
                        elif cx > 390 and cx < 485 and cy > 1 and cy < 65: # Red
                            colourIndex = 2
                        elif cx > 505 and cx < 600 and cy > 1 and cy < 65: # Yellow
                            colourIndex = 3

                        if colourIndex == 0:
                            bpoints[bindex].appendleft((cx, cy))
                        elif colourIndex == 1:
                            gpoints[gindex].appendleft((cx, cy))
                        elif colourIndex == 2:
                            rpoints[rindex].appendleft((cx, cy))
                        elif colourIndex == 3:
                            ypoints[yindex].appendleft((cx, cy))

            # if the finger is not up, clear the points
            else:
                bpoints.append(deque(maxlen=512))
                bindex += 1
                gpoints.append(deque(maxlen=512))
                gindex += 1
                rpoints.append(deque(maxlen=512))
                rindex += 1
                ypoints.append(deque(maxlen=512))
                yindex += 1


            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # draw lines of all the colors (Blue, Green, Red and Yellow)
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(img, points[i][j][k - 1], points[i][j][k], colours[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colours[i], 2)

    cv2.imshow("Image", img)
    cv2.imshow("Paint", paintWindow)

    cv2.waitKey(1)

    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    if cv2.waitKey(1) & 0xFF == ord("s"):
        cv2.imwrite("signature.png", paintWindow)
        break

# cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()