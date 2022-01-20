
import numpy as np
import matplotlib.pyplot as plt
import tools as ts
import quadtree as qdt

def PLS_elicitation(pb,x_init,p_init=ts.init_glouton,V=ts.voisinage,f=ts.y_sol):
    #print("x_init",x_init)
    racine=qdt.Node(x_init,f(pb,x_init),parent=None)
    racine.sons=[]
    Xe_approx=qdt.QuadTree(pb["p"],racine)#une approximation de l ensemble des solutions efficaces Xe
    Xe_approx.clear_tree()
    Xe_approx.racine=racine
    
    Pa=[]#population auxiliaire
    i=0
    #generation de tous les voisins pp de chaque solution p dans P
    v=V(pb,x_init)
    for pp in v:
        #si pp n est pas domine par p
        if(not all(f(pb,pp)<=f(pb,x_init))):
            #a modifier
            if(Xe_approx.insert_tree(qdt.Node(pp,f(pb,pp)))):
                Pa.append(pp)
    #print("P",P)
    X=[set(Xe_approx.racine.solution)]
    Y=[f(pb,Xe_approx.racine.solution)]
    for node in Xe_approx.nodes:
        #if(not check_set_in_list(node.solution,X)):
            #X.append(node.solution)
            #Y.append(node.v)
        X.append(node.solution)
        Y.append(node.v)
    return X,Y



def demande(voisinage_Y,preferences,w_etoile,fonc = ts.som_pond_Y,fonc_PMR=ts.PMR_SP):
    y_etoile,res = ts.MMR(voisinage_Y,preferences,fonc_PMR)
    ymr,res = ts.MR(y_etoile,voisinage_Y,preferences,fonc_PMR)
    if(ts.y_prefere_yprim(fonc,y_etoile,ymr,w_etoile)):
        return y_etoile,ymr
    return ymr,y_etoile

def rbls(pb,eps,max_it,w_etoile,f = ts.y_sol,fonc_ag = ts.som_pond_Y, fonc_PMR = ts.PMR_SP):
    """
    pb : dict des donnees du probleme considere
    implementation du regret-based local search
    renvoie la solution du sac a dos
    """
    sol = ts.init_glouton(pb)
    y_courant = f(pb,sol)
    it = 0
    nb_question = 0
    theta = []
    ameliore = True
    val_mmr = []
    while(ameliore and it < max_it) : 
        sol_voisins, y_sol_voisins = PLS_elicitation(pb,sol)
        while( ts.MMR(y_sol_voisins,theta,fonc_PMR)[1]> eps):
            (a,b) = demande(y_sol_voisins,theta,w_etoile,fonc_ag)
            theta.append((a,b))
            ind = np.where(np.array(y_sol_voisins) == b)[0][0]
            del y_sol_voisins[ind]
            del sol_voisins[ind]
            
            val_mmr.append(ts.MMR(y_sol_voisins,theta,fonc_PMR)[1])
            nb_question += 1
        if(ts.MR(y_courant,y_sol_voisins,theta,fonc_PMR)[1] > eps):
            y_courant,res = ts.MMR(y_sol_voisins,theta,fonc_PMR)
            sol = list(np.array(sol_voisins)[np.where(np.array(y_sol_voisins) == y_courant)[0][0]])
            it += 1
        else:
            ameliore = False
    return nb_question,sol, fonc_ag(w_etoile,y_courant),val_mmr,it
