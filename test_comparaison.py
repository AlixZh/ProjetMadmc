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
    """
    pb : probleme condiere
    x : liste des indices des objets selectionnes
    x_pl :liste des indices des objets pris par le PL
    val_ag : valeur de la fonction d agregation pour x
    val_pl : valeur de la fonction d agregation pour x_pl
    calcul le nombre de difference d objet pris et les erreurs relative
    """
    x = np.array(ts.sol(pb,x))
    x_pl = np.array(ts.sol(pb,x_pl))
    return np.sum(np.abs(x-x_pl)), np.abs(val_ag-val_pl)/np.abs(val_pl)

def execution_comparaison(eps = 0.1, nb_test = 50,nb_critere = [2,3,4,5,6],nb_objet = [10,20,50,100,150]):
    """
    executer nb_test fois tous les nombres de critere de nb_critere et pour tous les nombres d objets de nb_objet
    renvoie 8 listes 4 pour SP et 4 pour OWA
    1-liste des temps d execution 
    2-liste des nombres de question
    3-liste des erreurs relatives
    4-liste du nombre d objet different pris par rapport a l opt
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
                    l_cpt_erreur_sp[p,n,_type,i],l_erreur_relative_sp[p,n,_type,i] = erreur(pb,temp[_type+1][0],temp[0][0],temp[_type+1][-2],temp[0][-1])
                
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
                    print(temp[_type+1][0],temp[0][0],temp[_type+1][-2],temp[0][-1])
                    l_cpt_erreur_owa[p,n,_type,i] ,l_erreur_relative_owa[p,n,_type,i] = erreur(pb,temp[_type+1][0],temp[0][0],temp[_type+1][-2],temp[0][-1])
                    
    return l_temps_sp,l_nb_Q_sp, l_erreur_relative_sp,l_cpt_erreur_sp,l_temps_owa ,l_nb_Q_owa,l_erreur_relative_owa ,l_cpt_erreur_owa 
#plot



def plot(L,criteres = [2,3,4,5,6],objets=[10,20,50,100,150],critere = True,nb_test = 20, path= "fig/"):
    """
    L: liste[liste], len(L) = nb de fonction d agregation possible, contient les listes renvoyer par execution
    criteres : liste du nombre de criteres a considerer
    objets: liste du nombre d ojet a consider
    critere: tracer les plots en fonction de la liste criteres
    nb_test: nombre d iteration, executer nb_test fois differents instances de meme taille
    path : nom du repertoire pour stocker les images de courbe
    trace tous les courbes necessaires 
    """

    ag = ["SP","OWA"]
    mline = ["-.","dotted","--"]
    comp = ["Nb_Questions", "Erreur Relative","Nb_different_objet_pris"]
    m = ["exacte","methode1","methode2"]
    if(critere):
        for n in range(len(objets)):
            for ncomp in range(1,len(comp)+1):
                fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
                fig.set_size_inches(25,10)
                fig.suptitle(comp[ncomp-1]+"_n="+str(objets[n]))
                for v in range(2): #pSPT ou OWA
                    for methode in range(2):
                        axs[v].plot(criteres,np.sum(L[v][ncomp][:,n,methode,:],1)/nb_test,label=m[methode+1]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("criteres")
                    axs[v].set_ylabel(comp[ncomp-1])
                    axs[v].legend()
                plt.savefig(path+comp[ncomp-1]+"_n="+str(objets[n]))
                plt.show()
                plt.close(fig)

            #Comp Temps
            fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
            fig.set_size_inches(25,10)
            fig.suptitle("Temps_"+"n="+str(objets[n]))
            for v in range(2): #parcours des methodes #premier erreur cpt , deuxieme relatif
                for methode in range(3):
                    print("ICI   ",np.sum(L[v][0][:,n,methode,:],1))
                    axs[v].plot(criteres,np.sum(L[v][0][:,n,methode,:],1)/nb_test,label=m[methode]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("criteres")
                    axs[v].set_ylabel("Temps (s)")
                    axs[v].legend()
            plt.savefig(path+"Temps_"+"n="+str(objets[n]))
            plt.show()
            plt.close(fig)
    else:
        for p in range(len(criteres)):
            for ncomp in range(1,len(comp)+1):
                fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
                fig.set_size_inches(25,10)
                fig.suptitle(comp[ncomp-1]+"_p="+str(criteres[p]))
                for v in range(2): #pSPT ou OWA
                    for methode in range(2):
                        axs[v].plot(objets,np.sum(L[v][ncomp][p,:,methode,:],1)/nb_test,label=m[methode+1]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("Nb objets")
                    axs[v].set_ylabel(comp[ncomp-1])
                    axs[v].legend()
                plt.savefig(path+comp[ncomp-1]+"_p="+str(criteres[p]))
                plt.show()
                plt.close(fig)

            #Comp Temps
            fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
            fig.set_size_inches(25,10)
            fig.suptitle("Temps_"+"p="+str(criteres[p]))
            for v in range(2): #parcours des methodes #premier erreur cpt , deuxieme relatif
                for methode in range(3):
                    axs[v].plot(objets,np.sum(L[v][0][p,:,methode,:],1)/nb_test,label=m[methode]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("Nb objets")
                    axs[v].set_ylabel("Temps (s)")
                    axs[v].legend()
            plt.savefig(path+"Temps_"+"p="+str(criteres[p]))
            plt.show()
            plt.close(fig)
            
            
def test(eps=0.1,nb_test = 50,criteres = [2,3,4,5,6],objets=[10,20,50,100,150],path="fig/"):
    """
    eps: espilon
    executre nb_test fois tous les instances de nombre de criteres et nombre d objets, en fonction du nombre de critere , puis du nombre d objet
    """
    #critere x:
    for nbobjet in objets:
        a,b,c,d,e,f,g,h = execution_comparaison(eps , nb_test,criteres,[nbobjet])
        plot([[a,b,c,d],[e,f,g,h]],criteres,[nbobjet],True ,nb_test,path)
    #objets x
    
    for nbc in criteres:
        a,b,c,d,e,f,g,h = execution_comparaison(eps , nb_test,[nbc],objets)
        plot([[a,b,c,d],[e,f,g,h]],[nbc],objets,False,nb_test,path)

        
def plot_mmr_Q(eps = 0.1, nb_test = 50,nb_critere = [2,4,6],nb_objet = [20,50,100,150],path="fig/"):
    """
    permet de tracer les courbes de mmr en fonctin du nombre de question et les histogrammes des nombres de question
    """
    
    data = ts.lire_fichier("./2KP200-TA-0.dat")
    ag = ["SP","OWA"]
    mline = ["-.","dotted"]
    m = "methode1 "
    
    for p in range(len(nb_critere)):
        for n in range(len(nb_objet)):
            mmr = [[],[]] # 0 : SP, 1: OWA
            nbq = [[],[]]
            for i in range(nb_test):
                pb=ts.get_pb_alea(data,nb_objet[n],nb_critere[p])
                w_etoile = ts.gen_poids(nb_critere[p])
                
                #creation
                test_m1 = execution_methode1([pb,w_etoile],True)
                
                #SP
                temp = test_m1.une_experience_sp()
                #x2,temps2,nb_question2,y_ag2 = test_m2.une_experience_sp()
                
                #Stockage SP
                nbq[0].append(temp[2])
                mmr[0].append(temp[-1])
                    
                #OWA
                temp = test_m1.une_experience_owa()
                
                #Stockage OWA

                nbq[1].append(temp[2])
                mmr[1].append(temp[-1])
            

            fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
            fig.set_size_inches(25,10)
            fig.suptitle("Histogramme_Nb_Q_"+"p_=_"+str(nb_critere[p])+"_n="+str(nb_objet[n]))
            for _type in range(len(ag)):
                axs[_type].hist(nbq[_type],label=m+ag[_type] )
                axs[_type].set_xlabel("Nb questions")
                axs[_type].legend()

            plt.savefig(path+"Histogramme_Nb_Q_"+"p_=_"+str(nb_critere[p])+"_n="+str(nb_objet[n]))
            plt.show()
            plt.close(fig)
            
            Ymmr = [[],[]]
            nbm = []
            for _type in range(len(ag)):
                nb = set()
                for i in mmr[_type] : 
                    nb.add(len(i))
                nb = list(nb)
                nb.sort()
                maxnb = max(nb)
                mmrxx = []
                for i in range(maxnb):
                    mmrxx.append([])
                nbm.append(maxnb)
                for i in range(nb_test):
                    for j in range(maxnb):
                
                        if(len(mmr[_type][i])>j):
                            if(mmr[_type][i][j] == float("-inf")):
                                mmrxx[j].append(0)
                            else:
                                mmrxx[j].append(mmr[_type][i][j])
                            
                for i in range(maxnb):
                    Ymmr[_type].append(np.sum(mmrxx[i])/len(mmrxx[i]))
            fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
            fig.set_size_inches(25,10)
            fig.suptitle("Variation_mmr_"+"_p="+str(nb_critere[p])+"_n="+str(nb_objet[n]))
            for _type in range(2):
                print(len(Ymmr[_type]),nbm[_type],Ymmr[_type])
                axs[_type].plot(range(nbm[_type]),Ymmr[_type],label=m+ag[_type] )
                axs[_type].set_xlabel("Nb questions")
                axs[_type].set_ylabel("MMR")
                axs[_type].legend()
            plt.savefig(path+"Variation_mmr_"+"_p="+str(nb_critere[p])+"_n="+str(nb_objet[n]))
            plt.show()
            plt.close(fig)
s = time.time()
test()
e = time.time()  
