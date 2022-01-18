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
    return np.floor(w / len(xi))

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

def dict_pb(data,vp,xi):
    """
    data : dictionnaire des instances
    vp : liste des indices de critères
    xi : liste des indices des objets
    renvoie un dictionnaire des donnees du probleme a considerer
    """
    res = dict()
    res["n"] = len(xi)
    res["p"] = len(vp)
    res["W"] = wmax(data,xi)
    res["wi"], res["v"] = get_donnees_pb(data,vp,xi)
    res["vp"] = vp
    res["xi"] = xi
    return res

def get_pb_alea(data, n=20,p = 3):
    """
    data : dictionnaire de tous les instances
    n : nombre d objets du probleme
    p : nombre de critere a considerer
    renvoie des donnees d un probleme avec n objets et 3 contraintes
    """
    xi = set()
    vp = set()
    while(len(xi) < n ): #pour eviter d avoir des criteres et objets identiques
        x = np.random.randint(0,data["n"], 1)[0]
        if(x not in xi):
            xi.add(x)
    while(len(vp) < p):
        v = np.random.randint(1, len(data["nom_param"]), 1)[0]
        if(v not in vp):
            vp.add(v) 
    return dict_pb(data,vp,xi)


def sol(pb,x):
    """
    pb : un dictionnaire des donnees du probleme a considerer
    x : liste des indices des objets a prendre
    renvoie la solution de x sous forme res[i] = 1 si l objet i est pris
    """
    res = [0] * pb["n"]
    for i in x:
        res[i] = 1
    return res
    
def y_sol(pb,x,list_ind = True):
    """
    pb : un dictionnaire des donnees du probleme a considerer
    x  : (une solution realisable) liste des objets à prendre dans cette solution
    revoie l'evaluation de x, contient que des 1 et 0
    """
    res=[0]*pb["p"]
    if(list_ind):
        res=np.array([0]*pb["p"])
        for i in x:
            res+=np.array(pb["v"][i])
    else:
        for i in range(pb["n"]):
            for p in range(pb["p"]):
                res[p] += pb["v"][i][p]*x[i]
    return res


#----------------------------------------
# fonction d initialisation
#----------------------------------------

def init_glouton(pb):
    """
    pb :  un dictionnaire des donnees du probleme a considerer

    renvoie une solution initiale 
    """
    somme_yi = np.sum(pb["v"],1) / pb["p"] #somme des vp des criteres a considerer
    indice=np.argsort(somme_yi)  #trier la moyenne arithmetique de chaque objet
    i = pb["n"]-1
    sol=[] #liste contient les indices des objets prises
    s = 0  #somme des poids des objets ajouter dans sol      
    while(i >= 0):
        if (s + pb["wi"][i] <= pb["W"]):
            s += pb["wi"][i]  
            sol.append(i)
        i -= 1
    return sol

#----------------------------------------
# fonction voisinage
#----------------------------------------   

def voisinage(pb,x_init):
    """
    pb : un dictionnaire des donnees du probleme a considerer
    x_init: les indices des objets d une solution trouve

    revoie la voisinage de cette solution trouver
    """
    list_voisinage=[]
    for obj in x_init:
        list_x_change=echange_11(pb,x_init,obj)
        for x in list_x_change:
            add_set_in_list(x,list_voisinage)
    return list_voisinage

def echange_11(pb,x_init,obj_retire):
    """
    pb : une liste des donnees du probleme
    x_init : une solution trouve solution 
    obj_retire : indice d objet retire
    
    renvoie la voisinage de cette solution en retirant objet obj_retire
    """
    list_x_change=[]
    nb_obj=pb["n"]
    w_=pb["wi"]#liste poids

    W=pb["W"]
    L=x_init.copy()
    L.remove(obj_retire)
    poids_=np.sum([w_[i] for i in x_init],axis=0)-w_[obj_retire]#poids sans obj_retire
    for obj in range(nb_obj) :
        L_=set(L.copy())
        if(obj not in x_init):
            if(w_[obj]+poids_<=W):
                #echange 1-1
                L_.add(obj)
                #des on peut encore ajouter des objets
                poids_poss=w_[obj]+poids_
                obj_poss=list(np.where(w_<=(W-poids_poss))[0])
                for op in obj_poss:
                    if(op==obj_retire or op in L_):
                        continue
                    if(w_[op]+poids_poss<=W):
                        poids_poss+=w_[op]
                        L_.add(op)
                add_set_in_list(L_,list_x_change)
    return list_x_change


def add_set_in_list(set1,list2):
    """
    ajouter un set dans un list de set si :
    il n est pas dedans et 
    il n est pas un subset de set dans list

    """
    if(set1 not in list2):
        add=True
        for s in list2:
            if(set1.issubset(s)):
                add=False
                break
        if(add==True):
            list2.append(set1)


#----------------------------------------
# fonction d agregation
#----------------------------------------

def gen_poids(taille):
    """
    taille : taille du vecteur poids
    renvoie le vecteur poids sommant a 1
    """
    w = np.zeros(taille)
    s = 1
    for i in range(taille-1):
        w[i] = s*np.random.sample()
        s = s - w[i]
    w[-1] = 1 - np.sum(w)
    return w

def som_pond(pb,w,x,list_ind = True):
    """
    pb : donnees du probleme a considerer
    w : liste des poids de ponderation pour la somme ponderee
    x : la liste des indices des objets a prendre dans le sac ou la liste contenant des 1 et 0
    list_ind si x est la liste des indices des objets
    
    renvoie le resultat de la fonction d agregation somme ponderee, 
    et true s il est valide, false, s il y a une erreur
    """
    res = 0
    if(len(w) != pb["p"]):
        print("la taille du nb de poids de ponderation n'est pas egale à la taille du nombre d objet")
        return res
    elif(round(np.sum(w)) != 1):
        print("sum(wi) != 1")
        return res
    ai = y_sol(pb,x,list_ind)
    for p in range(pb["p"]):
        res += ai[p]*w[p]
    return res                                  
                                      
                
def owa(pb,w,x,list_ind = True):
    """
    pb : donnees du probleme a considerer
    w : liste des poids de ponderation pour la somme ponderee
    x : la liste des indices des objets a prendre dans le sac ou la liste contenant des 1 et 0
    list_ind si x est la liste des indices des objets
    
    renvoie le resultat de la fonction d agregation somme ponderee, 
    et true s il est valide, false, s il y a une erreur
    """
    res = 0
    if(len(w) != pb["p"]):
        print("la taille du nb de poids de ponderation n'est pas egale à la taille du nombre d objet")
        return res
    elif(round(np.sum(w)) != 1):
        print("sum(wi) != 1")
        return res
    ai = y_sol(pb,x,list_ind)
    ind = np.argsort(ai) #trier les criteres dans l ordre croissant
    for p in range(pb["p"]):
        res += ai[ind[p]]*w[p]
    return res 

def owa_Y(pb,w,y,list_ind = True):
    """
    pb : donnees du probleme a considerer
    w : liste des poids de ponderation pour la somme ponderee
    x : la liste des indices des objets a prendre dans le sac ou la liste contenant des 1 et 0
    list_ind si x est la liste des indices des objets
    
    renvoie le resultat de la fonction d agregation somme ponderee, 
    et true s il est valide, false, s il y a une erreur
    """
    res = 0
    if(len(w) != pb["p"]):
        print("la taille du nb de poids de ponderation n'est pas egale à la taille du nombre d objet")
        return res
    elif(round(np.sum(w)) != 1):
        print("sum(wi) != 1")
        return res
    ind = np.argsort(y) #trier les criteres dans l ordre croissant
    for p in range(pb["p"]):
        res += y[ind[p]]*w[p]
    return res 

def gen_capacite(pb,w=[]):
    """
    pb : donnees du problem
    generer les poids de choquet
    """
    nvw = true #il faut generer un w
    if(w != []):
        nvw = false #il ne faut pas generer de w
    if(nvw):
        w = [0]
    possibilite = [[set()]]
    for i in range(1,pb["p"]-1):
        comb = list(itertools.combinations([k for k in range(pb["p"])],i))
        possibilite.append([set(i) for i in comb])
        if(nvw and i ==1): #generer les jeux de poids pour les singletons
            w.append(np.random.random(len(comb))) 
        else:
        	w.append(np.random.random(len(comb))) #achanger
    possibilite.append([{i for i in range(pb["p"])}])
    if(nvw):
        w.append(1)
    return w, possibilite


def int_choquet(pb,w,x):
    """
    pb : donnees du probleme a considerer
    w : liste des poids de ponderation pour la somme ponderee
    x : la liste des indices des objets a prendre dans le sac 
    renvoie le resultat de la fonction d agregation somme ponderee, 
    et true s il est valide, false, s il y a une erreur
    """
    res = 0
    w, possibilite = gen_capacite(pb,w)
    ai = y(pb,x)    
    ind = np.argsort(ai) #trier les criteres dans l ordre croissant
    
    for i in range(0,pb["p"]):
        if(i == 0):
            res += (ai[ind[i]] -0) * w[len(ind[i:])][np.where( np.array(possibilite) == set(ind[i:]) )]
        else : 
            res += (ai[ind[i]] -ind[i-1]) * w[len(ind[i:])][np.where(np.array(possibilite) == set(ind[i:]) )]
    return res

