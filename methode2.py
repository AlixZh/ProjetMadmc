
import numpy as np
import matplotlib.pyplot as plt
import tools as *

  
def init_glouton(data,vp,xi):
    """
    data : dictionnaire des instances
    vp : liste des indices de critères
    xi : liste des indices des objets
    """
    sol=[]
    pb = get_donnees_pb(data,vp,xi)
    W = wmax(data,vp,xi)
    somme = np.sum(pb[:,1:],1)
    for i in range(len(xi)):
        
    while(np.sum(sol) < W):
    
  
  
