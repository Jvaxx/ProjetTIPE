import numpy as np
import fonctions as fc
from PyLTSpice.LTSpiceBatch import SimCommander


# Parametres generaux
celerite = fc.celerite
frequence = fc.frequence
longueurOnde = fc.longueurOnde
distanceEntreAntennes = fc.distanceEntreAntennes

pointsAntennes = [
    [distanceEntreAntennes/(np.sqrt(3)), 0],
    [distanceEntreAntennes/(np.sqrt(3)), 2*np.pi/3],
    [distanceEntreAntennes/(np.sqrt(3)), 4*np.pi/3],
]


LTC = SimCommander('SimuSonore.asc')
pointsTest = np.array([[1000, -np.pi/7]])
directions = []

phasesList = [fc.calculDesPhases(point, pointsAntennes) for point in pointsTest]
print(phasesList)
for i, phases in enumerate(phasesList):
    fc.lancerUneSimu(phases, 0.4, 'testoune' + str(i), LTC)
    dephasageSimu, directionSimu = fc.traitementSimu('testoune' + str(i))
    print(fc.trouverLaDirection(fc.radToDeg(fc.normaliserAnglePositif(directionSimu))))
    directions.append(fc.trouverLaDirection(fc.radToDeg(fc.normaliserAnglePositif(directionSimu)))*np.pi/180)
    print(directions)

fc.plotResultats(pointsTest[:, 1], directions, pointsAntennes)