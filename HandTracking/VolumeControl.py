
import cv2
import time
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import math
import osascript





cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=0.8)



while True:
    success, img = cap.read()
    detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    #4 and 8 are thumb and index finger tip

    if len(lmList) != 0:
        #print(lmList[4],lmList[8])

        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]

        cv2.circle(img,(x1,y1),10,(0,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,0,255),cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2),(0,0,255),3)

        cx,cy = (x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(cx,cy),10,(0,0,255),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        #print(length)

        # if length<50:
        #     #cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
        #     osascript.run('set volume output volume 1')
        # elif 100>length>50:
        #     osascript.run('set volume output volume 25')
        # elif 150>length>200:
        #     osascript.run('set volume output volume 50')
        # elif 200>length>250:
        #     osascript.run('set volume output volume 75')
        # elif 250>length:
        #     osascript.run('set volume output volume 100')
        # cv2.waitKey(100)

        vol = int(np.interp(length,[30,300],[0,100]))
        print(vol,length)
        #osascript.run('set x to '+ str(vol))
        osascript.run('set volume output volume '+str(vol))
        cv2.waitKey(100)



    cv2. imshow('Webcam',img)
    cv2.waitKey(1)