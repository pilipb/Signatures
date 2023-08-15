import cv2
import mediapipe as mp
import numpy as np
from collections import deque
from pathlib import Path

'''
This script allows you to draw with your finger on the screen. The line drawing can then be saved as a png image or cleared.

'''

def mainloop():

    downloads_path = str(Path.home() / "Downloads")

    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    # initialize deques to store line
    bpoints = [deque(maxlen=512)]

    # initialize an index variable for each of the colors
    bindex = 0

    # colours in BGRA format
    colour = (0, 0, 0, 255)

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
        if not success:
            raise Exception("Could not get frame")

        img = cv2.flip(img, 1)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        results = hands.process(imgRGB)

        # add the same paint interface to the camera feed captured through the webcam (for ease of usage)
        img = cv2.rectangle(img, (40, 70), (140, 135), (0,0,255), -1)
        cv2.putText(img, "CLEAR ALL", (49, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # add a caption that says press 'q' to quit 's' to save in a box at the top of the screen in large font
        img = cv2.rectangle(img, (0, 0), (ypix, 70), (122, 122, 122), -1)
        cv2.putText(img, "Press 'q' to quit, 's' to save to downloads", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.7, (0, 0, 0), 2, cv2.LINE_AA)

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
                                bindex = 0
                                paintWindow[:, :, :] = 255

                            bpoints[bindex].appendleft((cx, cy))

                # if the finger is not up, clear the points
                else:
                    bpoints.append(deque(maxlen=512))
                    bindex += 1
                
                # show the hand on the camera feed
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        # draw lines
        points = bpoints
        for i in range(len(points)):
            for j in range(1, len(points[i])):
                if points[i][j - 1] is None or points[i][j] is None:
                    continue
                cv2.line(img, points[i][j - 1], points[i][j], colour, 5)
                cv2.line(paintWindow, points[i][j - 1], points[i][j], colour, 5)

        # if the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if cv2.waitKey(1) & 0xFF == ord("s"):
            # save image to downloads folder
            cv2.imwrite(downloads_path + "/signature.png", paintWindow)
            # TODO: copy image to clipboard ???
            break

        cv2.imshow("Image", img)
        cv2.imshow("Paint", paintWindow)

        cv2.waitKey(1)

    # cleanup the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mainloop()