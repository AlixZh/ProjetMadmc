# ProjetMadmc
Élicitation incrémentale et recherche locale pour le problème du sac à dos multi-objectifs


## Explication des variables

data : dict(str,Any), dictionnaire des données de tous les données possibles.
data["i"] : list[list[int]] contient les données de tous les objets
data["i"][i] : list[int], contient le poids et les differents valeurs des critères de l'objet i
data["nom_param"] : contient le nom que represente chaque indice de data["i"][i]
data["W"] : int, valeur de la capacité de tous les objets

pb : dict(str,Any), dictionnaire des données du problème à considérer.
pb["v"] : list[int], contient tous les objets du probeleme


## Explication des fichiers 

tools.py : contient des fonctions communes qui permettent d'aider à l'implémentation des deux méthodes 
           (fonctions d'agregation, d'extraction des données, génération de poids, de problème, calcul de PMR, MR, MMR et de voisinage...)

QuadTree.py : contient l'implémentation de quad tree

methode1.py : contient l'implémentation de la méthode 1, PLS et solution_optimale

methode2.py : contient l'implémentation de la méthode 2, PLS_elicitation et rbls

PL.py : contient les PL pour trouver la solution optimale en fonction du vecteur poids du décideur

## Exécution

Lancer le fichier test_methode.py pour executer la méthode 1, la méthode 2 et la méthode exacte pour une instance donnée.
Lancer le fichier test_comp.py pour obtenir les courbes de comparaison

Appeler la fonction main de test_methode pour avoir les resultats des 2 methodes et du PL, en donnant en parametre le nombre d'objet et critere à considérer
