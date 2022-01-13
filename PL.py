from gurobipy import *
import numpy as np



def opt_pl(pb,fonc,w):
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


    m = Model("SD")     

    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name="x%d" % (i+1)))

    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = LinExpr();
    obj = fonc(pb,w,x,False)
    print("obj ",obj)
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    print(m)
    # Definition des contraintes
    m.addConstr(quicksum(a[j]*x[j] for j in colonnes) <= b, "Contrainte%d" % 1)

    # Resolution
    m.optimize()


    print("")                
    print('Solution optimale:')
    for j in colonnes:
        print('x%d'%(j+1), '=', x[j].x)
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
