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
from test_methode import *


def erreur(pb,x,x_pl,val_ag,val_pl):
    x = np.array(ts.sol(pb,x))
    x_pl = np.array(ts.sol(pb,x_pl))
    return np.sum(np.abs(x-x_pl)), (val_ag-val_pl)/val_pl
    
    
def execution_comparaison(eps = 0.1, nb_test = 50,nb_critere = [2,3,4,5,6],nb_objet = [10,20,50,100,150]):
    """
    """
    
    data = ts.lire_fichier("./2KP200-TA-0.dat")
    
    l_temps_sp = np.zeros((len(nb_critere),len(nb_objet),3,nb_test)) #0 exacte, 1 : methode1, 2: methode2
    l_nb_Q_sp = np.zeros((len(nb_critere),len(nb_objet),2,nb_test))
    l_erreur_relative_sp = np.zeros((len(nb_critere),len(nb_objet),2,nb_test))
    l_cpt_erreur_sp = np.zeros((len(nb_critere),len(nb_objet),2,nb_test))
    
    l_temps_owa = np.zeros((len(nb_critere),len(nb_objet),3,nb_test)) #0 exacte, 1 : methode1, 2: methode2
    l_nb_Q_owa = np.zeros((len(nb_critere),len(nb_objet),2,nb_test))
    l_erreur_relative_owa = np.zeros((len(nb_critere),len(nb_objet),2,nb_test))
    l_cpt_erreur_owa = np.zeros((len(nb_critere),len(nb_objet),2,nb_test))

    
    for p in range(len(nb_critere)):
        for n in range(len(nb_objet)):
            for i in range(nb_test):
                pb=ts.get_pb_alea(data,nb_objet[n],nb_critere[p])
                w_etoile = ts.gen_poids(nb_critere[p])
                
                #creation
                test_m1 = execution_methode1([pb,w_etoile],True)
                test_m2 = execution_methode2(0.1,100,[pb,w_etoile],True)
                test_e=execution_exacte([pb,w_etoile],True)
                
                #SP
                temp = []
                temp.append(test_e.une_experience_sp())
                temp.append(test_m1.une_experience_sp())
                temp.append(test_m2.une_experience_sp())
                #x2,temps2,nb_question2,y_ag2 = test_m2.une_experience_sp()
                
                #Stockage SP
                l_temps_sp[p,n,0,i] = temp[0][1]
                for _type in range(2):
                    l_temps_sp[p,n,_type + 1,i] = temp[_type+1][1]
                    l_nb_Q_sp[p,n,_type,i] = temp[_type+1][2]
                    l_cpt_erreur_sp[p,n,_type,i],l_erreur_relative_sp[p,n,_type,i] = erreur(pb,temp[_type+1][0],temp[0][0],temp[_type+1][-2],temp[0][-2])
                
                #OWA
                temp = []
                temp.append(test_e.une_experience_owa())
                temp.append(test_m1.une_experience_owa())
                temp.append(test_m2.une_experience_owa())
                
                #Stockage OWA
                l_temps_owa[p,n,0,i] = temp[0][1]
                for _type in range(2):
                    l_temps_owa[p,n,_type+1,i] = temp[_type+1][1]
                    l_nb_Q_owa[p,n,_type,i] = temp[_type+1][2]
                    l_cpt_erreur_owa[p,n,_type,i] ,l_erreur_relative_owa[p,n,_type,i] = erreur(pb,temp[_type+1][0],temp[0][0],temp[_type+1][-2],temp[0][-2])
                    
    return l_temps_sp,l_nb_Q_sp, l_erreur_relative_sp,l_cpt_erreur_sp,l_temps_owa ,l_nb_Q_owa,l_erreur_relative_owa ,l_cpt_erreur_owa 
