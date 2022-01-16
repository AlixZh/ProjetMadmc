import tools as ts
import numpy as np
import matplotlib.pyplot as plt
import quadtree as qdt
import methode2 as m2
from gurobipy import *
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

def PLS(pb,p_init=ts.init_glouton,V=ts.voisinage,f=ts.y):
    x_init=p_init(pb)#population initiale
    #print("x_init",x_init)
    racine=qdt.Node(x_init,f(pb,x_init))
    Xe_approx=qdt.QuadTree(pb["p"],racine)#une approximation de l ensemble des solutions efficaces Xe
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
                    #a modifier
                    if(Xe_approx.insert_tree(qdt.Node(pp,f(pb,pp)))):
                        Pa.append(pp)
        P=Pa.copy()
        Pa=[]
        #print("P",P)
    X=[set(x_init)]
    Y=[f(pb,x_init)]
    for node in Xe_approx.nodes:
        X.append(node.solution)
        Y.append(node.v)

    return X,Y

def PMR_SP(x,y,P=[]):
    """
    x(array) : une evaluation d'une solution realisable
    y(array) : une autre evaluation
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie tuple(array,float):lambda qui donne le max regret (y-x),et la valeur de max regret
    """
    env = Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    if(len(x)!=len(y)):
        print ("erreur len(x)!=len(y)")
    nbvar=len(x) #nombre d objet possible
    colonnes = range(nbvar)

    #matrice des contraintes
    a = [1]*nbvar
    # Second membre
    b = 1.0
    #parametre de fonction objectif
    c=(y-x)

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
    #print("obj ",obj)
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    #print(m)
    # Definition des contraintes
    m.addConstr(quicksum(lambda_[j]*a[j] for j in colonnes) <= b, "Contrainte%d" % 1)
    for x1,y1 in P:
        m.addConstr(quicksum(lambda_[j]*(y1-x1)[j] for j in colonnes) <= 0.0)

    # Resolution
    m.optimize()
    # print("")                
    # print('Solution optimale:')
    res=np.array([0.0]*nbvar)
    for j in colonnes:
        res[j]=lambda_[j].X
    # print("")
    # print('Valeur de la fonction objectif :', m.objVal)
    return res,m.objVal

def PMR_OWA(xx,yy,P=[]):
    """
    x(array) : une evaluation d'une solution realisable
    y(array) : une autre evaluation
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie tuple(array,float):lambda qui donne le max regret (y-x),et la valeur de max regret
    """
    env = Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()

    x=xx.copy()
    y=yy.copy()
    x.sort()
    y.sort()
    if(len(x)!=len(y)):
        print ("erreur len(x)!=len(y)")
    nbvar=len(x) #nombre d objet possible
    colonnes = range(nbvar)

    #matrice des contraintes
    a = [1]*nbvar
    # Second membre
    b = 1.0
    #parametre de fonction objectif
    c=(y-x)

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
    #print("obj ",obj)
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    #print(m)
    # Definition des contraintes
    m.addConstr(quicksum(lambda_[j]*a[j] for j in colonnes) == 1, "Contrainte%d" % 1)#somme lambda=1
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
    # print("")                
    # print('Solution optimale:')
    res=np.array([0.0]*nbvar)
    for j in colonnes:
        res[j]=lambda_[j].x
    # print("")
    # print('Valeur de la fonction objectif :', m.objVal)
    return res,m.objVal

def MR(x,X,P=[],fonc_pmr=PMR_SP):
    """
    x(array) : une evaluation d'une solution realisable
    X(list(array)) : ensemble d'evaluations possibles
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    fonc_pmr : programmation lineaire de pmr pour un type de fonction aggregation(PMR_SP:somme pondérée, PMR_OWA:OWA ou PMR_IC:l’intégrale de Choquet)
    revoie tuple(list,float): y dans list X telle qu'il maximise (pmr)(le pire des regrets associé à la recommandation de l'alternative x à la place
de toute autre alternative dans X ), et la valeur max
    """

    arg_res_mr=np.array([0.0]*len(x))
    res_mr=float("-inf")
    for y in X:
        if(np.all(x==y)):
            continue
        # if((x,y) in P):
        #     continue
        arg_res_pmr,res_pmr=fonc_pmr(x,y,P)
        if(res_pmr>=res_mr):
            arg_res_mr=y
            res_mr=res_pmr
    return arg_res_mr,res_mr
def MMR(X,P=[],fonc_pmr=PMR_SP):
    """
    X(list(array)) : ensemble d'evaluations possibles
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie array,float : x dans X qui donne Minimax Regret et minimax regret
    """
    arg_res_mmr=np.array([0.0]*len(X[0]))
    res_mmr=float("inf")
    for x in X:
        arg_res_mr,res_mr=MR(x,X,P,fonc_pmr)
        if(res_mr<=res_mmr):
            arg_res_mmr=x
            res_mmr=res_mr
    return arg_res_mmr,res_mmr


def solution_optimal(pb,X,lambda_etoile,fonc=som_pond_Y,fonc_PMR=PMR_SP):
    """
    X : ensemble de solutions generer par PLS
    fonc : fonction d'aggregation 
    lambda_etoile : vecteur poids pour decideur
    fonc_PMR: programmation lineaire de pmr pour un type de fonction aggregation(PMR_SP:somme pondérée, PMR_OWA:OWA ou PMR_IC:l’intégrale de Choquet)
    """
    P=[]
    xp_etoile,val_xp=MMR(X,fonc_pmr=fonc_PMR)
    yp_etoile,val_yp=MR(xp_etoile,X,fonc_pmr=fonc_PMR)
    if(x_prefere_y(pb,fonc,xp_etoile,yp_etoile,lambda_etoile)):
        P.append((xp_etoile,yp_etoile))
    else:
        P.append((yp_etoile,xp_etoile))
    i=0
    while (MMR(X,P=P,fonc_pmr=fonc_PMR)[1]>0. and i<10):
        xp_etoile,val_xp=MMR(X,P=P,fonc_pmr=fonc_PMR)
        yp_etoile,val_yp=MR(xp_etoile,X,P=P,fonc_pmr=fonc_PMR)
        if(x_prefere_y(pb,fonc,xp_etoile,yp_etoile,lambda_etoile)):
            P.append((xp_etoile,yp_etoile))
        else:
            P.append((yp_etoile,xp_etoile)) 
        i+=1    
    print(i)  
    return xp_etoile

def x_prefere_y(pb,fonc,a,b,lambda_etoile):
    """
    demander au decideur si il prefere a à b
    """
    #print("a ",a)
    #print("b",b)
    fw_a = fonc(lambda_etoile,a)
    fw_b = fonc(lambda_etoile,b)
    if(np.all(fw_a > fw_b)):
        return True
    return False



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
