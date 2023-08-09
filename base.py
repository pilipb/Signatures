import numpy as np
import cv2
from collections import deque

'''
this script is based on a tutorial from pyimagesearch.com

the script is used to track a blue object and draw on the screen with this object onto a canvas.

Next steps TODO:
- define hand tracking for drawing using fingertip
- define hand tracking for erasing using fist
- define hand tracking for changing color using thumb
- export drawing as image (png trace)
- create GUI 
- package as executable



'''

# initialise variables

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

colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colourIndex = 0

# create a blank white image
paintWindow = np.zeros((471, 636, 3)) + 255

# draw buttons like colored rectangles on the white image
paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colours[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), colours[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colours[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colours[3], -1)

# label the buttons
cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# load the video
camera = cv2.VideoCapture(0)

# keep looping
while True:
    # grab the current paintWindow
    (grabbed, frame) = camera.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # check to see if we have reached the end of the video
    if not grabbed:
        break

    # add the same paint interface to the camera feed captured through the webcam (for ease of usage)
    frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
    frame = cv2.rectangle(frame, (160, 1), (255, 65), colours[0], -1)
    frame = cv2.rectangle(frame, (275, 1), (370, 65), colours[1], -1)
    frame = cv2.rectangle(frame, (390, 1), (485, 65), colours[2], -1)
    frame = cv2.rectangle(frame, (505, 1), (600, 65), colours[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

    # determine which pixels fall within the blue boundaries and then blur the binary image
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # find contours in the image
    (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # check to see if any contours were found
    if len(cnts) > 0:

        # sort the contours and find the largest one -- we will assume this contour correspondes to the area of the bottle cap
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)

        # draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

        # get the moments to calculate the center of the contour (in this case Circle)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        # check if any button has been pressed on the paint window
        if center[1] <= 65:
            if 40 <= center[0] <= 140:
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                bindex = 0
                gindex = 0
                rindex = 0
                yindex = 0

                paintWindow[67:, :, :] = 255
            elif 160 <= center[0] <= 255:
                colourIndex = 0
            elif 275 <= center[0] <= 370:
                colourIndex = 1
            elif 390 <= center[0] <= 485:
                colourIndex = 2
            elif 505 <= center[0] <= 600:
                colourIndex = 3
        else:
            if colourIndex == 0:
                bpoints[bindex].appendleft(center)
            elif colourIndex == 1:
                gpoints[gindex].appendleft(center)
            elif colourIndex == 2:
                rpoints[rindex].appendleft(center)
            elif colourIndex == 3:
                ypoints[yindex].appendleft(center)
    # append the next deque when no contours are detected (i.e., bottle cap reversed)
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1

    # draw lines of all the colors (Blue, Green, Red and Yellow)
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colours[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colours[i], 2)

    # show the frame and the paintWindow image
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

