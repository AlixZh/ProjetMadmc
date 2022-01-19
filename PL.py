from gurobipy import *
import numpy as np
import tools as ts


def opt_pl_SP(pb,fonc,w):
    """
    pb : dict du pb considere
    fonc : fonction d agregation
    w : liste des poids
    """
    nbvar=pb["n"] #nombre d objet possible
    colonnes = range(nbvar)


    #matrice des contraintes
    a = pb["wi"]
    # Second membre
    b = pb["W"]

    env = Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()
    m = Model("SD",env=env)     

    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name="x%d" % (i)))

    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = LinExpr();
    obj = fonc(pb,w,x,False)
    #print("obj ",obj)
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    #print(m)
    # Definition des contraintes
    m.addConstr(quicksum(a[j]*x[j] for j in colonnes) <= b, "Contrainte%d" % 1)

    # Resolution
    m.optimize()


    # print("")                
    # print('Solution optimale:')
    # for j in colonnes:
    #     print('x%d'%(j+1), '=', x[j].x)
    # print("")
    # print('Valeur de la fonction objectif :', m.objVal)
    return m.objVal


def opt_pl_OWA(pb,w):
    """
    pb : dict du pb considere
    w : liste des poids
    """

    env = Env(empty=True)
    env.setParam("OutputFlag",0)
    env.start()
    m = Model("OWA",env=env)
    # declaration variables de decision
    r=[]
    x = []
    b=[]
    N=range(pb["n"])
    P=range(pb["p"])
    for i in N:
        x.append(m.addVar(vtype=GRB.BINARY, lb=0,ub=1, name="x%d" % (i)))
    for i in P:
        r.append(m.addVar(vtype=GRB.CONTINUOUS,name="r%d" % (i)))
    for i in P:
        bi=[]
        for j in P:
            bi.append(m.addVar(vtype=GRB.BINARY, lb=0, ub=1, name="b%d" % (i*10+j)))
        b.append(bi)
    # maj du modele pour integrer les nouvelles variables

    m.update()

    obj = LinExpr();
    obj =quicksum(w[j]*r[j] for j in P)
    #print("obj ",obj)
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    #print(m)
    # Definition des contraintes

    m.addConstr(quicksum(pb["wi"][j]*x[j] for j in N) <= pb["W"])
    y=LinExpr();
    y=ts.y_sol(pb,x,list_ind = False)
    #grand nombre M M is a sufficiently large constant (larger than any possible difference between various indi- vidual outcomes yi)
    M=10000
    for i in P:
        for k in P:
            m.addConstr(r[k]<=y[i]+M*b[i][k])
    for k in P:
        m.addConstr(quicksum(b[i][k] for i in P)==k)

    #m.addConstr(quicksum(a[j]*x[j] for j in colonnes) <= b, "Contrainte%d" % 1)

    # Resolution
    m.optimize()


    # print("")                
    # print('Solution optimale:')
    # for j in N:
    #     print('x%d'%(j+1), '=', x[j].x)
    # print("")
    # print('Valeur de la fonction objectif :', m.objVal)    
    return m.objVal

