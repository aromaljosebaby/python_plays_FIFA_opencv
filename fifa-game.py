import numpy as np
import cv2
import imutils
import time
from imutils.video import VideoStream
from direct_keys_for_other_guy_proj import PressKey,W, A,S, D, Space, ReleaseKey,X,C
import time
import pyautogui

time_c=[]

cam = VideoStream(src=0).start()
currentKey = list()

time.sleep(3)

while True:

    t_now=time.time()
    key = False

    img = cam.read()
    img = np.flip(img, axis=1)  # so that it wont look like mirror
    img = imutils.resize(img, width=700)
    img = imutils.resize(img, height=480)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    value = (11, 11)
    blurred = cv2.GaussianBlur(hsv, value, 0)
    colourLower = np.array([83, 100, 80])
    colourUpper = np.array([104, 255, 255])

    height = img.shape[0]
    width = img.shape[1]

    mask = cv2.inRange(blurred, colourLower, colourUpper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    leftContour = mask[ 0:height, 0:190]   #0:height, 0:190
    rightContour = mask[30:450, 210:630] # 0:height, 210:630

    cnts_left = cv2.findContours(leftContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_left = imutils.grab_contours(cnts_left)

    cnts_right = cv2.findContours(rightContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_right = imutils.grab_contours(cnts_right)




    if len(cnts_right) > 0:   # this is for the movement section

        c = max(cnts_right, key=cv2.contourArea)


        c = c.T
        c[0][0] += 210   # we do this because wrt to right contour portion its 0 cord is 210 after the real img coord so we have to add 210 to get the real img coord

        c[1][0]+=30  # we are adding 30 to all y coordinate of right contours because since the right contour region starts from y coord 30 its 0 value is axsually 30 in real img coord , so we hav e to add 30 to riaght contour values to get real img coord

        c = c.T  # bringing back the original contour matrix


        M = cv2.moments(c)
        try:
            cX = int(M["m10"] / (M["m00"]))
            cY = int(M["m01"] / M["m00"])


        except:
            cX=390
            cY=190

        #print(cX,cY)

        cv2.drawContours(img, c, -1, (0, 230, 255), 3)
        cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)

        if cX > 210 and cX<350:  # left most half
            if  cY >310:  # down left region
                PressKey(A)
                PressKey(S)

                ReleaseKey(W)
                ReleaseKey(D)


            elif  cY>170:  # left region
                PressKey(A)

                ReleaseKey(W)
                ReleaseKey(S)
                ReleaseKey(D)

                '''key = True
                currentKey.append(A)'''


            else:
                PressKey(W)  # left up region
                PressKey(A)

                ReleaseKey(S)
                ReleaseKey(D)

                '''key = True
                currentKey.append(W)
                currentKey.append(A)'''

        elif cX > 350 and cX<490:  # middle vertical zone

            if cY > 310:  # down region
                PressKey(S)

                ReleaseKey(W)
                ReleaseKey(D)
                ReleaseKey(A)

                '''key = True
                currentKey.append(S)'''

            elif cY > 170:  # middle button ( so dont do anything )
                ReleaseKey(W)
                ReleaseKey(D)
                ReleaseKey(A)
                ReleaseKey(S)

            else:
                PressKey(W)  # up region

                ReleaseKey(A)
                ReleaseKey(D)
                ReleaseKey(S)



        else:  # right most half in movement section

            if cY > 310:  # down right region
                PressKey(S)
                PressKey(D)

                ReleaseKey(A)
                ReleaseKey(W)



            elif cY > 170:  # right region
                PressKey(D)

                ReleaseKey(W)
                ReleaseKey(A)
                ReleaseKey(S)



            else:     # right up region
                PressKey(W)
                PressKey(D)

                ReleaseKey(A)
                ReleaseKey(S)

                '''key = True
                currentKey.append(W)
                currentKey.append(D)'''


    if len(cnts_left) > 0:  # pass n shoot section

        c = max(cnts_left, key=cv2.contourArea)

        M = cv2.moments(c)
        try:
            cX = int(M["m10"] / (M["m00"]))
            cY = int(M["m01"] / M["m00"])
        except:
            cX = 390
            cY = 190

        cv2.drawContours(img, c, -1, (0, 230, 255), 3)
        cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)

        if cX <170 and cX >30 :  #  then maybe one of the shoot or pass is pressed

            if cY<190 and cY>50:  # pass
                print('pass')



                PressKey(C)


                key = True
                currentKey.append(C)
            elif cY<430 and cY>290:   # shoot

                print('shoot')



                PressKey(X)


                key = True
                currentKey.append(X)



    '''img = cv2.rectangle(img, (0, 0), (width // 2 - 40, height // 2), (0, 255, 0), 1)
    cv2.putText(img, 'LEFT', (110, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

    img = cv2.rectangle(img, (width // 2 + 40, 0), (width - 2, height // 2), (0, 255, 0), 1)
    cv2.putText(img, 'RIGHT', (440, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

    img = cv2.rectangle(img, (2 * (width // 5), 3 * (height // 4)), (3 * width // 5, height), (0, 255, 0), 1)
    cv2.putText(img, 'NITRO', (2 * (width // 5) + 20, height - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))'''

    #img=cv2.circle(img,(190,290),180,(0,255,0),2)

    #img = cv2.circle(img, (190, 290), 180, (0, 255, 0), 2)
    #img = cv2.circle(img, (500, 120), 100, (0, 255, 0), 2)
    #img = cv2.circle(img, (500, 360), 100, (0, 255, 0), 2)

    # up and down
    #cv2.rectangle(img, (370, 50), (450, 130), (0, 255, 0), 2)  # 80
    #cv2.rectangle(img, (370, 350), (450, 430), (0, 255, 0), 2)

    # right and left
    #cv2.rectangle(img, (240, 190), (320, 270), (0, 255, 0), 2)  # 80
    #cv2.rectangle(img, (370, 350), (450, 430), (0, 255, 0), 2)

    img = cv2.line(img, (190, 0), (190, 480), (0, 255, 0), 1)

    img=cv2.rectangle(img, (210, 30), (630, 450), (0,0, 0), 2)
    img=cv2.line(img, (350, 30), (350, 450), (0, 255, 0), 2)
    img=cv2.line(img, (490, 30), (490, 450), (0, 255, 0), 2)
    img=cv2.line(img, (210, 170), (630, 170), (0, 255, 0), 2)
    img=cv2.line(img, (210, 310), (630, 310), (0, 255, 0), 2)

    img = cv2.circle(img, (100, 120), 70, (83, 70, 39), -1)
    img = cv2.circle(img, (100, 360), 70, (143, 157, 42), -1)

    cv2.putText(img, 'PASS', (60,130), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
    cv2.putText(img, 'SHOOT', (45, 370), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))








    if not key and len(currentKey) != 0:
        for current in currentKey:
            ReleaseKey(current)
        currentKey = list()

    key = cv2.waitKey(1) & 0xFF
    cv2.imshow("Steering", img)
    time_c.append(time.time()-t_now)

    if key == ord("q"):
        break

cam.stop()
cv2.destroyAllWindows()

print(np.mean(time_c))