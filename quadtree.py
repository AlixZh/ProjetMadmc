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
    def __init__(self,solution,v,parent=None,k=None):
        self.solution=solution
        self.v=np.array(v)
        self.sons=[]
        self.parent = parent
        self.k=np.array(k)
    def clear_node(self):
        self.sons=[]
        self.parent =None
        self.k=None       
class QuadTree(object):
    """
    presentation des solutions non dominee dans le quadtree(maximisation)
    racine : type node
    nodes : list des nodes les solutions non dominee sans racine
    p : nb de critere
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
    def clear_tree(self):
        self.racine=None
        self.nodes=[]
        for node in self.nodes:
            node.clear_node()
    def check_dominance(self,node,k,racine_local):
        """
        vefifier si node est domine par les nodes dans la branch ou racine_local est le racine
        node : Node
        k : chaine binaire courant pour node
        racine_local :Node 
        """

        if(np.all(k>=racine_local.k)):
            if(np.all(node.v<=racine_local.v)):
                return True
            else:
                for son in racine_local.sons:
                    k1=np.array([0]*self.p)
                    k1[np.where(node.v<=racine_local.v)]=1
                    if(self.check_dominance(node,k1,son)):
                        return True
        return False
    def check_dominated(self,node,k,racine_local):
        """
        trouver les nodes dominee par node
        node : Node
        k : chaine binaire
        racine_local : Node

        """
        if(racine_local not in self.nodes):
            return False,None
        value=[]
        if(np.all(racine_local.k>=k)):
            if(np.all(racine_local.v<=node.v)):
                return True,[racine_local]
            else:
                for son in racine_local.sons:
                    k1=np.array([0]*self.p)
                    k1[np.where(node.v<=racine_local.v)]=1
                    condition,value1=self.check_dominated(node,k1,son)
                    if(condition):
                        value+=value1
            if(len(value)!=0):
                return True,value

        return False,None
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
        if(np.all(node.k==1)):
            return False
        if(np.all(node.k==0)):
            if(np.all(node.v==racine_local.v)):
                return False
            self.racine=node
            node_a_inserer=[]
            for node1 in self.nodes:
                self.nodes.remove(node1)
                node1.parent=None
                node1.sons=[]
                node1.k=None
                node_a_inserer.append(node1)
            for node2 in node_a_inserer:
                self.insert_tree(node2)
            return True
        s=racine_local.sons.copy()
        #chercher sur la branch ou la racine.k>=node.k(ou c'est possible avoir dominance)
        for son in racine_local.sons:
            if(self.check_dominance(node,node.k,son)):
                return False

        #chercher si les noeuds sont dominee par node
        list_node_reinserer=[]
        for son in racine_local.sons:
            isdominee,subtrees=self.check_dominated(node,node.k,son)
            #son est domine par node, supprimer son, reinserer subtree de son 
            if(isdominee):
                for subtree in subtrees:
                    if(subtree not in self.nodes):
                        continue
                    self.nodes.remove(subtree)
                    subtree.parent.sons.remove(subtree)
                    subtree.clear_node()
                    li=self.get_branch(subtree)
                    for s_son in li:
                        s_son.clear_node()
                        self.nodes.remove(s_son)
                        list_node_reinserer.append(s_son)
        for son in racine_local.sons:
            #meme successorship , vefier s il y a dominance
            if(np.all(son.k==node.k)):
                #si node est dominee
                if(np.all(node.v<=son.v)):
                    for i in range(len(list_node_reinserer)):
                        n=list_node_reinserer[i]
                        self.insert_tree(n,self.racine)
                    return False
                if(self.insert_tree(node,son)):
                    for i in range(len(list_node_reinserer)):
                        n=list_node_reinserer[i]
                        self.insert_tree(n,self.racine)
                    return True
        #inserer node
        for n in self.nodes:
            if(np.all(node.v==n.v)):
                return False
        if(node.parent==None):
            node.parent=racine_local
            racine_local.sons.append(node)
            self.nodes.append(node)
        else:
            if(node.parent!=racine_local):
                node.parent.sons.remove(node)
                node.parent=racine_local
                racine_local.sons.append(node)
        for i in range(len(list_node_reinserer)):
            n=list_node_reinserer[i]
            self.insert_tree(n,self.racine)

        return True


