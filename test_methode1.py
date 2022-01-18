import numpy as np
import tools as ts
import methode1
import PL
from gurobipy import *
data=ts.lire_fichier()
pb=ts.get_pb_alea(data)
lambda_etoile=ts.gen_poids(pb["p"])
#lambda_etoile.sort()
lambda_etoile.sort()
lambda_etoile=lambda_etoile[::-1]#ordre decroissant
print("\nsolution",methode1.solution_optimal(pb,lambda_etoile,fonc=ts.owa_Y,fonc_PMR=ts.PMR_OWA))
PL.opt_pl_owa(pb,lambda_etoile)



