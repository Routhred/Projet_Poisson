from PIL import ImageGrab
import win32gui
import time
import numpy as np
import cv2 as cv
toplist, winlist = [], []
tableau_pixel_victoire=[150,298,164,312]    #carré où tester pour savoir qui a gagner
couleur_pixel_victoire=[74,73,74]            #couleur a chercher pour savoir qui a gagné
pixel_fin_couleur=[0,0,0,213,69,0]          #couleur des pixels_fin si le match est fini
pixel_fin_test=[0,0,0]               #ici on rentre la couleur des pixels_fin
pixel_fin=[(61,314),(288,197),(37,175)]
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


i = 0
cap = cv.VideoCapture(1)
ret, frame = cap.read()
frame = frame[130:400, 80:550]
frame = cv.resize(frame, (480, 360))
cv.imshow('frame',frame)
cv.waitKey(1)
win32gui.EnumWindows(enum_cb, toplist)
fish = [(hwnd, title) for hwnd, title in winlist if 'frame' in title.lower()]
fish = fish[0]
hwnd = fish[0]
win32gui.SetForegroundWindow(hwnd)
rect = win32gui.GetWindowRect(hwnd)
while(1):
    ret, frame = cap.read()
    if ret:
        frame = frame[130:400, 80:550]
        frame = cv.resize(frame, (480, 360))
        cv.imshow('frame',frame)
        cv.waitKey(1)
        rect = win32gui.GetWindowRect(hwnd)
        screen = ImageGrab.grab(rect)
        image = np.array(screen)
        image = image[32:-9,9:-9]
        image = image[:, :, ::-1].copy()
        cv.imshow('image',image)
        cv.waitKey(1)
