import numpy as np
import tools as ts
import methode1
import PL
from gurobipy import *
from itertools import chain, combinations
import time
# def powerset(iterable):
#     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#     s = list(iterable)
#     return [set(list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))[i]) for i in range(len(s)+1)]
# n=3
# w=ts.gen_poids(n)
# ens=powerset(range(n))
# v=[0]*(2**n)
# v[-1]=1

# for i in range(1,n):
#     v[i]=w[i-1]
# for i in range(1,len(ens)):
#     for j in range(1,len(ens)):

class test_methode1(object):
    """docstring for test_methode1"""
    def __init__(self):
        data=ts.lire_fichier()
        self.pb=ts.get_pb_alea(data)
        self.poids_SP=ts.gen_poids(self.pb["p"])#alea
        self.poids_OWA=np.sort(self.poids_SP)[::-1]#ordre decroissant
        self.poids_IC=np.sort(self.poids_SP)[::-1]
    def une_experience_sp(self):
        start=time.time()
        nb_question,sol,opt_sp,list_mmr_en_iteration=methode1.solution_optimal(self.pb,self.poids_SP,fonc=ts.som_pond_Y,fonc_PMR=ts.PMR_SP)
        end=time.time()
        opt_pl=PL.opt_pl_SP(self.pb,ts.som_pond,self.poids_SP)
        return end-start,nb_question,opt_pl-opt_sp
    def une_experience_owa(self):
        start=time.time()
        nb_question,sol,opt_owa,list_mmr_en_iteration=methode1.solution_optimal(self.pb,self.poids_OWA,fonc=ts.owa_Y,fonc_PMR=ts.PMR_OWA)
        end=time.time()
        opt_pl=PL.opt_pl_OWA(self.pb,self.poids_OWA)
        return end-start,nb_question,opt_pl-opt_owa
def main():
    test_m1=test_methode1()
    print(" probleme generer ",test_m1.pb)

    print("---------------- test methode1 somme pondérée ------------------ ")
    print(" w* pour somme pondérée" ,test_m1.poids_SP)
    temps,nb_question,erreur=test_m1.une_experience_sp()
    print("temps de calcul : " , temps)
    print("nombre de questions posées : " ,nb_question)
    print("erreur par rapport à la solution optimale du décideur : ", erreur)
    print("\n---------------- test methode1 owa --------------------------- ")
    print(" w* pour owa" ,test_m1.poids_OWA)
    temps2,nb_question2,erreur2=test_m1.une_experience_owa()
    print("temps de calcul : " , temps2)
    print("nombre de questions posées : " ,nb_question2)
    print("erreur par rapport à la solution optimale du décideur : ", erreur2)

if __name__ == "__main__":
    main()



