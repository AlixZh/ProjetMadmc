import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from gurobipy import *

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
    list_ind=True si x contient indice d'objets,False si x sous forme x[i] = 1 si l objet i est pris,sinon x[i]=0
    pb : un dictionnaire des donnees du probleme a considerer
    x  : (une solution realisable) liste des objets à prendre dans cette solution
    revoie l'evaluation de x
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

def gen_poids_precision(taille, precision):
    """
    taille : taille du vecteur poids
    precision : nombre de chiffre apres la virgule
    renvoie le vecteur poids sommant a 1
    """
    w = np.zeros(taille)
    s = 1
    for i in range(taille-1):
        w[i] = round(s*np.random.sample(),precision)
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

def som_pond_Y(w,y):
    """
    w : liste des poids de ponderation pour la somme ponderee
    y : une evaluation d'une solution realisable 
    
    renvoie le resultat de la fonction d agregation somme ponderee, 
    et true s il est valide, false, s il y a une erreur
    """
    res = 0
    if(len(w) != len(y)):
        print("la taille du nb de poids de ponderation n'est pas egale à la taille du nombre d objet")
        return res
    elif(round(np.sum(w)) != 1):
        print("sum(wi) != 1")
        return res
    for i in range(len(w)):
        res += y[i]*w[i]
    return res 


def owa_Y(w,y):
    """
    w : liste des poids(ordre decrossant)
    y : evaluation d'une solution
    renvoie le resultat de la fonction d agregation somme ponderee, 
    et true s il est valide, false, s il y a une erreur
    """
    res = 0
    if(len(w) != len(y)):
        print("la taille du nb de poids de ponderation n'est pas egale à la taille du nombre d objet")
        return res
    elif(round(np.sum(w)) != 1):
        print("sum(wi) != 1")
        return res
    yy = np.sort(y) #trier les criteres dans l ordre croissant

    for i in range(len(w)):
        res += yy[i]*w[i]
    return res


#----------------------------------------
# fonction pour calculer pmr,mr,mmr
#----------------------------------------

def PMR_SP(y,yprim,P=[]):
    """
    y(array) : une evaluation d'une solution realisable
    yprim(array) : une autre evaluation

    revoie tuple(array,float):lambda qui donne le max regret (y-x),et la valeur de max regret
    """
    env = Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    if(len(y)!=len(yprim)):
        print ("erreur len(y)!=len(yprim)")
    nbvar=len(y)
    colonnes = range(nbvar)

    #matrice des contraintes
    a = [1]*nbvar
    # Second membre
    b = 1.0
    #parametre de fonction objectif
    c=(yprim-y)

    m = Model("PMR_SP",env=env)     
 # declaration variables de decision
    lambda_ = []
    for i in colonnes:
        lambda_.append(m.addVar(vtype=GRB.CONTINUOUS,lb=0.0,ub=1.0, name="lambda%d" % (i+1)))

    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = LinExpr();
    for i in range(nbvar):
        obj+=c[i]*lambda_[i]
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    # Definition des contraintes
    m.addConstr(quicksum(lambda_[j]*a[j] for j in colonnes) == b, "Contrainte%d" % 1)
    for yi,yprim_i in P:
        m.addConstr(quicksum(lambda_[j]*(yi-yprim_i)[j] for j in colonnes) >= 0.0)

    # Resolution
    m.optimize()

    if(m.status==3):
        return None,float("-inf")
    res=np.array([0.0]*nbvar)
    for j in colonnes:
        res[j]=lambda_[j].x
    return res,m.objVal

def PMR_OWA(y,yprim,P=[]):
    """
    y(array) : une evaluation d'une solution realisable
    yprim(array) : une autre evaluation
    revoie tuple(array,float):lambda qui donne le max regret (y-x),et la valeur de max regret
    """
    env = Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    y_=y.copy()
    yprim_=yprim.copy()
    y_.sort()
    yprim_.sort()
    if(len(y_)!=len(yprim_)):
        print ("erreur len(x)!=len(y)")
    nbvar=len(y_)
    colonnes = range(nbvar)

    #matrice des contraintes
    a = [1]*nbvar
    # Second membre
    b = 1.0
    #parametre de fonction objectif
    c=(yprim_-y_)

    m = Model("PMR_OWA",env=env)     
 # declaration variables de decision
    lambda_ = []
    for i in colonnes:
        lambda_.append(m.addVar(vtype=GRB.CONTINUOUS,lb=0.0,ub=1.0, name="lambda%d" % (i+1)))

    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = LinExpr();
    for i in range(nbvar):
        obj+=c[i]*lambda_[i]
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    # Definition des contraintes
    m.addConstr(quicksum(lambda_[j]*a[j] for j in colonnes) == b, "Contrainte%d" % 1)#somme lambda=1
    for i in range(0,nbvar-1):
        m.addConstr(lambda_[i]-lambda_[i+1] >= 0 )#lambda_i>lambda_i+1
    for a1,a2 in P.copy():
        x1=a1.copy()
        y1=a2.copy()
        x1.sort()
        y1.sort()
        m.addConstr(quicksum(lambda_[j]*(x1-y1)[j] for j in colonnes) >= 0.0)
    # Resolution
    m.optimize()
    if(m.status==3):
        return None,float("-inf")
    res=np.array([0.0]*nbvar)
    for j in colonnes:
        res[j]=lambda_[j].x
    return res,m.objVal

def MR(y,Y,P=[],fonc_pmr=PMR_SP):
    """
    y(array) : une evaluation d'une solution realisable
    Y(list(array)) : ensemble d'evaluations possibles
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    fonc_pmr : programmation lineaire de pmr pour un type de fonction aggregation(PMR_SP:somme pondérée, PMR_OWA:OWA ou PMR_IC:l’intégrale de Choquet)
    revoie tuple(list,float): y dans list Y telle qu'il maximise (pmr)(le pire des regrets associé à la recommandation de l'alternative y à la place
de toute autre alternative dans Y ), et la valeur max
    """

    arg_res_mr=np.array([0.0]*len(y))
    res_mr=float("-inf")
    for yprim in Y:
        if(np.all(y==yprim)):
            continue
        # if((x,y) in P):
        #     continue
        w,res_pmr=fonc_pmr(y,yprim,P)
        if(res_pmr>=res_mr):
            arg_res_mr=yprim
            res_mr=res_pmr
    return arg_res_mr,res_mr
def MMR(Y,P=[],fonc_pmr=PMR_SP):
    """
    Y(list(array)) : ensemble d'evaluations possibles
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie array,float : y dans Y qui donne Minimax Regret et minimax regret
    """
    arg_res_mmr=np.array([0.0]*len(Y[0]))
    res_mmr=float("inf")
    for y in Y:
        arg_res_mr,res_mr=MR(y,Y,P,fonc_pmr)
        if(res_mr<=res_mmr):
            arg_res_mmr=y
            res_mmr=res_mr
    return arg_res_mmr,res_mmr
def y_prefere_yprim(fonc,y,yprim,lambda_etoile):
    """
    demander au decideur si il prefere y à yprim
    fonc : fonction agregation avec Y : evaluation de X
    y(array) : une evaluation de solution
    yprim(array) : une autre evaluation de solution
    lambda_etole : poids exacte de fonction d'agregation
    """
    fw_y = fonc(lambda_etoile,y)
    fw_yprim = fonc(lambda_etoile,yprim)
    if(np.all(fw_y > fw_yprim)):
        return True
    return False


#----------------------------------------
# fonction pas encore realisable pour integrale de choquet
#----------------------------------------

# def gen_capacite(pb,w=[]):
#     """
#     pb : donnees du problem
#     generer les poids de choquet
#     """
#     nvw = True #il faut generer un w
#     if(w != []):
#         nvw = False #il ne faut pas generer de w
#     if(nvw):
#         w = [0]
#     possibilite = [[set()]]
#     for i in range(1,pb["p"]-1):
#         comb = list(itertools.combinations([k for k in range(pb["p"])],i))
#         possibilite.append([set(i) for i in comb])
#         if(nvw and i ==1): #generer les jeux de poids pour les singletons
#             w.append(np.random.random(len(comb))) 
#         else:
#           w.append(np.random.random(len(comb))) #achanger
#     possibilite.append([{i for i in range(pb["p"])}])
#     if(nvw):
#         w.append(1)
#     return w, possibilite


# def int_choquet(pb,w,x):
#     """
#     pb : donnees du probleme a considerer
#     w : liste des poids de ponderation pour la somme ponderee
#     x : la liste des indices des objets a prendre dans le sac 
#     renvoie le resultat de la fonction d agregation int_choquet, 
#     et true s il est valide, false, s il y a une erreur
#     """
#     res = 0
#     w, possibilite = gen_capacite(pb,w)
#     ai = y(pb,x)    
#     ind = np.argsort(ai) #trier les criteres dans l ordre croissant
    
#     for i in range(0,pb["p"]):
#         if(i == 0):
#             res += (ai[ind[i]] -0) * w[len(ind[i:])][np.where( np.array(possibilite) == set(ind[i:]) )]
#         else : 
#             res += (ai[ind[i]] -ind[i-1]) * w[len(ind[i:])][np.where(np.array(possibilite) == set(ind[i:]) )]
#     return res

