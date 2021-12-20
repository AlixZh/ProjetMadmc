
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
  
  
  
