from PIL import ImageGrab
import win32gui
import time
import cv2 as cv
toplist, winlist = [], []
tableau_pixel_victoire=[150,300,170,305]    #carré où tester pour savoir qui a gagner
couleur_pixel_victoire=[247,81,0]            #couleur a chercher pour savoir qui a gagné
pixel_fin_couleur=[0,0,0,213,69,0]          #couleur des pixels_fin si le match est fini
pixel_fin_test=[0,0,0]               #ici on rentre la couleur des pixels_fin
pixel_fin=[(110,314),(198,110),(430,350)]#<--- changer ici les coordonnées des pixels a tester pour trouver la fin du match
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

win32gui.EnumWindows(enum_cb, toplist)
street = [(hwnd, title) for hwnd, title in winlist if 'snes' in title.lower()]
street = street[0]
hwnd = street[0]


def test_couleur2(a,b,c,d,couleur,image,mode):
    vrai=False
    color = 0
    couleur_reel=[0,0,0]
    test = False
    if mode=='one':
        for i in range(c-a):
            for j in range(d-b):
                try:
                    (couleur_reel[0],couleur_reel[1],couleur_reel[2]) = image.getpixel((a+i,b+j))
                    image.putpixel((a+i,b+j),(255,0,0))
                except:
                    print("erreur getpixel")
                if couleur_reel[0] !=0:
                    print(couleur_reel,couleur)
                if not(test_tableau([0,0,0],couleur_reel)):
                    if(test_tableau(couleur_reel,couleur)):
                        vrai=True
                        image.putpixel((a + i, b + j), (0, 255, 0))
        if vrai:
            color = 0
        else:
            color = 1
        image.show('imahge')
    elif mode == 'every':
        for i in range(c-a):
            for j in range(d-b):
                try:
                    (couleur_reel[0],couleur_reel[1],couleur_reel[2]) = image.getpixel((a+i,b+j))
                except:
                    print("erreur getpixel")
                if not(test_tableau([0,0,0],couleur_reel)):
                    test = True
        if not(test):
            vrai = True
    return vrai,color
def test_tableau(tab1,tab2):
    egal=True
    if (len(tab1)==len(tab2)):
        for i in range(len(tab1)):
            if (tab1[i]!=tab2[i]):
                egal=False
    else:
        print("impossible")
    return egal
def test_fin(couleur,pixel):
    fin = False
    #print("on test la fin")
    compteur = 0
    gagnant = 0
    rect = win32gui.GetWindowRect(hwnd)
    time.sleep(0.001)
    screen = ImageGrab.grab(rect)
    for i in range(3):
        try:
            (pixel_fin_test[0], pixel_fin_test[1], pixel_fin_test[2]) = screen.getpixel((pixel[i][0], pixel[i][1]))
            print(screen.getpixel((pixel[i][0], pixel[i][1])))
        except:
            print("erreur, getpixel")
        if (test_tableau(couleur, pixel_fin_test)):
            compteur += 1

    if compteur == 3:
        compteur = 0
        time.sleep(1)
        rect = win32gui.GetWindowRect(hwnd)
        time.sleep(0.001)
        screen = ImageGrab.grab(rect)
        for i in range(3):
            try:
                (pixel_fin_test[0], pixel_fin_test[1], pixel_fin_test[2]) = screen.getpixel(
                    (pixel_fin[i][0], pixel_fin[i][1]))
            except:
                print("erreur, getpixel")
            if (test_tableau([0, 0, 0], pixel_fin_test)):
                compteur += 1
        if compteur == 3:
            win, color = test_couleur(150, 298, 164, 312, couleur_pixel_victoire, screen)
            print("c'est la fin")
            fin = True
            if win:
                if color == 0:
                    gagnant = 0
                elif color == 1:
                    gagnant = 1
        #print(fin,gagnant)
    return fin, gagnant

win32gui.SetForegroundWindow(hwnd)
win32gui.SetForegroundWindow(hwnd)
rect = win32gui.GetWindowRect(hwnd)
screen = ImageGrab.grab(rect)
win, color = test_couleur(100, 310, 200, 330, couleur_pixel_victoire, screen,"one")

