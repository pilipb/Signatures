import autopy as autopy
import cv2
import time
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import math
import osascript
import pyautogui

import tkinter as tk
from PIL import ImageGrab

lastx, lasty = 0, 0


def xy(event):
    "Takes the coordinates of the mouse when you click the mouse"
    global lastx, lasty
    lastx, lasty = event.x, event.y


def addLine(event):
    """Creates a line when you drag the mouse
    from the point where you clicked the mouse to where the mouse is now"""
    global lastx, lasty
    canvas.create_line((lastx, lasty, event.x, event.y))
    # this makes the new starting point of the drawing
    lastx, lasty = event.x, event.y

def save(event):
    x=root.winfo_rootx()+canvas.winfo_x()
    y=root.winfo_rooty()+canvas.winfo_y()
    x1=x+canvas.winfo_width()
    y1=y+canvas.winfo_height()
    im = ImageGrab.grab((x, y, x1, y1))
    im.save("captured.png")

root = tk.Tk()
root.geometry("800x600")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = tk.Canvas(root)
canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", addLine)
root.bind("<Control-s>", save)





clocX,clocY = [0,0]
plocX,plocY = [0,0]

frameR = 100
wCam,hCam = 1280,720
wScr, hScr = autopy.screen.size()

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=0.8,maxHands=1)
tipIds = [4,8,12,16,20]
while True:
    root.mainloop()
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,0),2)
    plocX,plocY=clocX,clocY
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]


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
        #totalFingers = fingers.count(1)
        if fingers[1]==1 and fingers[0]==1:

            x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))
            #autopy.mouse.click()

            pyautogui.mouseDown(button='left')
            if int(wCam-x3) not in range(int(wScr)) or int(y3) not in range(int(hScr)):
                print('outside of bounds')
            else:
                autopy.mouse.move(wCam-x3,y3)
            #pyautogui.dragTo(wCam-x3,y3, button='left')

        if fingers[1]==1 and fingers[0]==0:

            x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))

            clocX,clocY=wCam-x3,y3

            if int(wCam-x3) not in range(int(wScr)) or int(y3) not in range(int(hScr)):
                print('outside of bounds')
            else:
                autopy.mouse.move(wCam-x3,y3)





                #pyautogui.mouseDown(button='left')

                # if fingers[0]==0:
                #    pyautogui.mouseUp(button='left')





                # autopy.mouse.toggle(None, 'down')
                # if fingers[0]==0:
                #     autopy.mouse.toggle(None, 'Down')

                # x1,y1 = lmList[8][1],lmList[8][2]
                # x2,y2 = lmList[12][1],lmList[12][2]
                # length = math.hypot(x2-x1,y2-y1)
                #
                # if length<45:
                #     cv2.circle(img,(x1,y1),10,(0,255,0),cv2.FILLED)
                #
                #     autopy.mouse.click()









    # GET THE TIP OF INDEX AND MIDDLE FINGERS
    # CHECK WHICH FINGERS ARE UP
    # ONLY INDEX FINGER; MOVING MODE
        #CONVERT COORDINATES



    #cv2.imshow("Image",img)
    cv2.waitKey(1)



