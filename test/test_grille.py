import cv2 as cv
hauteur = 360
largeur = 480
hauteur_case = hauteur//2
largeur_case = largeur//5
x_grille = 220
y_grille = 160
off_x_grille = 130
off_y_grille = 100
taille_y_case = hauteur//3
taille_x_case = largeur//3

cap = cv.VideoCapture(1)
i = 0
count = 0
ret, frame = cap.read()

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

#i+=1
if ret:
    frame = frame[130:400, 80:550]
    frame = cv.resize(frame, (480, 360))
    frame = grille(frame)
    cv.imshow('frame',frame)
    cv.waitKey(0)