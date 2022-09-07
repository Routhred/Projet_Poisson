import os
import sys
import time
import numpy as np
import cv2

cap=cv2.VideoCapture(1)
#cap=cv2.VideoCapture("D:\\travail\\coach\\poisson\\poissons.mp4")

kernel_blur=5
seuil=15
surface=1000
surface_max = 10000
ret, originale=cap.read()
originale=cv2.cvtColor(originale, cv2.COLOR_BGR2GRAY)
originale=cv2.GaussianBlur(originale, (kernel_blur, kernel_blur), 0)
kernel = 9
kernel_dilate=np.ones((kernel, kernel), np.uint8)
count = 0
continuer = True
print("ok")
while continuer:
    count += 1
    ret, frame = cap.read()
    if count == 10:
        if ret :
            gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray=cv2.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
            mask=cv2.absdiff(originale, gray)
            mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)[1]
            kernel_erode = np.ones((4, 4), np.uint8)
            kernel_dilate = np.ones((6, 6), np.uint8)
            mask=cv2.erode(mask, kernel_erode, iterations=2)
            mask=cv2.dilate(mask, kernel_dilate, iterations=3)
            contours, nada=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            frame_contour=frame.copy()
            for c in contours:
                cv2.drawContours(frame_contour, [c], 0, (0, 255, 0), 5)
                if cv2.contourArea(c)<surface or cv2.contourArea(c)>surface_max:
                    continue
                x, y, w, h=cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                print(x+(w*0.5),y+(h*0.5))
            print('_____________________________________________')
            originale=gray
            cv2.putText(frame, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}  k {:d}".format(seuil, kernel_blur, surface,kernel), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
            cv2.imshow("frame", frame)
            cv2.imshow("contour", frame_contour)
            cv2.imshow("mask", mask)
            intrus=0
            key=cv2.waitKey(30)&0xFF
            if key==ord('q'):
                break
            if key==ord('p'):
                kernel_blur=min(43, kernel_blur+2)
            if key==ord('m'):
                kernel_blur=max(1, kernel_blur-2)
            if key==ord('i'):
                surface+=100
            if key==ord('k'):
                surface=max(100, surface-100)
            if key==ord('+'):
                surface_max+=1000
            if key==ord('-'):
                surface_max=max(1000, surface_max-1000)
            if key==ord('o'):
                seuil=min(255, seuil+1)
            if key==ord('l'):
                seuil=max(1, seuil-1)
            if key == ord('a'):
                kernel += 1
            if key == ord('z'):
                kernel = max(1, kernel - 1)
            if key==ord('c'):
                continuer = False
        count = 0
cap.release()
cv2.destroyAllWindows()