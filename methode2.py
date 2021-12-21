
import numpy as np
import matplotlib.pyplot as plt
import tools as *

def pmr(fonc,pb,x,xprim,omega_theta):
    """
    fonc : fonction d agregation
    pb : donnees du probleme
    x : une solution realisable
    xprim une autre solution realisable
    omega_theta : tuple(list[foat], list[int])
    renvoie la regret max de recommander x que xprim
    """
    yx = y(pb, x)
    yxprim = y(pb,xprim)
    max_trouve = 0 #valeur max trouve pour la difference
    max_w = omega_theta[0][0] 
    for i in range(omega_theta[0][1:]): 
        if(fonct(pb,w,yx)-fontc(yxprim
    return m

def mr():
    """
    fonc : fonction d agregation
    x : une solution realisable
    xprim une autre solution realisable
    omega_theta
    renvoie la regret max de recommander x que tout autre element de X
    """
    return
               
def mmr():
    return

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
        if(obj!=obj_retire):
            if(w_[obj]+poids_<=W):
                #ne peut qu'ajouter cet obj
                if(any(v_[obj]>v_[obj_retire])):
                    #ameliorer le profit
                    list_x_change.append([obj]+L)
    return list_x_change

def voisin(pb,courante):
    """
    pb : donnees du probleme
    courante : solution courante
    """
    ens ={}
    return ens

rbls(pb,eps,max_it):
    """
    pb : dict des donnees du probleme considere
    implementation du regret-based local search
    renvoie la solution du sac a dos
    """
    sol = init_glouton(pb)
    it = 0
    ameliore = True
    while(ameliore and it < max_it) : 
        sol_voisins = voisinage(pb, sol)
         while( mmr(sol_voisins, omega) > eps):
                (a,b) = demande(sol_voisins,omega)
            
    
    
    
