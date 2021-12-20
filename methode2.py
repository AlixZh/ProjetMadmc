
import numpy as np
import matplotlib.pyplot as plt

def get_donnees_pb(data,vp,xi):
  """
  data : dictionnaire des instances
  vp : liste des indices de critères
  xi : liste des indices des objets
  renvoie une liste des donnees du probleme a considerer
  """
  res = []
  for x in xi :
    res.append([data["i"][x][p] for p in vp])
  return res
  
def init_glouton(data,vp,xi):
  """
  data : dictionnaire des instances
  vp : liste des indices de critères
  xi : liste des indices des objets
  """
  sol=[]
  
  
  
