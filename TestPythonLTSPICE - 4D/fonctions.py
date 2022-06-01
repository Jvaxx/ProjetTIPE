import os
from PyLTSpice.LTSpiceBatch import SimCommander
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead
import numpy as np


celerite = 340
frequence = 300
longueurOnde = celerite/frequence
distanceEntreAntennes = longueurOnde/2
pasOptimalAbaque = 3
nbrPlusProcheVoisin = 94


def traitementSimu(nomSimu: str):
    LTR = LTSpiceRawRead(f'SimuSonore.raw')
    # LTR = LTSpiceRawRead(f'{nomSimu}.raw')

    # Recuperation des listes de valeurs
    amplitudes = np.array([list(LTR.get_trace(f'V(sortiecrete{i+1})'))[-1] for i in range(6)])
    ampFondamentalesMult = np.array([list(LTR.get_trace(f'V(sortiepb{i+1})'))[-1] for i in range(30)])
    correcteurMultiplieur = 1.10

    amplitudes30 = np.empty(30)
    for i in range(6):
        amplitudes30[i:i+5] = np.delete(amplitudes, i, axis=0)*amplitudes[i]
    

    # en radians
    preAcos = 2*ampFondamentalesMult*correcteurMultiplieur/amplitudes30
    preAcos[preAcos>1] = 1
    preAcos[preAcos<-1] = -1
    dephasages = np.arccos(preAcos)


    return dephasages


def calculDesPhases(pointSource, pointsAntennes):
    ptSrc = polVersCart(pointSource)
    ptsAnts = polVersCartArray(pointsAntennes)
    phasesNonNorm = (np.linalg.norm(ptSrc - ptsAnts, axis=1) % longueurOnde) * (360/longueurOnde)
    phases = normaliserAngleCentreArray(phasesNonNorm)

    return phases


def lancerUneSimu(phases: list, duree: float, nomFichier: str):
    LTC = SimCommander('SimuSonore.asc')

    for i in range(6):
        LTC.set_parameter(f'Phase{i+1}', f'{{{phases[i]}}}')

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


def ajouterResultat(nomFichier: str, resultats):
    with open(nomFichier, 'a') as fichier:
        for result in resultats:
            fichier.write(str(result) + ',')
        fichier.write('\n')