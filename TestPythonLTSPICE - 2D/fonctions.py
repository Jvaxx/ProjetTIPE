import os
import time
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead
from cv2 import pointPolygonTest
import numpy as np
import matplotlib.pyplot as plt


celerite = 342
frequence = 300
longueurOnde = celerite/frequence
distanceEntreAntennes = longueurOnde/3


def traitementSimu(nomSimu: str):
    """
    Programme traitant une simulation dont les données sont dans le fichier nomSimu
    """

    # Lecteur de la simu
    LTR = LTSpiceRawRead(f'{nomSimu}.raw')

    # Recuperation des listes de valeurs
    amplitude1 = list(LTR.get_trace('V(sortiecrete1)'))[-1]
    amplitude2 = list(LTR.get_trace('V(sortiecrete2)'))[-1]
    amplitude3 = list(LTR.get_trace('V(sortiecrete3)'))[-1]

    valeursMult1 = np.array(list(LTR.get_trace('V(sortiemult1)')[-500:]))
    valeursMult2 = np.array(list(LTR.get_trace('V(sortiemult2)')[-500:]))
    amplitudeFondamentalMult1 = (np.max(valeursMult1) + np.min(valeursMult1))/2
    amplitudeFondamentalMult2 = (np.max(valeursMult2) + np.min(valeursMult2))/2

    correcteurMultiplieur = 1.07

    # en radians
    dephasages = [
        (np.arccos(2 * amplitudeFondamentalMult1 * correcteurMultiplieur /
            (amplitude1*amplitude2))),
        (np.arccos(2 * amplitudeFondamentalMult2 * correcteurMultiplieur /
            (amplitude1*amplitude3))),
    ]

    # en radians
    preAsin = [
        preAsinTraitement(-dephasages[0] * (longueurOnde / distanceEntreAntennes) / (2 * np.pi)),
        preAsinTraitement(-dephasages[0] * (longueurOnde / distanceEntreAntennes) / (2 * np.pi)),
        preAsinTraitement(-dephasages[1] * (longueurOnde / distanceEntreAntennes) / (2 * np.pi)),
        preAsinTraitement(-dephasages[1] * (longueurOnde / distanceEntreAntennes) / (2 * np.pi)),
    ]

    directions = [
        (np.arcsin(preAsin[0]) + np.pi/3),
        (-np.arcsin(preAsin[1]) + np.pi/3),
        (np.arcsin(preAsin[2]) - np.pi/3),
        (-np.arcsin(preAsin[3]) - np.pi/3),
    ]

    return dephasages, directions


def traitementTheorique(phases: list, amplitude: float):
    """
    Meme que le prgm de traitement par LTSpice mais en generant tout de A a Z et sans passer par LTSpice donc
    """

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
    """
    Calcule les 3 phases à injecter dans LTSpice pour un set d'antennes données et un point source.
    Fonctionne en 3D comme en 2D
    """
    phase1 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[0]))) 
        % longueurOnde) * (360/longueurOnde))
    phase2 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[1]))) 
        % longueurOnde) * (360/longueurOnde))
    phase3 = normaliserAngleCentre(((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[2]))) 
        % longueurOnde) * (360/longueurOnde))
    return [phase1, phase2, phase3]


def lancerUneSimu(phases: list, duree: float, nomFichier: str, LTC):
    """
    Fonction de lancement d'une simu.
    Prend en entrée les 3 phases des 3 antennes. Ecrit les resultats de la simu dans un fichier
    """

    # Mise en place des pramaetres de la simu
    LTC.set_parameter('Phase1', f'{{{phases[0]}}}')
    LTC.set_parameter('Phase2', f'{{{phases[1]}}}')
    LTC.set_parameter('Phase3', f'{{{phases[2]}}}')
    LTC.set_parameter('Frequence', f'{{{frequence}}}')

    LTC.add_instruction(f'.tran {duree}')
    
    # Lancement simu
    LTC.run(run_filename=f'{nomFichier}.net')
    LTC.wait_completion()
    LTC.reset_netlist()


def trouverLaDirection(directions):
    """
    Le traitement de simu donne 4 directions possibles, dont 2 qui sont proches.
    Cette fonction revoie les 2 element les plus proches d'une liste. Tres mal optimisée.
    """
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
    """
    Fonction de [0; 2*pi] --> [-pi; pi]
    """
    if 0 <= angle <= 180: return angle
    if angle >= 180: return angle - 360


def normaliserAnglePositif(angles): #en radians
    """
    Ramene l'angle dans l'intervalle [0; pi]
    """
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


def preAsinTraitement(valeur):
    """
    Prend en considération les cas limites
    """
    if -1 < valeur < 1:
        return valeur
    if valeur < -1:
        return -1
    if valeur > 1:
        return 1


def plotResultats(valeursInit, valeursExp, antennes):
    """
    Plot en polaire des resultats
    """
    antounettes = np.array(antennes)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.scatter(antounettes[:,1], antounettes[:,0], c = 'red', marker = 'x')
    rayonScatter = np.repeat([0.72], len(valeursInit))
    ax.scatter(valeursInit, rayonScatter, c='red')
    ax.scatter(valeursExp, rayonScatter, c='green')
    ax.set_rticks([antounettes[0,0], 0.75])
    ax.set_rmax(0.75)
    plt.show()
