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
import street_fighter as st
#import tekken as tk
#============================================#
#========Variables===========================#
bg = pygame.image.load('score\\score.png')











#============================================#
#==========main==============================#
fond,screen,running,score = f.initVariables()
depart = input("Lancer le programme: Y/N\n")
if depart in ["Y", "Yes", "yes", "y"]:
    jeu = input("Choisissez le jeu que vous voulez stream:\n1: Street fighter\n2: Tekken\n")
    if jeu == "1":
        print("ok")
        st.main()
    elif jeu == "2":
        print("ko")
        st.main()