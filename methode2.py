
import numpy as np
import matplotlib.pyplot as plt
import tools as *

def pmr(pb,fonc,x,xprim,omega_theta):
    """
    fonc : fonction d agregation
    pb : donnees du probleme
    x : une solution realisable
    xprim une autre solution realisable
    omega_theta : list[foat] contenant les capacites de choquet ou les poids ponderes
    renvoie la regret max de recommander x que xprim
    """
    yx = y(pb, x)
    yxprim = y(pb,xprim)
    max_trouve = 0 #valeur max trouve pour la difference
    max_w = omega_theta[0][0]
    for i in range(omega_theta[0]): 
        courante = fonct(pb,w,yx)-fontc(pb,w,yxprim)
        if( courante > max_trouve):
            max_trouve = courante
            max_w = w
    return max_trouve,max_w

def mr(pb,fonc,x,Xrond,omega_theta):
    """
    fonc : fonction d agregation
    x : une solution realisable
    Xrond : ens des solutions realisables
    omega_theta
    renvoie la regret max de recommander x que tout autre element de X
    """
    max_trouve = 0
    max_w = omega_theta[0][0]
    xmr = 0
    for xprim in Xrond : 
        if(xprim != x) : 
            max_trouve_courante,max_w_courante = pmr(pb,fonc,x,xprim,omega_theta)
            if(max_trouve_courante > max_trouve):
                max_w = max_w_courante
                max_trouve = max_trouve_courante
                xmr = xprim
    return max_trouve,max_w, xmr
               
def mmr(pb,fonc,Xrond,omega_theta):
    max_trouve = 0
    max_w = omega_theta[0][0]
    xmmr = Xrond[0]
    for x in Xrond:
        max_trouve_courante,max_w_courante,xmr_courante = mmr(pb,fonc,x,Xrond,omega_theta)
        if(max_trouve_courante > max_trouve):
            max_w = max_w_courante
            max_trouve = max_trouve_courante
            xmr = xmr_courante
            xmmr = x
    return xmmr,max_trouve,max_w, xmr

def echange_11(pb,x_init,obj_retire):
    """
    dict[str,Any] *list[int]*int -> set[set(int)]
    pb : dictionnaire des donnees du probleme
    x_init : une solution trouvé solution 
    obj_rerire : 
    renvoie la voisinage de cette solution
    """
    list_x_change={} #contient les ensembles d objets voisinages de x_init et obj_retire
    nb_obj = pb["n"]
    w_ = pb["wi"] #liste poids
    v_ = pb["v"] #liste profit
    W = pb["W"]
    L = set(x_init)
    L.remove(obj_retire)
    poids_ = np.sum([w_[i] for i in x_init],axis=0)-w_[obj_retire]#poids sans obj_retire
    for obj in range(nb_obj) :
        if(obj not in x_init):
            if(w_[obj] + poids_ <= W):
                #echange 1-1
                L.add(obj)
                list_x_change.append(L)

    return list_x_change


def voisins(pb,courante):
    """
    pb : dict du probleme des donnes
    """
    res = set()
    for obj_retire in courante:
        res.add(echange_11(pb,courante,obj_retire))
    return tous_les_voisins

def omega_theta(pb,Xrond): #achanger
    """
    generer tous les capacites de choquet ou poids de ponderation
    """
    o_t = {}
    for x in Xrond:
    	yx = y(pb,x)
    return o_t

def demande(Xrond,omega):
	"""
	demander au decideur de renvoyer un couple (a,b) tq qu il prefere a à b
	"""
	a=[]
	b=[]
	return a,b




def rbls(pb,eps,max_it,fonc):
    """
    pb : dict des donnees du probleme considere
    implementation du regret-based local search
    renvoie la solution du sac a dos
    """
    sol = init_glouton(pb)
    it = 0
    theta = set()
    o_t = {}
    ameliore = True
    while(ameliore and it < max_it) : 
        sol_voisins = voisinage(pb, sol)
        while( mmr(sol_voisins, omega) > eps):
            (a,b) = demande(sol_voisins,omega)
            theta.add((a,b))
           	o_t = omega_theta(pb,theta) #achanger
        if(mr(sol,sol_voisins,o_t) > eps):
        	sol,_,_,_ = mmr(pb,fonc,sol_voisins,o_t)
        	it += 1
        else:
        	ameliore = false
    return sol
        
            
            
         
            
    
    
    
