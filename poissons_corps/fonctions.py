#------------------------import-------------------------------
import pyautogui
from PIL import ImageGrab
from PIL.Image import *
import cv2 as cv
import numpy as np
import pygame
import time
import win32gui
import os
#-------------------------------------------------------------
#------------------------variables----------------------------
#pyautogui.KEYBOARD_KEYS
affichage_score = [pygame.image.load('score\\zero.png'),
                   pygame.image.load('score\\un.png'),
                   pygame.image.load('score\\deux.png'),
                   pygame.image.load('score\\trois.png'),
                   pygame.image.load('score\\quattre.png'),
                   pygame.image.load('score\\cinq.png'),
                   pygame.image.load('score\\six.png'),
                   pygame.image.load('score\\sept.png'),
                   pygame.image.load('score\\huit.png'),
                   pygame.image.load('score\\neuf.png')]
x_score=[110,174,590,654]
y_score=415
#Images :
frame_vide = cv.imread("test.png", cv.IMREAD_UNCHANGED)
bg = pygame.image.load('score\\score.png')
cap = cv.VideoCapture(0)
#dictionnaire:
tableau_touches = {"rouge" : [['b','x'],['r','z','l'],['q',0,'d'],['a','s','y']],
                   "noir" : [['3','9'],['p','8','m'],['4',0,'6'],['1','2','9']]}
dico_touches={"rouge":[1,2],
              "noir":[1,2]}
dico_nouveau = {"rouge": [[1, 2], [3, 4]],
                "noir": [[1, 2], [3, 4]]}
#Variables_tailles:
hauteur = 360
largeur = 480
hauteur_case = hauteur//2
largeur_case = largeur//5
#pixel
tableau_pixel_victoire=[150,298,164,312]    #carré où tester pour savoir qui a gagner
couleur_pixel_victoire=[247,81,0]            #couleur a chercher pour savoir qui a gagné
pixel_fin_couleur=[0,0,0,213,69,0]          #couleur des pixels_fin si le match est fini
pixel_fin_test=[0,0,0]               #ici on rentre la couleur des pixels_fin
pixel_fin=[(80,314),(198,110),(430,350)]#<--- changer ici les coordonnées des pixels a tester pour trouver la fin du match
#taille_grille:
x_grille = 220
y_grille = 160
off_x_grille = 130
off_y_grille = 100
taille_y_case = hauteur//3
taille_x_case = largeur//3
#touches:
starta = "f"
startb = "h"
anciennes_touches=['a','b','c','d']
nouvelles_touches=['a','b','c','d']
#win32gui:
toplist, winlist = [], []
pyautogui.FAILSAFE = False
#video
#vidcap = cv.VideoCapture("IMG_4674.MOV")
#success,image = vidcap.read()
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

win32gui.EnumWindows(enum_cb, toplist)
kernel_blur=5
kernel_dilate=np.ones((5, 5), np.uint8)
count = 0
#-------------------------------------------------------------
#------------------------fonctions----------------------------
#""""""""""""""""""""""""""""""""""""""""""""""""""""
def init():
    #pyautogui.hotkey('alt','tab')
    press('f')
    time.sleep(5)
    suite_touches(['s','s','f','s','d','f'])
    time.sleep(2)
    suite_touches(['f','s','f','s','f'])
def initVariables():
    image, originale = recuperer_image()
    fond = image
    screen = init_score(bg)
    running = True
    score = [0, 0]
    return fond,screen,running,score
def press(a):
    pyautogui.keyDown(a)
    time.sleep(0.2)
    pyautogui.keyUp(a)
    #print(a)
def suite_touches(tab):
    for i in range(len(tab)):
        press(tab[i])
        time.sleep(0.5)
    return 0
#"""""""""""""""""""""""""""""""""""""""""""""""""""
def afficher_score(score,screen):
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    numero_score=[int(score[0]/10),score[0]-(score[0]//10)*10,int(score[1]//10),score[1]-(score[1]//10)*10]
    for i in range(4):
        afficher = affichage_score[numero_score[i]]
        screen.blit(afficher,(x_score[i],y_score))
        pygame.display.flip()
#""""""""""""""""""""""""""""""""""""""""""""""""""""
def recuperer_image():
    global cap
    ret,image = cap.read()
    if not(ret):
        while not(ret):
            cap = cv.VideoCapture(1)
            ret, image = cap.read()
    image = cv.resize(image, (480, 360))
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
    return gray,image
#""""""""""""""""""""""""""""""""""""""""""""""""""""
def imageToDico(image,ij,fond,originale):
    dico = retourne_dico(image, 4, fond,ij,originale)
    #print("dico = ",dico)
    dico_touches = dico_to_touches(dico)
    return dico, dico_touches
def dico_to_touches(dico):
    # sourcery skip: hoist-statement-from-if, merge-nested-ifs
    for couleur in ("rouge","noir"):
        for index in range(2):
            cox = dico[couleur][index][1]
            coy = dico[couleur][index][0]
            #test cases milieu
            done = False
            if cox < off_x_grille + x_grille and cox > off_x_grille :
                if coy < off_y_grille + y_grille and coy > off_y_grille :
                    if cox < 240 :
                        dico_touches[couleur][index] = tableau_touches[couleur][0][0]
                        done = True
                    else :
                        dico_touches[couleur][index] = tableau_touches[couleur][0][1]
                        done = True
            if not(done):
                #test cases autres
                cox = cox//taille_x_case
                coy = coy//taille_y_case
                dico_touches[couleur][index] = tableau_touches[couleur][coy+1][cox]
                done = True
    return dico_touches
def retourne_dico(image,n,fond,ij,originale):

    mask, tableau_poisson = create_mask(image, 1, fond,originale)
    #tableau_poissons = trouver_groupe(poissonx, poissony, n)
    dico_nouveau, _ = remplir_tableau_poisson(tableau_poisson, originale,ij)

    return dico_nouveau
def create_mask(image,pas,fond,originale):
    tableau_poisson = [[0,0],[0,0],[0,0],[0,0]]
    index_tableau = 0
    #cv.imshow('fond ', fond)
    #cv.waitKey(1)
    mask = cv.absdiff(fond, image)
    mask = cv.threshold(mask, 17, 255, cv.THRESH_BINARY)[1]
    kernel_erode = np.ones((4, 4), np.uint8)
    kernel_dilate = np.ones((9, 9), np.uint8)
    mask = cv.erode(mask, kernel_erode, iterations=2)
    mask = cv.dilate(mask, kernel_dilate, iterations=3)
    contours, nada = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    frame_contour = originale.copy()
    for c in contours:
        cv.drawContours(frame_contour, [c], 0, (0, 255, 0), 5)
        if cv.contourArea(c) < 600 or cv.contourArea(c) > 10000:
            continue
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(originale, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.rectangle(originale, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if index_tableau <4:
            tableau_poisson[index_tableau][0] = x+(w/2)
            tableau_poisson[index_tableau][1] = y+(h/2)
            #print(tableau_poisson[index_tableau][0],tableau_poisson[index_tableau][1])
        index_tableau += 1
    cv.imshow('image_cadré', originale)
    cv.waitKey(1)

    #cv.imshow("mask",mask)
    #cv.waitKey(1)
    return mask,tableau_poisson
def remplir_tableau_poisson(tableau_poissons,image,ij):
    index_poisson = 0
    index_noir = 0
    index_rouge = 0
    for poisson in tableau_poissons:
        #print(poisson)
        hs, ss, vs = 0, 0, 0
        rs, gs ,bs = 0, 0, 0
        for i in range(10):
            for j in range(10):
                r, g, b = image[int(poisson[1]) - (i*1)][int(poisson[0]) - (j*1)]
                h, s, v = rgb_to_hsv(r, g, b)
                hs = hs + h
                ss = ss + s
                vs = vs + v
                rs = rs + r
                gs = gs + g
                bs = bs + b
        #print(hs // 100, ss // 100, vs // 100)
        #print(rs // 100, gs // 100, bs // 100)
        if vs // 100 < 50:
            #print(f"poisson bleu en {int(poisson[0])} {int(poisson[1])}")
            poisson_couleur = True
            if index_noir == 0:
                dico_nouveau["noir"][index_noir][0] = int(poisson[1])
                dico_nouveau["noir"][index_noir][1] = int(poisson[0])
                index_noir += 1
            else:
                dico_nouveau["noir"][index_noir][0] = int(poisson[1])
                dico_nouveau["noir"][index_noir][1] = int(poisson[0])
        else:
            #print(f"poisson rouge en {int(poisson[0])} {int(poisson[1])}")
            poisson_couleur = False
            if index_rouge == 0:
                dico_nouveau["rouge"][index_rouge][0] = int(poisson[1])
                dico_nouveau["rouge"][index_rouge][1] = int(poisson[0])
                index_rouge += 1
            else:
                dico_nouveau["rouge"][index_rouge][0] = int(poisson[1])
                dico_nouveau["rouge"][index_rouge][1] = int(poisson[0])
        #print(index_noir, index_rouge)
        """b = int(poisson[0])
        a = int(poisson[1])
        if poisson_couleur:
            couleur = [0, 0, 255]
        else:
            couleur = [255, 0, 0]
        image[a][b] = couleur
        image[a + 1][b] = couleur
        image[a - 1][b] = couleur
        image[a][b + 1] = couleur
        image[a][b - 1] = couleur"""
        index_poisson += 1
    #cv.imwrite(f"D:\\travail\\coach\\poisson\\poissons\\image_grille{ij}.jpg",image)
    #print("dico nouveau = ", dico_nouveau)
    return dico_nouveau,image
def trouver_groupe(f,g,n):
    data_set = np.dstack((f,g))
    data_set = data_set[0]
    model = KMeans(n).fit(data_set)
    return model.cluster_centers_
def soustraire_couleur_test(couleur_1,couleur_2,seuil):
    egal = False
    for i in range(3):
        if int(couleur_1[i])-int(couleur_2[i]) > seuil:
            egal = True
    return egal
def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    h = 0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if df == 0:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v
#""""""""""""""""""""""""""""""""""""""""""""""""""""
def position_to_choix_perso(couleur,dico):
    position_largeur=dico[couleur][0][1]//largeur_case
    position_hauteur=dico[couleur][1][0]//hauteur_case
    if (couleur=="rouge"):
        tab_largeur=[['d']*position_largeur]
        tab_hauteur=[['s']*position_hauteur]
    else:
        tab_largeur=[['6']*position_largeur]
        tab_hauteur=[['2']*position_hauteur]
    if (position_hauteur==0):
        tab_hauteur=[['']]
    if (position_largeur==0) :
        tab_largeur=[['']]
    return tab_largeur,tab_hauteur
def choix_perso(dico):
    hauteur,largeur = position_to_choix_perso("rouge",dico)
    #print(hauteur,largeur)
    suite_touches(hauteur[0])
    suite_touches(largeur[0])
    hauteur, largeur = position_to_choix_perso("noir", dico)
    #print(hauteur, largeur)
    suite_touches(hauteur[0])
    suite_touches(largeur[0])
def choix_niveau(dico):
        position_largeur = (dico["rouge"][0][1] // 213)
        position_hauteur = (dico["rouge"][1][0] // 360)
        tab_largeur = [['d'] * position_largeur]
        tab_hauteur = [['s'] * position_hauteur]
        if (position_hauteur == 0):
            tab_hauteur = [['']]
        if (position_largeur == 0):
            tab_largeur = [['']]
        press('g')
        time.sleep(0.5)
        suite_touches(tab_hauteur[0])
        suite_touches(tab_largeur[0])
# """"""""""""""""""""""""""""""""""""""""""""""""""""
def match(dico_touches,):
    en_cour=True
    fin = False
    envoie_touches(dico_touches)
    gagnant = 1
    fin,gagnant = test_fin([0,0,0],pixel_fin)
    if (fin):
       en_cour=False
    return en_cour, gagnant
def test_fin(couleur,pixel):
    fin = False
    #print("on test la fin")
    test_final = False
    compteur = 0
    color = 0
    street = [(hwnd, title) for hwnd, title in winlist if 'snes' in title.lower()]
    street = street[0]
    hwnd = street[0]
    rect = win32gui.GetWindowRect(hwnd)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except:
        print("erreur foreground")
    time.sleep(0.001)
    screen = ImageGrab.grab(rect)
    for i in range(3):
        try:
            (pixel_fin_test[0], pixel_fin_test[1], pixel_fin_test[2]) = screen.getpixel((pixel[i][0], pixel[i][1]))
            #print(pixel_fin_test[0], pixel_fin_test[1], pixel_fin_test[2])
            #print(screen.getpixel((pixel[i][0], pixel[i][1])))
        except:
            print("erreur, getpixel")
        if (test_tableau(couleur, pixel_fin_test)):
            compteur += 1

    if compteur == 3:
        compteur = 0
        time.sleep(3)
        rect = win32gui.GetWindowRect(hwnd)
        time.sleep(0.001)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except:
            print("erreur foreground")
        time.sleep(0.05)
        screen = ImageGrab.grab(rect)
        for i in range(3):
            try:
                (pixel_fin_test[0], pixel_fin_test[1], pixel_fin_test[2]) = screen.getpixel((pixel_fin[i][0], pixel_fin[i][1]))
                #print(pixel_fin_test[0], pixel_fin_test[1], pixel_fin_test[2])
                screen.putpixel((pixel_fin[i][0], pixel_fin[i][1]),((255,255,255)))
            except:
                print("erreur, getpixel")
            #screen.show("image_test.png")
            if (test_tableau([0, 0, 0], pixel_fin_test)):
                compteur += 1
        if compteur == 3:
            '''while not(test_final):
                rect = win32gui.GetWindowRect(hwnd)
                time.sleep(0.001)
                screen = ImageGrab.grab(rect)
                test_final,_ = test_couleur(100, 300, 190, 350, [0,0,0], screen,"every")
                time.sleep(0.5)
                i+=1
                if i == 100:
                    test_final == True'''
            win, color = test_couleur2(100, 310, 200, 330, couleur_pixel_victoire, screen,"one")
            print("c'est la fin")
            fin = True
            '''if win:
                if color == 0:
                    gagnant = 0
                elif color == 1:
                    gagnant = 1'''
        #print(fin,gagnant)
    return fin, color
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
                    #image.putpixel((a+i,b+j),(255,0,0))
                except:
                    print("erreur getpixel")
                if couleur_reel[0] !=0:
                    print(couleur_reel,couleur)
                if not(test_tableau([0,0,0],couleur_reel)):
                    if(test_tableau(couleur_reel,couleur)):
                        vrai=True
                        #image.putpixel((a + i, b + j), (0, 255, 0))
        if vrai:
            color = 0
        else:
            color = 1
        #image.show('imahge')
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
def test_couleur(a,b,c,d,couleur,image,mode):
    vrai=False
    color = 0
    couleur_reel=[0,0,0]
    test = False
    if mode=='one':
        for i in range(c-a):
            for j in range(d-b):
                try:
                    (couleur_reel[0],couleur_reel[1],couleur_reel[2]) = image.getpixel((a+i,b+j))
                except:
                    print("erreur getpixel")
                if couleur_reel[0] !=0:
                    print(couleur_reel,couleur)
                if not(test_tableau([0,0,0],couleur_reel)):
                    if(test_tableau(couleur_reel,couleur)):
                        vrai=True
        if vrai:
            color = 0
        else:
            color = 1
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
def envoie_touches(dico):
    '''anciennes_touches = nouvelles_touches
    nouvelles_touches[0] = dico['rouge'][0]
    nouvelles_touches[1] = dico['rouge'][0]
    nouvelles_touches[2] = dico['noir'][0]
    nouvelles_touches[3] = dico['noir'][0]
    touches_a_eteindre,touches_a_envoyer = test_tableau_touches(anciennes_touches,nouvelles_touches)
    for index in range(len(touches_a_eteindre)):
        pyautogui.keyUp(touches_a_eteindre[index])
        time.sleep(0.01)
    for index in range(len(touches_a_envoyer)):
        pyautogui.keyDown(touches_a_envoyer[index])
        time.sleep(0.01)'''
    for couleur in ("rouge", "noir"):
        pyautogui.keyDown(dico[couleur][0])
        pyautogui.keyDown(dico[couleur][1])
        pyautogui.keyUp(dico[couleur][0])
        pyautogui.keyUp(dico[couleur][1])
    time.sleep(0.05)
    #ssfrdppprint(dico)
def test_tableau_touches(tab1,tab2):
    tabt1 = tab1
    tabt2 = tab2
    tab_return = []
    tab_return2 = []
    for i in range(len(tabt1)):
        for j in range(len(tabt2)):
            if tabt1[i] == tabt2[j]:
                tabt1[i] = 0
                tabt2[j] = 0
    for i in range(len(tabt1)):
        if tabt1[i] != 0:
            tab_return.append(tabt1[i])
        if tabt2[i] != 0:
            tab_return2.append(tabt2[i])
    return tab_return, tab_return2
#-------------------------------------------------------------
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
def init_score(bg):
    pygame.display.set_caption("score des poissons")
    screen = pygame.display.set_mode((938,504))
    screen.blit(bg, (0, 0))
    afficher_score((0, 0), screen)
    pygame.display.flip()
    return screen
def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
def street_fighter():
    os.system("\"C:\\Users\\foxfa\\OneDrive\\Bureau\\poissons_corps\\Street Fighter 2 Turbo.smc\"")
def envoie_victoire(victory):
    file = builtins.open('victoire.txt','w')
    file.write(str(victory))
    file.close()
#------------------------main---------------------------------
'''
depart = input("Lancer le programme: Y/N\n")
if depart == "Y" or depart == "Yes" or depart == "yes" or depart == "y":
    #street_fighter()
    print("Vous devez avoir lancé le stream\n A partir de maintenant il ne faudra plus toucher aux fenetres")
    print("Après Avoir répondu \'ok\' à ce message vous aurez 10 sec pour mettre street fighter au premier plan")
    depart = input("Entrez ok\n")
    street = [(hwnd, title) for hwnd, title in winlist if 'snes' in title.lower()]
    street = street[0]
    hwnd = street[0]
    if depart == 'ok':
        time.sleep(10)
        init()
        match_continue = True
        while running:
            try:
                win32gui.SetForegroundWindow(hwnd)
            except:
                print('erreur foreground')
            rect = win32gui.GetWindowRect(hwnd)
            time.sleep(2)
            image,originale = recuperer_image()
            dico, dico_touches = imageToDico(image, 0,fond,originale)
            choix_perso(dico)
            suite_touches([starta, startb])
            time.sleep(3)
            fond = image
            image,originale = recuperer_image()
            dico, dico_touches = imageToDico(image, 1,fond,originale)
            choix_niveau(dico)
            time.sleep(5)
            press(starta)
            time.sleep(5)
            match_continue = True
            while match_continue :
                image,originale = recuperer_image()
                if True:
                    dico, dico_touches = imageToDico(image, 0,fond,originale)
                    #print(dico_touches)
                    match_continue, gagnant = match(dico_touches)
                    count = 0
                    fond = image
                count +=1
            print("c'est la fin-match")
            print(score,gagnant)
            score[gagnant]+=1
            afficher_score(score=score,screen=screen)
            envoie_victoire(gagnant)
            time.sleep(5)
            press(starta)'''


