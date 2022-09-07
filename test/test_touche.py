import pyautogui
import time

def test_tableau(tab1,tab2):
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

tab1 = ['r','a',4,8]
tab2 = ['s','b',2,6]
print(test_tableau(tab1,tab2))