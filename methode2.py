
import numpy as np
import matplotlib.pyplot as plt


def pmr(pb,fonc,x,xprim,omega_theta):
    """
    fonc : fonction d agregation
    pb : donnees du probleme
    x : une solution realisable
    xprim une autre solution realisable
    omega_theta : list[foat] contenant les capacites de choquet ou les poids ponderes
    renvoie la regret max de recommander x que xprim
    """

    max_trouve = -1
    max_w = -1
    init = True
    for w in omega_theta: 
        if(init):
            max_trouve = fonc(pb,w,x)-fonc(pb,w,xprim) #valeur max trouve pour la difference
            max_w = next(iter(omega_theta))
            init = False
            break
        if( courante > max_trouve):
            print("entrer dans pmr")
            max_trouve = courante
            max_w = w
    print(max_trouve)
    return max_trouve,max_w

def mr(pb,fonc,x,Xrond,omega_theta):
    """
    fonc : fonction d agregation
    x : une solution realisable
    Xrond : ens des solutions realisables
    omega_theta
    renvoie la regret max de recommander x que tout autre element de X
    """
    max_trouve = -1
    max_w = -1
    xmr = -1
    init = True
    for xprim in Xrond : 
        if(xprim != set(x)) : 
            if(init):
                max_trouve_courante,max_w_courante = pmr(pb,fonc,x,xprim,omega_theta)
                init = False
                break
            max_trouve_courante,max_w_courante = pmr(pb,fonc,x,xprim,omega_theta)
            if(max_trouve_courante > max_trouve):
                max_w = max_w_courante
                max_trouve = max_trouve_courante
                xmr = xprim #y*
    print("fin ----------")
    return max_trouve,max_w, xmr
               
def mmr(pb,fonc,Xrond,omega_theta):
    max_trouve = -1
    max_w = next(iter(omega_theta))
    init = True
    xmmr = Xrond[0]
    xmr = -1
    for x in Xrond:
        if(init):
            max_trouve_courante,max_w_courante,xmr_courante = mr(pb,fonc,x,Xrond,omega_theta)
            init = False
            break
        max_trouve_courante,max_w_courante,xmr_courante = mr(pb,fonc,x,Xrond,omega_theta)
        if(max_trouve_courante > max_trouve):
            max_w = max_w_courante
            max_trouve = max_trouve_courante
            xmr = xmr_courante
            xmmr = x
    return xmmr,max_trouve,max_w, xmr


def omega_theta(pb,fonc,theta): #achanger
    """
    generer tous les capacites de choquet ou poids de ponderation
    """
    o_t = set()
    set_w = set()
    non_trouve = True
    while(non_trouve):
        non_trouve = False
        w = tuple(gen_poids(pb["p"]))
        if( w not in set_w): # pour ne pas verifier pour des w deja trouve
            for a,b in theta:
                if(not demande_a_prefere_b(pb,fonc,a,b,w)):
                    non_trouve = True
                    break
    o_t.add(w)
    return o_t

def demande(y_etoile,voisinage_Y,preferences,w_etoile,fonc = som_pond_Y,fonc_pmr=PMR_SP):
    ymr,res = MR(y_etoile,voisinage_Y,preferences,fonc_pmr)
    if(y_prefere_yprim(fonc,y_etoile,ymr,w_etoile)):
        return y_etoile,ymr
    return ymr,y_etoile

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
    o_t.add(tuple(gen_poids(pb["p"])))
    ameliore = True
    w_etoile = tuple(gen_poids(pb["p"])) # liste de poids cache du decideur
    
    while(ameliore and it < max_it) : 
        sol_voisins = voisinage(pb, sol)
        print("mmr ",mmr(pb,fonc,sol_voisins, o_t))
        while( mmr(pb,fonc,sol_voisins, o_t)[1] > eps):
            print("entrer ")
            (a,b) = demande(pb,fonc,sol,sol_voisins,w_etoile)
            theta.add((a,b))
            o_t = omega_theta(pb,fonc,theta) #achanger
            print("coc")
        if(mr(pb,fonc,sol,sol_voisins,o_t)[0] > eps):
            print("cocc")
            sol,_,_,_ = mmr(pb,fonc,sol_voisins,o_t)
            it += 1
        else:
            ameliore = False
    return sol,o_t,it
    
    #essaie
