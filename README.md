# ProjetMadmc
Élicitation incrémentale et recherche locale pour le problème du sac à dos multi-objectifs


## Explication des variables

data : dict(str,Any), dictionnaire des données de tous les données possibles.
data["i"] : list[list[int]] contient les données de tous les objets
data["i"][i] : list[int], contient le poids et les differents valeurs des critères de l'objet i
data["nom_param"] : contient le nom que represente chaque indice de data["i"][i]
data["W"] : int, valeur de la capacité de tous les objets

pb : dict(str,Any, dictionnaire des données du problème à considérer.
pb["v"] : list[int], contient tous les objets de 
