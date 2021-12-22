import numpy as np
def add_set_in_list(set1,list2):
    """
    ajouter un set dans un list de set si :
    il n est pas dedans et 
    il n est pas un subset de set dans list

    """
    if(set1 not in list2):
        add=True
        for s in list2:
            if(set1.issubset(s)):
                add=False
                break
        if(add==True):
            list2.append(set1)


def echange_11(pb,x_init,obj_retire):
    """
    pb : une liste des donnees du probleme
    x_init : une solution trouve solution 
    obj_retire : 
    renvoie la voisinage de cette solution
    """
    list_x_change=[]
    nb_obj=pb["n"]
    w_=pb["wi"]#liste poids

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
                obj_poss=list(np.where(w_<=(W-poids_poss))[0])

                print("obj_poss",obj_poss,obj,obj_retire)
                for op in obj_poss:
                    if(op==obj or op==obj_retire):
                        continue
                    if(w_[op]+poids_poss<=W):
                        poids_poss+=w_[op]
                        L_.add(op)
                add_set_in_list(L_,list_x_change)

    print("obj_retire",obj_retire,list_x_change)
    return list_x_change

def voisinage(pb,x_init):
    list_voisinage=[]
    for obj in x_init:
        list_x_change=echange_11(pb,x_init,obj)
        for x in list_x_change:
            add_set_in_list(x,list_voisinage)
    return list_voisinage

def init_glouton(pb):
    somme_yi = np.sum(pb["v"],1) / pb["p"] #somme des vp des criteres a considerer
    indice=np.argsort(somme_yi)  #trier la moyenne arithmetique de chaque objet
    i = pb["n"]-1
    sol=[] #liste contient les indices des objets prises
    s = 0  #somme des poids des objets ajouter dans sol      
    while(i >= 0):
        if (s + pb["wi"][i] <= pb["W"]):
            s += pb["wi"][i]  
            sol.append(indice[i])
        i -= 1
    return sol

pb={}
pb["n"]=5
pb["wi"]=[1,2,3,4,5]#liste poids
pb["W"]=10
pb["v"]=[[1,2,3],[3,2,1],[3,4,1],[4,3,2],[5,1,2]]
pb["p"]=3
x_init=init_glouton(pb)
print(x_init)

print(voisinage(pb,x_init))

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
