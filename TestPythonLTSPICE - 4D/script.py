import numpy as np
import fonctions as fc


# Parametres generaux
celerite = fc.celerite
frequence = fc.frequence
longueurOnde = fc.longueurOnde
distanceEntreAntennes = fc.distanceEntreAntennes

pointsAntennes = [ # r, theta, phi avec 0<theta<pi, 0<phi<2pi
    [distanceEntreAntennes/(np.sqrt(3)), np.pi/2, np.pi/2],
    [distanceEntreAntennes/(np.sqrt(3)), np.pi/2, 2*np.pi/3],
    [distanceEntreAntennes/(np.sqrt(3)), np.pi/2, 4*np.pi/3],

    [distanceEntreAntennes/(np.sqrt(3)), 0, 0],
    [distanceEntreAntennes/(np.sqrt(3)), 2*np.pi/3, 0],
    [distanceEntreAntennes/(np.sqrt(3)), 2*np.pi/3, np.pi],
]

pointSource = [1000, np.pi/3, np.pi/2]
phases = fc.calculDesPhases(pointSource, pointsAntennes)
fc.lancerUneSimu(phases, 0.3, 'superTest')
dephasages = np.array(fc.radToDeg(fc.traitementSimu('superTest'))) % 360
fc.ajouterResultat('resultats.txt', dephasages)