
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

    max_trouve = 0 #valeur max trouve pour la difference
    if(omega_theta == set()):
        max_w = gen_poids(pb["p"])
    else:
        max_w = omega_theta.pop()
    for w in omega_theta: 
        courante = fonc(pb,w,x)[1]-fonc(pb,w,xprim)[1]
        if( courante > max_trouve):
            max_trouve = courante
            max_w = w
    return max_trouve,max_w

def mr(pb,fonc,x,Xrond,omega_theta):
    """
    fonc : fonction d agregation
    x : une solution realisable
    Xrond : ens des solutions realisables
    omega_theta : ensemble des jeux de poids possibles
    renvoie la regret max de recommander x que tout autre element de X
    """
    max_trouve = 0
    if(omega_theta == set()):
        max_w = gen_poids(pb["p"])
    else:
        max_w = omega_theta.pop()
    xmr = 0
    for xprim in Xrond : 
        if(xprim != x) : 
            max_trouve_courante,max_w_courante = pmr(pb,fonc,x,xprim,omega_theta)
            if(max_trouve_courante > max_trouve):
                max_w = max_w_courante
                max_trouve = max_trouve_courante
                xmr = xprim #y*
    return max_trouve,max_w, xmr
               
def mmr(pb,fonc,Xrond,omega_theta):
    """
    pb : dict du probleme
    fonc : fonction d agregation utilisee
    Xrond : sol realisable
    omega_theta : ensemble des jeux de poids possibles
    """
    max_trouve = 0
    if(omega_theta == set()):
        max_w = gen_poids(pb["p"])
    else:
        max_w = omega_theta.pop()

    xmmr = Xrond[0]
    xmr = -1
    for x in Xrond:
        max_trouve_courante,max_w_courante,xmr_courante = mr(pb,fonc,x,Xrond,omega_theta)
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

def omega_theta(pb,fonc,theta): #achanger
    """
    generer tous les capacites de choquet ou poids de ponderation
    """
    o_t = set()
    set_w = set()
    non_trouve = True
    while(non_trouve):
        non_trouve = False
        w = gen_poids(pb["p"])
        if( w not in set_w): # pour ne pas verifier pour des w deja trouve
            for a,b in theta:
                if(not demande_a_prefere_b(pb,fonc,a,b,w)):
                    non_trouve = True
                    break
    o_t.add(w)
    return o_t

def demande_a_prefere_b(pb,fonc,a,b,w_etoile):
    """
    demander au decideur si il prefere a à b
    """
    fw_a = fonc(pb,w_etoile,a)
    fw_b = fonc(pb,w_etoile,b)
    if(np.all(fw_a > fw_b)):
        return True
    return False


def demande(pb,fonc,x_etoile,Xetoile,w_etoile):
    omega_t = [w_etoile]
    max_trouve,max_w, xmr = mr(pb,fonc,x_etoile,Xetoile,omega_t)
    if(demande_a_prefere_b(pb,fonc,x_etoile,xmr,w_etoile)):
        return x_etoile[0],xmr.pop()
    return xmr[0],x_etoile.pop()

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

def rbls(pb,eps,max_it,fonc):
    """
    pb : dict des donnees du probleme considere
    implementation du regret-based local search
    renvoie la solution du sac a dos
    """
    sol = init_glouton(pb)
    it = 0
    theta = set()
    o_t = set()
    ameliore = True
    w_etoile = gen_poids(pb["p"]) # liste de poids cache du decideur
    
    while(ameliore and it < max_it) : 
        sol_voisins = voisinage(pb, sol)
        while( mmr(pb,fonc,sol_voisins, o_t)[1] > eps):
            (a,b) = demande(pb,sol,sol_voisins,[w_etoile])
            theta.add((a,b))
            o_t = omega_theta(pb,fonc,theta) #achanger
        if(mr(pb,fonc,sol,sol_voisins,o_t)[0] > eps):
            sol,_,_,_ = mmr(pb,fonc,sol_voisins,o_t)
            it += 1
        else:
            ameliore = False
    return sol
    
    #essaie
        
            
            
         
            
    
    
    
