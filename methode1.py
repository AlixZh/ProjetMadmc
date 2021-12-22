import tools as ts
import numpy as np
import matplotlib.pyplot as plt
import quadtree as qdt
def echange_11(pb,x_init,obj_retire):
    """
    pb : une liste des donnees du probleme
    x_init : une solution trouve solution 
    obj_retire : 
    renvoie la voisinage de cette solution
    """
    list_x_change=[]
    nb_obj=pb["n"]
    w_=pb["wi"]#liste poids
    v_=pb["v"]#liste profit
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
                wi=w_.copy()
                wi.pop(obj)
                wi.pop(obj_retire)
                obj_poss=list(np.where(wi<=(W-poids_poss))[0])
                print(obj_poss,obj,obj_retire)
                for op in obj_poss:
                    if(w_[obj]+poids_poss<=W):
                        poids_poss+=w_[obj]
                        L_.add(op)
                if(L_ not in list_x_change):
                    list_x_change.append(L_)

    return list_x_change
    
def voisinage(pb,x_init):
    list_voisinage=[]
    for obj in x_init:
        list_x_change=echange_11(pb,x_init,obj)
        for x in list_x_change:
            if(x not in list_voisinage):
                list_voisinage.append(x)
    return list_voisinage



def PLS(pb,V=voisinage):
    P0=[init_glouton(pb)]#population initiale
    Xe_approx=P0.copy()#une approximation de l ensemble des solutions efficaces Xe
    P=P0.copy()#population
    Pa=[]#population auxiliaire
    while (P!=[]):
        for p in P:
            for pp in V(pb,P,p)
'''
def MiseAJour(X,x):
    XX=np.array(X)
    xx=np.array(x)
    tri_x1=XX[np.argsort(XX,axis=0)[:,0]]

    t=0
    f=len(XX)-1
    while(f-t>0 ):
        m=(f-t)//2
        if(tri_x1[t+m][0]<xx[0]):
            t=m
        else:
            f=m
    if(tri_x1[m+t][0]<xx[0]):
        m=m+1
    if(tri_x1[m+t][1]<xx[1]):
        X.append(xx)
        for i in range(0,m+t):
            if(tri_x1[i][1]<xx[1]):
                X.remove(tri_x1[i].tolist())
                    
    return X


def point_ideal(points_non_domine):
    #point_ideal en maximisation
    return np.max(np.array(points_non_domine),axis=0)

def point_nadir(points_non_domine):
    #point_nadir en maximisation
    return np.min(np.array(points_non_domine),axis=0)
'''
