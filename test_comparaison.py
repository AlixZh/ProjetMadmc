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
                print(nb_objet[n],i)
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


#plot



def plot(L,criteres = [2,3,4,5,6],objets=[10,20,50,100,150],critere = True,path= "fig/"):
    """
    
    """
    #SPtemps, SPnb_Q, SPerreur_r, SPcpt_erreur = L_SP
    #SPtemps, SPnb_Q, SPerreur_r, SPcpt_erreur = L_SP

    ag = [" SP"," OWA"]
    mline = ["-.","dotted","--"]
    comp = [" Nb_Questions ", " Erreur R "," Erreur Cpt "]
    m = ["exacte","methode1","methode2"]
    if(critere):
        for n in range(len(objets)):
            for ncomp in range(1,len(comp)+1):
                fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
                fig.set_size_inches(25,10)
                fig.suptitle(comp[ncomp-1]+" n = "+str(objets[n]))
                for v in range(2): #pSPT ou OWA
                    for methode in range(2):
                        axs[v].plot(criteres,np.sum(L[v][ncomp][:,n,methode,:],1),label=m[methode+1]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("criteres")
                    axs[v].set_ylabel(comp[ncomp-1])
                    axs[v].legend()
                plt.savefig(path+comp[ncomp-1]+" n = "+str(objets[n]))
                plt.show()
                plt.close(fig)

            #Comp Temps
            fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
            fig.set_size_inches(25,10)
            fig.suptitle("Temps "+" n = "+str(objets[n]))
            for v in range(2): #parcours des methodes #premier erreur cpt , deuxieme relatif
                for methode in range(3):
                    print("ICI   ",np.sum(L[v][0][:,n,methode,:],1))
                    axs[v].plot(criteres,np.sum(L[v][0][:,n,methode,:],1),label=m[methode]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("criteres")
                    axs[v].set_ylabel("Temps (s)")
                    axs[v].legend()
            plt.savefig(path+"Temps_ "+"n = "+str(objets[n]))
            plt.show()
            plt.close(fig)
    else:
        for p in range(len(criteres)):
            for ncomp in range(1,len(comp)+1):
                fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
                fig.set_size_inches(25,10)
                fig.suptitle(comp[ncomp-1]+" p = "+str(criteres[p]))
                for v in range(2): #pSPT ou OWA
                    for methode in range(2):
                        axs[v].plot(objets,np.sum(L[v][ncomp][p,:,methode,:],1),label=m[methode+1]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("Nb objets")
                    axs[v].set_ylabel(comp[ncomp-1])
                    axs[v].legend()
                plt.savefig(path+comp[ncomp-1]+" p = "+str(criteres[p]))
                plt.show()
                plt.close(fig)

            #Comp Temps
            fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
            fig.set_size_inches(25,10)
            fig.suptitle("Temps "+" p = "+str(criteres[p]))
            for v in range(2): #parcours des methodes #premier erreur cpt , deuxieme relatif
                for methode in range(3):
                    axs[v].plot(objets,np.sum(L[v][0][p,:,methode,:],1),label=m[methode]+ag[v],linestyle=mline[methode])
                    axs[v].set_xlabel("Nb objets")
                    axs[v].set_ylabel("Temps (s)")
                    axs[v].legend()
            plt.savefig(path+"Temps_ "+"p = "+str(criteres[p]))
            plt.show()
            plt.close(fig)
            
            
def test(eps=0.1,nb_test = 50,criteres = [2,3,4,5,6],objets=[10,20,50,100,150],path="fig/"):
    #critere x:
    # for nbobjet in objets:
    #     a,b,c,d,e,f,g,h = execution_comparaison(eps , nb_test,criteres,[nbobjet])
    #     plot([[a,b,c,d],[e,f,g,h]],criteres,[nbobjet],True ,path)
    #objets x
    
    for nbc in criteres:
        a,b,c,d,e,f,g,h = execution_comparaison(eps , nb_test,[nbc],objets)
        plot([[a,b,c,d],[e,f,g,h]],[nbc],objets,False,path)

        
def plot_mmr_Q(eps = 0.1, nb_test = 20,nb_critere = [2,4,6],nb_objet = [20,50,100],path="fig/"):
    """
    """
    
    data = ts.lire_fichier("./2KP200-TA-0.dat")
    ag = [" SP"," OWA"]
    mline = ["-.","dotted"]
    m = ["methode1","methode2"]
    for p in range(len(nb_critere)):
        for n in range(len(nb_objet)):
            mmr_owa = [[],[]]
            nbq_owa = [[],[]]
            mmr_sp = [[],[]]
            nbq_sp = [[],[]]
            for i in range(nb_test):
                pb=ts.get_pb_alea(data,nb_objet[n],nb_critere[p])
                w_etoile = ts.gen_poids(nb_critere[p])
                
                #creation
                test_m1 = execution_methode1([pb,w_etoile],True)
                test_m2 = execution_methode2(0.1,100,[pb,w_etoile],True)
                
                #SP
                temp = []
                temp.append(test_m1.une_experience_sp())
                temp.append(test_m2.une_experience_sp())
                #x2,temps2,nb_question2,y_ag2 = test_m2.une_experience_sp()
                
                #Stockage SP
                for _type in range(2):
                    nbq_sp[_type].append(temp[_type][2])
                    mmr_sp[_type].append(temp[_type][-1])
                #OWA
                temp = []
                temp.append(test_m1.une_experience_owa())
                temp.append(test_m2.une_experience_owa())
                
                #Stockage OWA
                for _type in range(2):
                    nbq_owa[_type].append(temp[_type][2])
                    mmr_owa[_type].append(temp[_type][-1])
            

            fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
            fig.set_size_inches(25,10)
            fig.suptitle("Hytograme Nb Q "+" p = "+str(nb_critere[p])+" n = "+str(nb_objet[n]))

            axs[0].hist(nbq_sp,range(max(max(nbq_sp[0]),max(nbq_sp[1]))),label=[i+ag[0] for i in m])
            axs[0].set_xlabel("Nb questions")
            axs[0].set_ylabel("Nb")
            axs[0].legend()
            axs[1].hist(nbq_owa,range(max(max(nbq_owa[0]),max(nbq_owa[1]))),label=[i+ag[1] for i in m])
            axs[1].set_xlabel("Nb questions")
            axs[1].set_ylabel("Nb")
            axs[1].legend()
            plt.savefig(path+"Hytograme Nb Q "+" p = "+str(nb_critere[p])+" n = "+str(nb_objet[n]))
            plt.show()
            plt.close(fig)
            for i in range(nb_test):
                fig, axs = plt.subplots(1, 2) #un pour SP et un pour OWA
                fig.set_size_inches(25,10)
                fig.suptitle("Variation mmr "+" p = "+str(nb_critere[p])+" n = "+str(nb_objet[n]))
                for methode in range(2):
                    axs[0].plot(range(nbq_sp[methode][i]),mmr_sp[methode][i],label=[i+ag[0] for i in m],linestyle=mline)
                    axs[0].set_xlabel("Nb questions")
                    axs[0].set_ylabel("Nb")
                    axs[0].legend()
                    axs[1].plot(range(nbq_owa[methode][i]),mmr_owa[methode][i],label=[i+ag[1] for i in m],linestyle=mline)
                    axs[1].set_xlabel("Nb questions")
                    axs[1].set_ylabel("Nb")
                    axs[1].legend()
                plt.savefig(path+"Variation mmr "+" p = "+str(nb_critere[p])+" n = "+str(nb_objet[n])+str(i))
                plt.show()
                plt.close(fig)
s = time.time()
test()
e = time.time()  
