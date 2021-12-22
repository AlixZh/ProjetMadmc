import numpy as np
class Node(object):
    """ presentation d'une solution non dominee dans le quadtree
        attribut
        solution: indice des objets d une solution
        v: vecteur des valeurs des solutions pour les objectifs
        k: chaine binaire
        sons: list de fils
        parent : node pere
        """
    def __init__(self,v,parent=None,k=None):
        #self.solution=solution
        self.v=np.array(v)
        self.sons=[]
        self.parent = parent
        self.k=np.array(k)

class QuadTree(object):
    """
    presentation des solutions non dominee dans le quadtree(maximisation)
    """
    def __init__(self,p,racine=None,nodes=[]):
        self.racine = racine
        self.nodes  = nodes
        self.p      = p

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
    def check_branch(self,racine_branch,list_reinsert=set()): 
        """
        racine_branch: type Node , racine de subtree  

        revoie subtree(list des nodes) d ou racine_branch est le racine

        """

        check_list=set(racine_branch.sons)
        for son in racine_branch.sons:
            if(son.sons!=[]):
                list_nodes=list_nodes|self.get_branch(son,list_nodes)
        return list_nodes
    def clear_tree(self):
        self.racine=None
        self.nodes=[]

    def insert_tree(self,node,racine_local=None):
        """
        verifier et ajouter un nouveau node non dominee dans le quadtree
        node: node a inserer
        racine_local: la racine de quadtree
        """

        if(racine_local==None):
            racine_local=self.racine
        if(self.racine==None):
            self.racine=node
            return True

        node.k=np.array([0]*self.p)
        node.k[np.where(node.v<=racine_local.v)]=1
        #a reflechir pour le cas  node.k==1
        if(np.all(node.k==1) or np.all(node.k==0)):
            return False
        s=racine_local.sons.copy()
        for son in s:
            #son domine node , pas besoin d inserer node
            if(np.all(node.k>=son.k) and np.all(node.v<=son.v)):
                return False
        for son in s:
            #son est domine par node, supprimer son, reinserer subtree de son 
            if(np.all(son.k>=node.k) and np.all(son.v<=node.v)):
                self.nodes.remove(son)
                racine_local.sons.remove(son)
                for s_son in self.get_branch(son):
                    s_son.parent=None
                    #s_son.sons=[]
                    self.nodes.remove(s_son)
                    self.insert_tree(s_son,self.racine)
        
        for son in racine_local.sons:
            #meme successorship , vefier s il y a dominance
            if(np.all(son.k==node.k)):
                #s il n y a pas dominance
                if(not all(node.v<=son.v)):
                    #print("-----------",son.k,node.k)
                    return self.insert_tree(node,son)
                else:
                    return True

        
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
        return True

'''
#test l'exemple de cours de en minimisation 
a=Node([10,10,10])
b=Node([5,5,23])
c=Node([6,16,22])
d=Node([14,18,6])
e=Node([9,8,18])
f=Node([3,25,16])
g=Node([11,15,9])
h=Node([40,16,7])
tree=QuadTree(3)
#print(a)
tree.insert_tree(a)
tree.insert_tree(b)
tree.insert_tree(c)
tree.insert_tree(d)
tree.insert_tree(e)
tree.insert_tree(f)
tree.insert_tree(g)
tree.insert_tree(h)
tree.insert_tree(Node([4,8,12]))
tree.insert_tree(Node([12,15,5]))
print(len(tree.get_branch(a)))
print(len(tree.nodes))
for node in tree.nodes:
    print("tree node2 ",node.v , "parent ",node.parent.v)
    for son in node.sons:
        print("22 enfant de ",node.v," : ",son.v," parent ",son.parent.v)


tree.clear_tree()
print(tree.nodes)

'''




