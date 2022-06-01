import numpy as np
import fonctions as fc
import KNNPhase as knn


# Parametres generaux
celerite = fc.celerite
frequence = fc.frequence
longueurOnde = fc.longueurOnde
distanceEntreAntennes = fc.distanceEntreAntennes

pointsAntennes = [ # r, theta, phi avec 0<theta<pi, 0<phi<2pi
    [distanceEntreAntennes/(np.sqrt(3)), np.pi/2, 0],
    [distanceEntreAntennes/(np.sqrt(3)), np.pi/2, 2*np.pi/3],
    [distanceEntreAntennes/(np.sqrt(3)), np.pi/2, 4*np.pi/3],

    [distanceEntreAntennes/(np.sqrt(3)), 0, 0],
    [distanceEntreAntennes/(np.sqrt(3)), 2*np.pi/3, 0],
    [distanceEntreAntennes/(np.sqrt(3)), 2*np.pi/3, np.pi],
]

pointSource = [1000, np.pi/4, np.pi/4]
phases = fc.calculDesPhases(pointSource, pointsAntennes)
print(phases)
# fc.lancerUneSimu(phases, 0.3, 'superTest')
# dephasages = fc.traitementSimu('superTest')
# print(dephasages)



knn.AbaquePhase.Abaque(fc.pasOptimalAbaque, pointSource[0], fc.frequence)
abaque = knn.RecupereValeursFichier('AbaquePhase.txt')
directionCalc = knn.KNN(abaque, [0.58, 2.16, 2.76, 0.75, 2.34], fc.nbrPlusProcheVoisin)
print(directionCalc)
