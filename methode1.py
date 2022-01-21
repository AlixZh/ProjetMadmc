import tools as ts
import numpy as np
import matplotlib.pyplot as plt
import quadtree as qdt
def PLS(pb,p_init=ts.init_glouton,V=ts.voisinage,f=ts.y_sol):
    """la recherche locale de Pareto,
    donner une approximation des points non-dominés (au sens de Pareto)
    pb:dict du pb considere
    p_init:fonction retourne une solution initialement réalisable
    V: fonction donne la voisinage d'une solution
    f: fonction d'evaluation de la solution
    revoie X:ensemble des solutions non dominée,Y: ensemble d'evaluations de X
    """
    x_init=p_init(pb)#population initiale
    racine=qdt.Node(x_init,f(pb,x_init),parent=None)
    racine.sons=[]
    Xe_approx=qdt.QuadTree(pb["p"],racine)#une approximation de l ensemble des solutions efficaces Xe
    
    Xe_approx.clear_tree()
    Xe_approx.racine=racine
    P=[x_init]
    Pa=[]#population auxiliaire
    i=0
    while (P!=[]):
        #generation de tous les voisins pp de chaque solution p dans P
        for p in P:
            v=V(pb,p)
            for pp in v:
                #si pp n est pas domine par p
                if(not all(f(pb,pp)<=f(pb,p))):
                    if(Xe_approx.insert_tree(qdt.Node(pp,f(pb,pp)))):
                        Pa.append(pp)
        P=Pa.copy()
        Pa=[]
    X=[set(Xe_approx.racine.solution)]
    Y=[f(pb,Xe_approx.racine.solution)]
    for node in Xe_approx.nodes:
        X.append(node.solution)
        Y.append(node.v)
    return X,Y


def solution_optimal(pb,lambda_etoile,fonc=ts.som_pond_Y,fonc_PMR=ts.PMR_SP):
    """
    Y : ensemble d'evaluation de solutions generer par PLS
    fonc : fonction d'aggregation 
    lambda_etoile : vecteur poids pour decideur
    fonc_PMR: programmation lineaire de pmr pour un type de fonction aggregation(PMR_SP:somme pondérée, PMR_OWA:OWA ou PMR_IC:l’intégrale de Choquet)
    revoie (nombre de questions posées,solution x,optimale de fonction d'agregation obtenu,liste de mmr en fonction de nombre question posée)
    """
    X,Y=PLS(pb)
    P=[]
    y,val_mmr=ts.MMR(Y,fonc_pmr=fonc_PMR)
    yprim,val_mr=ts.MR(y,Y,fonc_pmr=fonc_PMR)
    list_mmr_en_iteration=[val_mmr]
    i=0#nb de question posé
    while (val_mmr>0. and i<len(Y)):
        if(ts.y_prefere_yprim(fonc,y,yprim,lambda_etoile)):
            P.append((y,yprim))
            ind = np.where(np.array(Y) == yprim)[0][0]
            del Y[ind]
            del X[ind]
        else:
            P.append((yprim,y))
            ind = np.where(np.array(Y) == y)[0][0]
            del Y[ind]
            del X[ind]
        y,val_mmr=ts.MMR(Y,P=P,fonc_pmr=fonc_PMR)
        yprim,val_mr=ts.MR(y,Y,P=P,fonc_pmr=fonc_PMR)
        i+=1
        list_mmr_en_iteration.append(val_mmr)    
    sol=[]
    for j in range(len(Y)):
        if(np.all(y==Y[j])):
            sol=X[j]
    return i,sol,fonc(lambda_etoile,y),list_mmr_en_iteration




