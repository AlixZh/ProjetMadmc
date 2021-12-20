import sys
import os
import numpy as np
import matplotlib.pyplot as plt


def lire_fichier(fichier="./2KP200-TA-0.dat"):
    """
    fichier : contenant les instances du probleme
    """
    data=dict()
    data["i"]=[]
    with open(fichier,"r") as fd:
        ligne = fd.readlines()
        for l in ligne:
            l = l.split()
            if(l[0] == "n"):
                data["n"]=int(l[1])
            elif(len(l) == 8 and l[0] == "c"):
                data["nom_param"] = l[1:]
            elif(l[0] == "i"):
                data["i"].append([int(i) for i in l[1:]])
            elif(l[0] == "W"):
                data["W"] = int(l[1])
            

    return data

def wmax(data,vp,xi):
    """
    data  dictionnaire des donnees
    vp : liste, contient les i indices des objectifs à prendre en compte
    xi : liste, contient les indices des objets à prendre
    renvoie la capacite a ne pas depasser
    """
    w = 1 
    for v in range(len(vp)):
        w += data["i"][xi[v]][vp[v]]
    return w // 2
