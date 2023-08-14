import cv2
import time
import os
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=0.8)

tipIds = [4,8,12,16,20]




while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!= 0:
        fingers = []

        #thumb on right hand atm
        if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #fingers
        for id in range(1,5):

            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)


        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
        cv2.putText(img,str(totalFingers),(20,225),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),15)







    cv2.imshow("Image",img)
    cv2.waitKey(1)

