from gurobipy import *
import numpy as np
import tools as *


def opt_pl(pb,fonc,xi,nbcont = 1):
	"""
	pb : dict du pb considere
	fonc : fonction d agregation
	x : liste des indices des objets a prendre
	nb_cont : nombre de contrainte
	"""
	nbvar=pb["n"] #nombre d objet possible
	lignes = range(nbcont)
	colonnes = range(nbvar)


	#matrice des contraintes
	a = np.array(pb["wi"])
	# Second membre
	b = pb["W"]

	# Coefficients de la fonction objectif
	c = y(pb,xi)

	m = Model("SD")     
		    
	# declaration variables de decision
	w = []
	for i in colonnes:
		w.append(m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name="w%d" % (i+1)))

	# maj du modele pour integrer les nouvelles variables
	m.update()

	obj = LinExpr();
	obj =0
	for j in colonnes:
		obj += c[j] * x[j]
		    
	# definition de l'objectif
	m.setObjective(obj,GRB.MAXIMIZE)

	# Definition des contraintes
	for i in lignes:
		m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

	# Resolution
	m.optimize()


	print("")                
	print('Solution optimale:')
	for j in colonnes:
		print('x%d'%(j+1), '=', w[j].w)
	print("")
	print('Valeur de la fonction objectif :', m.objVal)



























