
import numpy as np
from gurobipy import *
from itertools import chain, combinations
import time
import matplotlib.pyplot as plt

import quadtree as qdt
import tools as ts
import PL
import methode1 
import methode2 



class execution_methode1:
    """docstring for test_methode1"""
    def __init__(self,donnees = [],avec_pb = False):
        if(avec_pb):
            self.pb = donnees[0]
            self.poids_SP=donnees[1]
        else:
            data=ts.lire_fichier()
            self.pb=ts.get_pb_alea(data)
            self.poids_SP=ts.gen_poids(self.pb["p"])#alea
        self.poids_OWA=np.sort(self.poids_SP)[::-1]#ordre decroissant
        self.poids_IC=np.sort(self.poids_SP)[::-1]
        
    def une_experience_sp(self):
        start=time.time()
        nb_question,sol,opt_sp,list_mmr_en_iteration=methode1.solution_optimal(self.pb,self.poids_SP,fonc=ts.som_pond_Y,fonc_PMR=ts.PMR_SP)
        end=time.time()
        #sol_pl,opt_pl=PL.opt_pl_SP(self.pb,ts.som_pond,self.poids_SP)
        #return sol,sol_pl,end-start,nb_question,opt_pl-opt_sp,list_mmr_en_iteration
        return sol,end-start,nb_question,opt_sp
    
    def une_experience_owa(self):
        start=time.time()
        nb_question,sol,opt_owa,list_mmr_en_iteration=methode1.solution_optimal(self.pb,self.poids_OWA,fonc=ts.owa_Y,fonc_PMR=ts.PMR_OWA)
        end=time.time()
        #sol_pl,opt_pl=PL.opt_pl_OWA(self.pb,self.poids_OWA)
        #return sol,sol_pl,end-start,nb_question,opt_pl-opt_owa,list_mmr_en_iteration
        return sol,end-start,nb_question,opt_owa
    
class execution_methode2:
    """docstring for test_methode1"""
    def __init__(self,eps,max_it,donnees= [],avec_pb = False):
        if(avec_pb):
            self.pb = donnees[0]
            self.poids_SP=donnees[1]
        else:
            data=ts.lire_fichier()
            self.pb=ts.get_pb_alea(data)
            self.poids_SP=ts.gen_poids(self.pb["p"])#alea
        self.poids_OWA=np.sort(self.poids_SP)[::-1]#ordre decroissant
        self.max_it = max_it
        self.eps = eps
        #self.poids_IC=np.sort(self.poids_SP)[::-1]
        
    def une_experience_sp(self):
        start=time.time() 
        nb_question,sol,opt_sp,val_mmr,it = methode2.rbls(self.pb,self.eps,self.max_it,self.poids_SP,f = ts.y_sol,fonc_ag=ts.som_pond_Y,fonc_PMR=ts.PMR_SP)
        end=time.time()
        print(val_mmr)
        return sol,end-start,nb_question,opt_sp
    
    def une_experience_owa(self):
        start=time.time()
        nb_question,sol,opt_owa,val_mmr,it = methode2.rbls(self.pb,self.eps,self.max_it,self.poids_OWA,f=ts.y_sol,fonc_ag=ts.owa_Y,fonc_PMR=ts.PMR_OWA)
        end=time.time()
        print(val_mmr)
        return sol,end-start,nb_question,opt_owa
    
class execution_exacte:
    """docstring for test_methode1"""
    def __init__(self,donnees= [],avec_pb = False):
        if(avec_pb):
            self.pb = donnees[0]
            self.poids_SP=donnees[1]
        else:
            data=ts.lire_fichier()
            self.pb=ts.get_pb_alea(data)
            self.poids_SP=ts.gen_poids(self.pb["p"])#alea
        self.poids_OWA=np.sort(self.poids_SP)[::-1]#ordre decroissant
        #self.poids_IC=np.sort(self.poids_SP)[::-1]
        
    def une_experience_sp(self):
        start=time.time() 
        sol,opt=PL.opt_pl_SP(self.pb,ts.som_pond,self.poids_SP)
        end=time.time()
        return sol,end-start,opt
    
    def une_experience_owa(self):
        start=time.time()
        sol,opt=PL.opt_pl_OWA(self.pb,self.poids_OWA)
        end=time.time()
        return sol,end-start,opt
    
    
    
def main():
    data = ts.lire_fichier("./2KP200-TA-0.dat")
    mypb = ts.get_pb_alea(data)
    w_etoile = ts.gen_poids(mypb["p"])
    
    
    test_m=execution_methode1([mypb,w_etoile],True)
    print("---------------- test methode1 somme pondérée ------------------ ")
    print(" w* pour somme pondérée" ,test_m.poids_SP)
    x,temps,nb_question,y_ag=test_m.une_experience_sp()
    print("solution methode1 : ",x)
    print("temps de calcul : " , temps)
    print("nombre de questions posées : " ,nb_question)
    print("y_ag: ", y_ag)
    print("\n---------------- test methode1 owa --------------------------- ")
    print(" w* pour owa" ,test_m.poids_OWA)
    x,temps,nb_question,y_ag=test_m.une_experience_owa()
    print("solution methode1 : ",x)
    print("temps de calcul : " , temps)
    print("nombre de questions posées : " ,nb_question)
    print("y_ag: ", y_ag)
    
    
    test_m=execution_exacte([mypb,w_etoile],True)

    print("---------------- test methode_exacte somme pondérée ------------------ ")
    print(" w* pour somme pondérée" ,test_m.poids_SP)
    x,temps,y_ag=test_m.une_experience_sp()
    print("solution methode1 : ",x)
    print("temps de calcul : " , temps)
    print("y_ag: ", y_ag)
    print("\n---------------- test methode_exacte owa --------------------------- ")
    print(" w* pour owa" ,test_m.poids_OWA)
    x,temps,y_ag=test_m.une_experience_owa()
    print("solution methode1 : ",x)
    print("temps de calcul : " , temps)
    print("y_ag: ", y_ag)
    
    
    
    test_m=execution_methode2(0.1,100,[mypb,w_etoile],True)

    print("---------------- test methode2 somme pondérée ------------------ ")
    print(" w* pour somme pondérée" ,test_m.poids_SP)
    x,temps,nb_question,y_ag=test_m.une_experience_sp()
    print("solution methode2 : ",x)
    print("temps de calcul : " , temps)
    print("nombre de questions posées : " ,nb_question)
    print("y_ag: ", y_ag)
    print("\n---------------- test methode2 owa --------------------------- ")
    print(" w* pour owa" ,test_m.poids_OWA)
    x,temps,nb_question,y_ag=test_m.une_experience_owa()
    print("solution methode2 : ",x)
    print("temps de calcul : " , temps)
    print("nombre de questions posées : " ,nb_question)
    print("y_ag: ", y_ag)


if __name__ == "__main__":
    for i in range(10):
        main()
