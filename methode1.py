import tools as ts
import numpy as np
import matplotlib.pyplot as plt
import quadtree as qdt

def PLS(pb,p_init=ts.init_glouton,V=ts.voisinage,f=ts.y):
    x_init=p_init(pb)#population initiale

    racine=qdt.Node(x_init,ts.y(pb,x_init))
    Xe_approx=qdt.Quadtree(pb["p"],racine.copy())#une approximation de l ensemble des solutions efficaces Xe
    P=True
    Pa=qdt.Quadtree(pb["p"])#population auxiliaire

    while (P):
        #generation de tous les voisins pp de chaque solution p dans P
        for p in P:
            v=V(pb,P,p)
            for pp in v:
                #si pp n est pas domine par p
                if(f(pb,pp)<=f(pb,p)):
                    #a modifier
                    if(Xe_approx.insert_tree(Node(pp,ts.y(pb,pp)))):
                        Pa.insert_tree(Node(pp,ts.y(pb,pp)))

        P=(Pa.racine==None)

        Pa.clear_tree()



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
