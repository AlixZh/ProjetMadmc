import tools as ts
import numpy as np
import matplotlib.pyplot as plt

def voisinage(pb,x_init,obj_retire):
    """
    pb : une liste des donnees du probleme
    x_init : une solution trouve solution 
    obj_retire : 
    renvoie la voisinage de cette solution
    """
    list_x_change=[]
    nb_obj=pb["n"]
    w_=pb["wi"]#liste poids
    v_=pb["v"]#liste profit
    W=pb["W"]
    L=x_init.copy()
    L.remove(obj_retire)
    poids_=np.sum([w_[i] for i in x_init],axis=0)-w_[obj_retire]#poids sans obj_retire
    for obj in range(nb_obj) :
        L_=set(L.copy())

        if(obj not in x_init):
            if(w_[obj]+poids_<=W):
                #echange 1-1
                L_.add(obj)
                #des on peut encore ajouter des objets
                poids_poss=w_[obj]+poids_
                wi=w_.copy()
                wi.pop(obj)
                wi.pop(obj_retire)
                obj_poss=list(np.where(wi<=(W-poids_poss))[0])
                print(obj_poss,obj,obj_retire)
                for op in obj_poss:
                    if(w_[obj]+poids_poss<=W):
                        poids_poss+=w_[obj]
                        L_.add(op)
                if(L_ not in list_x_change):
                    list_x_change.append(L_)

    return list_x_change

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


class Node(object):
    """docstring for Node"""
    def __init__(self,v,sons=[],parent=None,k=None):
        self.v=np.array(v)
        self.sons=sons.copy()#nodes
        self.parent = parent
        self.k=np.array(k)

        
class QuadTree():
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
        for son in racine_local.sons:
                        #son est domine par node, supprimer son, reinserer les fils de son 
            if(np.all(son.k>=node.k) and np.all(son.v<=node.v)):
                self.nodes.remove(son)
                racine_local.sons.remove(son)
                for s_son in son.sons:
                    #s_son.parent=None
                    #self.nodes.remove(s_son)
                    self.insert_tree(s_son,racine_local)
            
        for son in racine_local.sons:
            
            #son domine node , pas besoin d inserer node
            if(np.all(node.k>=son.k) and np.all(node.v<=son.v)):
                return


            #meme successorship , vefier s il y a dominance
            if(np.all(son.k==node.k)):
                #s il n y a pas dominance
                if(not all(node.v<=son.v)):
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



