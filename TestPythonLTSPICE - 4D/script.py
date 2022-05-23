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

pointSource = [1000, 0, 0]
phases = fc.calculDesPhases(pointSource, pointsAntennes)
print(phases)
# fc.lancerUneSimu(phases, 0.3, 'superTest')
dephasages = np.array(fc.traitementSimu('superTest')) % 2*np.pi



# knn.AbaquePhase.Abaque(fc.pasOptimalAbaque, pointSource[0], fc.frequence)
# abaque = knn.RecupereValeursFichier('AbaquePhase.txt')
# directionCalc = knn.KNN(abaque, dephasages, fc.nbrPlusProcheVoisin)
# print(directionCalc)
