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
                data["n"]=l[1]
            if(len(l) == 8 and l[0] == "c"):
                data["nom_param"] = l[1:]
            if(l[0] == "i"):
                data["i"].append(l[1:])
            if(l[0] == "W"):
                data["W"] = l[1]
            

    return data
