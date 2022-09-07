import pyautogui
from PIL import ImageGrab
from PIL.Image import *
import cv2 as cv
import numpy as np
import pygame
import time
import win32gui
import os
import fonctions as f













def main():
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
            image, originale = recuperer_image()
            dico, dico_touches = imageToDico(image, 0, fond, originale)
            choix_perso(dico)
            f.suite_touches([starta, startb])
            time.sleep(3)
            fond = image
            image, originale = recuperer_image()
            dico, dico_touches = imageToDico(image, 1, fond, originale)
            choix_niveau(dico)
            time.sleep(5)
            press(starta)
            time.sleep(5)
            match_continue = True
            while match_continue:
                image, originale = recuperer_image()
                if True:
                    dico, dico_touches = imageToDico(image, 0, fond, originale)
                    # print(dico_touches)
                    match_continue, gagnant = match(dico_touches)
                    count = 0
                    fond = image
                count += 1
            print("c'est la fin-match")
            print(score, gagnant)
            score[gagnant] += 1
            afficher_score(score=score, screen=screen)
            envoie_victoire(gagnant)
            time.sleep(5)
            press(starta)