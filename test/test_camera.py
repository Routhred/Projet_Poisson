import cv2 as cv
import os

def grille(image):
    done = False
    for offset in ((0,taille_y_case,2*taille_y_case)):
        for cox in range(480):
            for coy in range(taille_y_case+offset):
                if coy>offset:
                    if cox<taille_x_case:
                        image[coy][cox] = 120+offset
                    elif cox < 2*taille_x_case:
                        image[coy][cox] = 160+offset
                    else :
                        image[coy][cox] = 200+offset
    for cox in range(x_grille):
        for coy in range(y_grille):
            if cox < x_grille/2 :
                image[coy+off_y_grille][cox+off_x_grille] = 255
                done = True
            else :
                image[coy+off_y_grille][cox+off_x_grille] = 150
                done = True
    return image
cap1 = cv.VideoCapture(1)
#os.system("\"C:\\Users\\foxfa\\OneDrive\\Bureau\\poissons_corps\\Street Fighter 2 Turbo.smc\"")
print("ok")
while(1):
    print('ok')
    ret, frame = cap1.read()
    if ret:
        #frame = frame[130:400, 80:550]
        #frame = cv.resize(frame, (480, 360))
        cv.imshow('frame',frame)
        cv.waitKey(1)

