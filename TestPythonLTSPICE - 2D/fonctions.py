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
    amplitude1 = list(LTR.get_trace('V(sortiecrete1)'))[-1]
    amplitude2 = list(LTR.get_trace('V(sortiecrete2)'))[-1]
    amplitude3 = list(LTR.get_trace('V(sortiecrete3)'))[-1]
    amplitudeFondamentalMult1 = list(LTR.get_trace('V(sortiepb1)'))[-1]
    amplitudeFondamentalMult2 = list(LTR.get_trace('V(sortiepb2)'))[-1]

    correcteurMultiplieur = 1.13

    # en radians
    dephasages = [
        (np.arccos(2 * amplitudeFondamentalMult1 * correcteurMultiplieur /
            (amplitude1*amplitude2))),
        (np.arccos(2 * amplitudeFondamentalMult2 * correcteurMultiplieur /
            (amplitude1*amplitude3))),
    ]

    # en radians
    directions = [
        (np.arcsin(-dephasages[0] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) + np.pi/3),
        (-np.arcsin(-dephasages[0] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) + np.pi/3),
        (np.arcsin(-dephasages[1] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) - np.pi/3),
        (-np.arcsin(-dephasages[1] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) - np.pi/3),
    ]

    return dephasages, directions


def traitementTheorique(phases: list, amplitude: float):
    points = np.linspace(0, 0.5, 7000)
    signaux = np.array([
        np.sin(points * 300 * 2 * np.pi + phases[0] * np.pi / 180),
        np.sin(points * 300 * 2 * np.pi + phases[1] * np.pi / 180),
        np.sin(points * 300 * 2 * np.pi + phases[2] * np.pi / 180),
    ]) * amplitude

    fondMult = np.array([
        np.mean(signaux[0]*signaux[1]),
        np.mean(signaux[0]*signaux[2]),
    ])

    dephasages = [
        (np.arccos(2 * fondMult[0] / (amplitude**2))),
        (np.arccos(2 * fondMult[1] / (amplitude**2))),
    ]

    directions = [
        (np.arcsin(-dephasages[0] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) + np.pi/3),
        (-np.arcsin(-dephasages[0] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) + np.pi/3),
        (np.arcsin(-dephasages[1] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) - np.pi/3),
        (-np.arcsin(-dephasages[1] * (longueurOnde / distanceEntreAntennes) /
            (2 * np.pi)) - np.pi/3),
    ]

    return dephasages, directions


def calculDesPhases(pointSource, pointsAntennes):
    phase1 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[0]))) 
        % longueurOnde) * (360/longueurOnde))
    phase2 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[1]))) 
        % longueurOnde) * (360/longueurOnde))
    phase3 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[2]))) 
        % longueurOnde) * (360/longueurOnde))
    return [phase1, phase2, phase3]


def lancerUneSimu(phases: list, duree: float, nomFichier: str):
    LTC = SimCommander('SimuSonore.asc')

    LTC.set_parameter('Phase1', f'{{{phases[0]}}}')
    LTC.set_parameter('Phase2', f'{{{phases[1]}}}')
    LTC.set_parameter('Phase3', f'{{{phases[2]}}}')
    LTC.set_parameter('Frequence', f'{{{frequence}}}')

    LTC.add_instruction(f'.tran {duree}')

    LTC.run(run_filename=f'{nomFichier}.net')
    LTC.wait_completion()


def trouverLaDirection(directions):
    marges = [
        abs(directions[2] - directions[0]),
        abs(directions[3] - directions[0]),
        abs(directions[2] - directions[1]),
        abs(directions[3] - directions[1]),
    ]
    minIndex = marges.index(min(marges))
    if minIndex == 0: return (directions[2]+directions[0])/2
    if minIndex == 1: return (directions[3]+directions[0])/2
    if minIndex == 2: return (directions[2]+directions[1])/2
    if minIndex == 3: return (directions[3]+directions[1])/2


def cylVersCart(point):
    return np.array([point[0]*np.cos(point[1]), point[0]*np.sin(point[1])])


def normaliserAngleCentre(angle):
    if 0 <= angle <= 180: return angle
    if angle >= 180: return angle - 360


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