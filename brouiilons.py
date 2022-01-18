import numpy as np
import tools as ts
import methode1
import PL
from gurobipy import *
data=ts.lire_fichier()
pb=ts.get_pb_alea(data)
#print(pb)
X,Y=methode1.PLS(pb)
lambda_etoile=ts.gen_poids(pb["p"])
#print(X,Y,lambda_etoile)
x=np.array([4,3,1,5])
y=np.sort(x)[::-1]
print(x,y)

from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
#print(list(powerset([1,2,3])))


def PMR_IC(x,y,P=[]):
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

    #tous les sous-emsembles 
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







'''
def PMR_SP(x,y,P=[]):
    """
    x(array) : une evaluation d'une solution realisable
    y(array) : une autre evaluation
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie tuple(array,float):lambda qui donne le max regret (y-x),et la valeur de max regret
    """
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

    m = Model("PMR_SP")     
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
    m.addConstr(quicksum(lambda_[j]*a[j] for j in colonnes) == b, "Contrainte%d" % 1)
    for x1,y1 in P:
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


def PMR_OWA(x,y,P=[]):
    """
    x(array) : une evaluation d'une solution realisable
    y(array) : une autre evaluation
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie tuple(array,float):lambda qui donne le max regret (y-x),et la valeur de max regret
    """
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

    m = Model("PMR_SP")     
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
    for x1,y1 in P:
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
def PMR_IC(x,y,P=[]):
    """
    x(array) : une evaluation d'une solution realisable
    y(array) : une autre evaluation
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie tuple(array,float):lambda qui donne le max regret (y-x),et la valeur de max regret
    """
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

    m = Model("PMR_SP")     
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
    for x1,y1 in P:
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

def mr(x,X,P=[],fonc_pmr=PMR_SP):
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
def mmr(X,P=[],fonc_pmr=PMR_SP):
    """
    X(list(array)) : ensemble d'evaluations possibles
    lambda_min(float) : borne inf de lambda possible( lambda_ parametre d'aggregation)
    lambda_max(float) : borne sup de lambda possible
    revoie array,float : x dans X qui donne Minimax Regret et minimax regret
    """
    arg_res_mmr=np.array([0.0]*len(X[0]))
    res_mmr=float("inf")
    for x in X:
        arg_res_mr,res_mr=mr(x,X,P,fonc_pmr)
        if(res_mr<=res_mmr):
            arg_res_mmr=x
            res_mmr=res_mr
    return arg_res_mmr,res_mmr

x=np.array([0.0,4.0,3.0])
y=np.array([3.0,2.0,1.0])
z=np.array([4.0,1.0,3.0])
#x.sort()
print(PMR_SP(x,z,P=[(x,y)]))
#print(PMR_OWA(x,z,P=[(x,y)]))
#print(len(x))
#print(mmr([x,y,z],[(x,z),(z,y)]))

'''


# pb={}
# pb["n"]=5
# pb["wi"]=[1,2,3,4,5]#liste poids
# pb["W"]=10
# pb["v"]=[[1,2,3],[3,2,1],[3,4,1],[4,3,2],[5,1,2]]
# pb["p"]=3
# x_init=ts.init_glouton(pb)
# print(x_init)

# print(ts.voisinage(pb,x_init))

'''
class Node(object):
    """docstring for Node"""
    def __init__(self,v,parent=None,k=None):
        self.v=np.array(v)
        self.sons=[]
        self.parent = parent
        self.k=np.array(k)

class QuadTree(object):
    """docstring for QuadTree"""
    def __init__(self,racine,p,nodes=[]):
        self.racine = racine
        self.nodes  = nodes
        self.p      = p
    def insert_tree(self,node,racine_local):

        node.k=np.array([0]*self.p)
        node.k[np.where(node.v>=racine_local.v)]=1
        if(np.all(node.k==1) or np.all(node.k==0)):
            return
        s=racine_local.sons.copy()
        for son in s:
            #son est domine par node, supprimer son, reinserer les fils de son 
            if(np.all(son.k>=node.k) and np.all(son.v>=node.v)):
                self.nodes.remove(son)
                racine_local.sons.remove(son)
                for s_son in son.sons:
                    s_son.parent=None
                    self.nodes.remove(s_son)
                    self.insert_tree(s_son,self.racine)
        for son in racine_local.sons:
            
            #son domine node , pas besoin d inserer node
            if(np.all(node.k>=son.k) and np.all(node.v>=son.v)):
                return

            #meme successorship , vefier s il y a dominance
            if(np.all(son.k==node.k)):
                #s il n y a pas dominance
                if(not all(node.v>=son.v)):
                    #print("-----------",son.k,node.k)
                    return self.insert_tree(node,son)
                else:
                    return

        
        #inserer node
        if(node.parent==None):
            node.parent=racine_local
            racine_local.sons.append(node)
            self.nodes.append(node)
        else:
            if(node.parent!=racine_local):
                node.parent.sons.remove(node)
                node.parent=racine_local
                racine_local.sons.append(node)
        




a=Node([10,10,10])
b=Node([5,5,23])
c=Node([6,16,22])
d=Node([14,18,6])
e=Node([9,8,18])
f=Node([3,25,16])
g=Node([11,15,9])
h=Node([40,16,7])
tree=QuadTree(a,3)
#print(a)
tree.insert_tree(b,a)
tree.insert_tree(c,a)
tree.insert_tree(d,a)
tree.insert_tree(e,a)
tree.insert_tree(f,a)
tree.insert_tree(g,a)
tree.insert_tree(h,a)
tree.insert_tree(Node([4,8,12]),a)
tree.insert_tree(Node([12,15,5]),a)

print(len(tree.nodes))
for node in tree.nodes:
    print("tree node2 ",node.v , "parent ",node.parent.v)
    for son in node.sons:
        print("22 enfant de ",node.v," : ",son.v," parent ",son.parent.v)




    def check_branch_dominant(self,node,racine_branch):
        
        """

        racine_branch: type Node , racine de subtree 
        node :         type Node , nouveau node qu'on veux inserer
        
        verifer si les nodes dans cette branche domine node
        
        revoie true si ce nouveau node est dominee 

        """
        if(np.all(node.v>=racine_branch.v)):
            
        list_nodes=set([racine_branch])|set(racine_branch.sons)
        for son in racine_branch.sons:
            if(son.sons!=[]):
                list_nodes=list_nodes|self.recherche_branch(son,list_nodes)
        return list_nodes



class QuadTree():
    """docstring for QuadTree"""
    def __init__(self,racine,p):
        self.racine = racine
        self.nodes  = [racine]
        self.p      = p
    def getNode(self,node):
        for n in self.nodes:
            if(n==node):
                return n
    def get_branch(self,racine_branch,list_nodes=set()): 
        """
        racine_branch: type Node , racine de subtree  

        revoie subtree(list des nodes) d ou racine_branch est le racine

        """
        list_nodes=list_nodes|set(racine_branch.sons)
        for son in racine_branch.sons:
            if(son.sons!=[]):
                list_nodes=list_nodes|self.get_branch(son,list_nodes)
        return list_nodes

    def insert_tree(self,node,racine_local):
        node.k=np.array([0]*self.p)
        node.k[np.where(node.v>=racine_local.v)]=1
        if(np.all(node.k==1) or np.all(node.k==0)):
            return

        for son in racine_local.sons:
            
            #son domine node , pas besoin d inserer node
            if(np.all(node.k>=son.k) and np.all(node.v>=son.v)):
                return
        
        #inserer node
        if(node.parent!=None):
            node.parent.sons.remove(node)
            #node.parent=racine_local
            #print("111==== node inserer",node.v,"parent",len(node.parent.sons),"get ",self.getNode(node.parent).v)
        node.parent=racine_local
        #print("1222 racine local ",racine_local.v,"sons " ,[son.v for son in racine_local.sons] ," node inserer",node.v,"parent",node.parent.v," k ", node.k)
        racine_local.sons.append(node)
        if(racine_local.v[0]==5):
            print("enfant de ",racine_local.v," nb ",len(racine_local.sons))
        for son in racine_local.sons:
            if(son !=node):
                if(racine_local.v[0]==5):

                    print("ahhhhhhhhhhenfant de ",racine_local.v," nb ",[son.v for son in racine_local.sons])
        #meme successorship , vefier s il y a dominance
                if(np.all(son.k==node.k)):
                    #s il n y a pas dominance
                    if(not all(node.v>=son.v)):
                        #print("-----------",son.v,node.v)
                        self.insert_tree(node,son)


        for son in racine_local.sons:
            if(son !=node):

                #son est domine par node, supprimer son, reinserer tous les noeuds dans cet subtree
                if(np.all(son.k>=node.k) and np.all(son.v>=node.v)):
                    self.nodes.remove(son)
                    racine_local.sons.remove(son)
                    for s_son in son.sons:
                        self.insert_tree(s_son,racine_local)
                

'''