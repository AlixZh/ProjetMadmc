import numpy as np
class Node(object):
    """ presentation d'une solution non dominee dans le quadtree
        attribut
        v: vecteur des objectif
        k: chaine binaire
        sons: list de fils
        parent : node pere
        """
    def __init__(self,v,parent=None,k=None):
        self.v=np.array(v)
        self.sons=[]
        self.parent = parent
        self.k=np.array(k)

class QuadTree(object):
    """
    presentation des solutions non dominee dans le quadtree(maximisation)
    """
    def __init__(self,racine,p,nodes=[]):
        self.racine = racine
        self.nodes  = nodes
        self.p      = p
    def insert_tree(self,node,racine_local):
        """
        verifier et ajouter un nouveau node non dominee dans le quadtree
        node: node a inserer
        racine_local: la racine de quadtree
        """
        node.k=np.array([0]*self.p)
        node.k[np.where(node.v<=racine_local.v)]=1
        if(np.all(node.k==1) or np.all(node.k==0)):
            return
        s=racine_local.sons.copy()
        for son in s:
            #son est domine par node, supprimer son, reinserer les fils de son 
            if(np.all(son.k>=node.k) and np.all(son.v<=node.v)):
                self.nodes.remove(son)
                racine_local.sons.remove(son)
                for s_son in son.sons:
                    s_son.parent=None
                    self.nodes.remove(s_son)
                    self.insert_tree(s_son,self.racine)
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
'''
test l'exemple de cours de en minimisation 
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

'''







