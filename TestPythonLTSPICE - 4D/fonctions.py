import os
from PyLTSpice.LTSpiceBatch import SimCommander
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead
import numpy as np


celerite = 342
frequence = 300
longueurOnde = celerite/frequence
distanceEntreAntennes = longueurOnde/6


def traitementSimu(nomSimu: str):
    LTR = LTSpiceRawRead(f'{nomSimu}.raw')

    # Recuperation des listes de valeurs
    amplitudes = np.array([
        list(LTR.get_trace('V(sortiecrete1)'))[-1],
        list(LTR.get_trace('V(sortiecrete2)'))[-1],
        list(LTR.get_trace('V(sortiecrete3)'))[-1],
        list(LTR.get_trace('V(sortiecrete4)'))[-1],
        list(LTR.get_trace('V(sortiecrete5)'))[-1],
        list(LTR.get_trace('V(sortiecrete6)'))[-1],
    ])
    fondamentauxMult = np.array([
        list(LTR.get_trace('V(sortiepb2)'))[-1],
        list(LTR.get_trace('V(sortiepb3)'))[-1],
        list(LTR.get_trace('V(sortiepb1)'))[-1],
        list(LTR.get_trace('V(sortiepb4)'))[-1],
        list(LTR.get_trace('V(sortiepb5)'))[-1],
    ])

    correcteurMultiplieur = 1.13

    # en radians
    dephasages = np.arccos(2*correcteurMultiplieur*fondamentauxMult/(amplitudes[1:]*amplitudes[0]))


    return dephasages


def calculDesPhases(pointSource, pointsAntennes):
    ptSrc = polVersCart(pointSource)
    ptsAnts = polVersCartArray(pointsAntennes)
    phasesNonNorm = (np.linalg.norm(ptSrc - ptsAnts, axis=1) % longueurOnde) * (360/longueurOnde)
    phases = normaliserAngleCentreArray(phasesNonNorm)

    # phase1 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[0]))) 
    #     % longueurOnde) * (360/longueurOnde))
    # phase2 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[1]))) 
    #     % longueurOnde) * (360/longueurOnde))
    # phase3 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[2]))) 
    #     % longueurOnde) * (360/longueurOnde))
    return phases


def lancerUneSimu(phases: list, duree: float, nomFichier: str):
    LTC = SimCommander('SimuSonore.asc')

    LTC.set_parameter('Phase1', f'{{{phases[0]}}}')
    LTC.set_parameter('Phase2', f'{{{phases[1]}}}')
    LTC.set_parameter('Phase3', f'{{{phases[2]}}}')
    LTC.set_parameter('Frequence', f'{{{frequence}}}')

    LTC.add_instruction(f'.tran {duree}')

    LTC.run(run_filename=f'{nomFichier}.net')
    LTC.wait_completion()


def polVersCart(point):
    return np.array([
        point[0]*np.sin(point[1])*np.cos(point[2]),
        point[0]*np.sin(point[1])*np.sin(point[2]),
        point[0]*np.cos(point[1]),
    ])


def polVersCartArray(points):
    res = []
    for i, point in enumerate(points):
        coords = [
            point[0]*np.sin(point[1])*np.cos(point[2]),
            point[0]*np.sin(point[1])*np.sin(point[2]),
            point[0]*np.cos(point[1]),
        ]
        res.append(np.array(coords))
    return np.array(res)


def normaliserAngleCentre(angle):
    if 0 <= angle <= 180: return angle
    if angle >= 180: return angle - 360


def normaliserAngleCentreArray(angles):
    res = np.zeros(len(angles))
    for i, angle in enumerate(angles):
        if 0 <= angle <= 180: res[i] = angle
        if angle >= 180: res[i] = angle - 360
    return res


def normaliserAnglePositif(angles): #en radians
    res = []
    for angle in angles:
        if angle < 0:
            res.append(angle + np.pi)
        else:
            res.append(angle)
    return res


def radToDeg(angle):
    if type(angle) == list:
        return list(map(lambda x: (x * 360) / (2*np.pi), angle))
    return (angle * 360) / (2*np.pi)


# print('distances')
# print(np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[0])))
# print(np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[1])))
# print(np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[2])))

# LTC.add_instructions(
#     '.meas TRAN Amplitude1 PARAM (V(SortieCrete1))',
#     '.meas TRAN Amplitude2 PARAM (V(SortieCrete2))',
#     '.meas TRAN Amplitude3 PARAM (V(SortieCrete3))',
#     '.meas TRAN AmplitudeFondMult1 PARAM (V(SortiePB1))',
#     '.meas TRAN AmplitudeFondMult2 PARAM (V(SortiePB2))',

#     '.meas TRAN dephasage1O PARAM arccos(2*AmplitudeFondMult1*1.13 / (Amplitude2*Amplitude1))',
#     '.meas TRAN dephasage2O PARAM arccos(2*AmplitudeFondMult2*1.13 / (Amplitude3*Amplitude1))',
#     f'.meas TRAN direction11O PARAM arcsin(-dephasage1O*{longueurOnde/distanceEntreAntennes}/(360))+60',
#     f'.meas TRAN direction12O PARAM -(arcsin(-dephasage1O*{longueurOnde/distanceEntreAntennes}/(360)))+60',
#     f'.meas TRAN direction21O PARAM arcsin(-dephasage2O*{longueurOnde/distanceEntreAntennes}/(360))-60',
#     f'.meas TRAN direction22O PARAM -(arcsin(-dephasage2O*{longueurOnde/distanceEntreAntennes}/(360)))-60'
# )