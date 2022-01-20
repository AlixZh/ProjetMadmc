
import numpy as np
import matplotlib.pyplot as plt





"""
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
"""
    
    
 def rbls(pb,eps,max_it,w_etoile,fonc_ag = som_pond_Y, fonc_pmr = PMR_SP):
    """
    pb : dict des donnees du probleme considere
    implementation du regret-based local search
    renvoie la solution du sac a dos
    """
    sol = init_glouton(pb)
    print("sol ",sol)
    y_courant = y_sol(pb,sol)
    print("ycourant : ",y_courant)
    it = 0
    theta = []
    ameliore = True

    while(ameliore and it < max_it) : 
        sol_voisins = voisinage(pb, sol)
        y_sol_voisins = [y_sol(pb,xx) for xx in sol_voisins] #sol des criteres
        print("nb question : ",it)
        while( MMR(y_sol_voisins,theta,fonc_pmr)[1]> eps):
            print(MMR(y_sol_voisins,theta,fonc_pmr)[1])
            (a,b) = demande(y_courant,y_sol_voisins,theta,w_etoile,fonc_ag)
            theta.append((a,b))
        if(MR(y_courant,y_sol_voisins,theta,fonc_pmr)[1] > eps):
            y_courant,res = MMR(y_sol_voisins,theta,fonc_pmr)
            print(y_sol_voisins,y_courant)
            print("where : ",np.where(np.array(y_sol_voisins)== y_courant))
            sol = list(np.array(sol_voisins)[np.where(np.array(y_sol_voisins) == y_courant)[0][0]])
            print("nv sol : ",sol)
            it += 1
        else:
            ameliore = False
    return sol,it
      
    
 def ri(pb,i,qi):
    res = 0
    for vi in range(pb["p"]):
        res += qi[vi]*pb["v"][i][vi]
    return res/pb["wi"][i]
