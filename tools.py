import sys
import os
import numpy as np
import matplotlib.pyplot as plt

#----------------------------------------
# fonction d agregation de donnees
#----------------------------------------

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

def wmax(data,xi):
    """
    data  dictionnaire des donnees
    xi : liste, contient les indices des objets à prendre
    renvoie la capacite a ne pas depasser
    """
    w = 1 
    for x in xi:
        w += data["i"][x][0]
    return w // 2

def get_donnees_pb(data,vp,xi):
    """
    data : dictionnaire des instances
    vp : liste des indices de critères
    xi : liste des indices des objets
    renvoie une liste des donnees vp et wi du probleme a considerer
    """
    res = []
    wi = []
    for x in xi :
        res.append(np.array([data["i"][x][p] for p in vp])) #contient que les vp
        wi.append(data["i"][x][0])
    return np.array(wi), np.array(res)

 def pb(data,vp,xi):
    """
    data : dictionnaire des instances
    vp : liste des indices de critères
    xi : liste des indices des objets
    renvoie un dictionnaire des donnees du probleme a considerer
    """
    res = dict()
    res["n"] = len(xi)
    res["p"] = len(vp)
    res["W"] = wmax(data,vp,xi)
    res["wi"], res["v"] = get_donnees_pb(data,vp,xi)
    res["vp"] = vp
    res["xi"] = xi
    return res

def sol(pb,x):
	"""
	pb : dict des donnees du probleme
	x : liste des indices des objets a prendre
	renvoie la solution de x sous forme res[i] = 1 si l objet i est pris
	"""
	res = [0] * pb["n"]
	for i in x:
		res[i] = 1
	return res
	


#----------------------------------------
# fonction d initialisation
#----------------------------------------

def init_glouton(pb):
    """
    data : dictionnaire des instances
    vp : liste des indices de critères
    xi : liste des indices des objets
    renvoie une solution initiale 
    """
    somme_yi = np.sum(pb["i"],1) / pb["p"] #somme des vp des criteres a considerer
    indice=np.argsort(somme_yi)  #trier la moyenne arithmetique de chaque objet
    i = pb["n"]-1
    sol=[] #liste contient les indices des objets prises
    s = 0  #somme des poids des objets ajouter dans sol      
    while(i >= 0):
        if (s + pb["wi"][i] < data["W"]):
            s += pb["wi"][i]  
            sol.append(indice[i])
        i -= 1
    return sol
    

#----------------------------------------
# fonction d agregation
#----------------------------------------
def y(pb,x):
    """
    pb : une liste des donnees du probleme
    x  : (une solution realisable) liste des indices des objets qu'on prends dans cette solution
    revoie y : evaluation de x
    """
    y=np.array([0]*pb["p"])
    for i in x:
        y+=np.array(pb["v"][i])
    return y

def som_pond(pb,w,x):
    """
    pb : donnees du probleme a considerer
	w : liste des poids de ponderation pour la somme ponderee
	x : la liste des indices des objets a prendre dans le sac
	renvoie le resultat de la fonction d agregation somme ponderee, 
	et true s il est valide, false, s il y a une erreur
    """
    res = 0
    if(len(w) != len(pb["n"])):
        print("la taille du nb de poids de ponderation n'est pas egale à la taille du nombre d objet")
        return false,res
	ai = y(pb,x)
	for p in range(pb["p"]):
		res = ai[p]*w[p]
	return true, res								  
									  
            	
def owa(pb,w,x):
    """
    pb : donnees du probleme a considerer
	w : liste des poids de ponderation pour la somme ponderee
	x : la liste des objets a prendre dans le sac x[i] = 1 , prendre l'objet pb["xi"][i]
	renvoie le resultat de la fonction d agregation somme ponderee, 
	et true s il est valide, false, s il y a une erreur
    """
	res = 0
	if(len(w) != len(pb["n"])):
		print("la taille du nb de poids de ponderation n'est pas egale à la taille du nombre d objet")
		return false,res
	elif(np.sum(w) != 1):
		print("sum(wi) != 1")
		return false,res
	ai = y(pb,x)
	ind = np.argsort(ai) #trier les criteres dans l ordre
	for p in range(pb["p"]):
		res += ai[ind[p]]*w[p]
	return true,res			   
				   
"""									  
def int_choquet():
    """
    pb : donnees du probleme a considerer
	w : liste des poids de ponderation pour la somme ponderee
	x : la liste des objets a prendre dans le sac x[i] = 1 , prendre l'objet pb["xi"][i]
	renvoie le resultat de la fonction d agregation somme ponderee, 
	et true s il est valide, false, s il y a une erreur
    """
"""	
	
