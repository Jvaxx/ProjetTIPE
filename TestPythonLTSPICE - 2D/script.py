import numpy as np
import fonctions as fc
from PyLTSpice.LTSpiceBatch import SimCommander


"""
Parametres generaux
"""

celerite = fc.celerite
frequence = fc.frequence
longueurOnde = fc.longueurOnde
distanceEntreAntennes = fc.distanceEntreAntennes

pointsAntennes = [
    [distanceEntreAntennes/(np.sqrt(3)), 0],
    [distanceEntreAntennes/(np.sqrt(3)), 2*np.pi/3],
    [distanceEntreAntennes/(np.sqrt(3)), 4*np.pi/3],
]




"""
Lancement de plusieurs simulations
Les directions a tester sont dans pointsATester (format [R, Theta], en radients)
Les directions obtenues sont dans directionsObtenues
"""

LTC = SimCommander('SimuSonore.asc') # C'est le pilote de la simu

pointsATester = np.array([ #les points qui vont etre tester
    [100, -np.pi/7], 
    [100, 2*np.pi/3], 
    [100, np.pi/4], 
])

#C'est les phases qui vont être entrees dans les 3 generateurs sur LTSpice, format [[phi1, phi2, phi3], [phi1, phi2, phi3], ...]
# L'itération des simulation se fait sur ces tuples de phases
listeDesPhases = [fc.calculDesPhases(point, pointsAntennes) for point in pointsATester]


# Boucle de simulation: une simu par triplet de phases (1 triplet de phase par point a tester)
directionsObtenues = [] #les directions obtenues apres simu, l'ordre correspond a ceux des ptsATester
for numeroDeSimulation, tripletDePhases in enumerate(listeDesPhases):

    # Generer les datas d'une simu de 0.4sec avec pour param le triplet de phase dans le fichier nommé "simulation{numéro de la simu}"
    fc.lancerUneSimu(tripletDePhases, 0.4, 'simulation' + str(numeroDeSimulation), LTC)

    # Traiter des données issues de la simulation précédente (il y a alors les 4 directions possibles, 2 par paires d'antennes)
    dephasageMesure, directionsMesuree = fc.traitementSimu('simulation' + str(numeroDeSimulation))

    # Selection de la direction apparaissant 2 fois et ajout de celle-ci dans la liste des directionsObtenues
    directionsObtenues.append(fc.trouverLaDirection(fc.radToDeg(fc.normaliserAnglePositif(directionsMesuree)))*np.pi/180)


#affichage des resultats - pas necessaire
fc.plotResultats(pointsATester[:, 1], directionsObtenues, pointsAntennes)