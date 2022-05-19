import numpy as np
import fonctions as fc


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

# angles = [np.pi/7, np.pi/3]
# directions = []
# for i, angle in enumerate(angles):
#     pointSource = [1000, angle] # polaire
#     phases = fc.calculDesPhases(pointSource, pointsAntennes)
#     fc.lancerUneSimu(phases, 0.3, 'test' + str(i))
#     dephasageSimu, directionSimu = fc.traitementSimu('test' + str(i))
#     directions.append(fc.trouverLaDirection(fc.radToDeg(fc.normaliserAnglePositif(directionSimu))))
#     print(f'simu {i+1} terminee')

# print(fc.radToDeg(angles))
# print(fc.radToDeg(directions))

pointSource = [1000, -np.pi/4] # polaire
phases = fc.calculDesPhases(pointSource, pointsAntennes)
fc.lancerUneSimu(phases, 0.3, 'testoune')
dephasageSimu, directionSimu = fc.traitementSimu('testoune')
print(fc.radToDeg(directionSimu))
print(fc.radToDeg(fc.normaliserAnglePositif(directionSimu)))
print(fc.trouverLaDirection(fc.radToDeg(fc.normaliserAnglePositif(directionSimu))))






# print('-----------', '\n')
# print('Phases initiales:          ', phases, '\n')
# print('-----------', '\n')
# print('Dephasage :                ', abs(phases[1] - phases[0]), abs(phases[2] - phases[0]))
# print('Dephasage obtenu par theo: ', fc.radToDeg(dephasageTheo))
# print('Dephasage obtenu par simu: ', fc.radToDeg(dephasageSimu), '\n')
# print('-----------', '\n')
# print('Directions theoriques:     ', fc.radToDeg(directionTheo))
# print('Directions simu:           ', fc.radToDeg(directionSimu))