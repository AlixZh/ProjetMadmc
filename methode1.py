import tools as ts
import numpy as np
import matplotlib.pyplot as plt


def point_ideal(points_non_domine):
	#point_ideal en maximisation
	return np.max(np.array(points_non_domine),axis=0)

def point_nadir(points_non_domine):
	#point_nadir en maximisation
	return np.min(np.array(points_non_domine),axis=0)


def echange_11(pb,x_init,obj_retire):
    """
    pb : une liste des donnees du probleme
    x_init : une solution trouvé solution 
    obj_rerire : 
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
        L_=L.copy()
        if(obj!=obj_retire):
            if(w_[obj]+poids_<=W):
                #echange 1-1
                L_.append(obj)
                #des on peut encore ajouter des objets
                poids_poss=w_[obj]+poids_
                obj_poss=np.where(pb["wi"]+poids_poss<W)[0]
                for op in obj_poss:
                    if(w_[obj]+poids_poss<=W):
                        poids_poss+=w_[obj]
                        L_.append(op)
                list_x_change.append(L_)


    return list_x_change

def voisinage(pb,x_init,obj_retire):
    """
    pb : une liste des donnees du probleme
    x_init : une solution trouvé solution 
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




