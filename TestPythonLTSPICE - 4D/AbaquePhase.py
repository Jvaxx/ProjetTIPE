#executer en tant que script ( ctrl + shit + E sur pyzo)
import os
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

import numpy as np
import math
import matplotlib.pyplot as plt
import fonctions as fc

c= fc.celerite


def sphVersCart(X):
    r, theta, phi = X
    rsin_theta = r * np.sin(theta)
    x = rsin_theta * np.cos(phi)
    y = rsin_theta * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


def rad(angle):
    return (angle/360)*2*np.pi


def troisDTo2D(matrice3D: np.array): #rentrer matrice 3D uniquement
    (a, b, d) = matrice3D.shape
    Matrice2D = matrice3D.reshape(a*b, d)
    return(Matrice2D)


def testRedondance(matrice: np.array):
    eleUniques, compte = np.unique(matrice, return_counts=True, axis=0)
    eleRedondants = eleUniques[compte > 1]
    nbRedondance = compte[compte > 1]
    return eleRedondants, nbRedondance


def simulationPhases(pas: float, r: float, freq: int) -> np.array:
    """Simule les 5 differences de phases pour une source localisée en de multiples points (variation de pas
    degrés pour theta et phi, à une distance r donnée)."""
    lambd = freq/c
    antennes = np.array([
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 0            ],
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 2 * np.pi / 3],
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 4 * np.pi / 3],
        [lambd / (5*np.sqrt(3)), 0            , 0            ],
        [lambd / (5*np.sqrt(3)), 2 * np.pi / 3, 0            ],
        [lambd / (5*np.sqrt(3)), 2 * np.pi / 3, np.pi        ]])
    antennesCart = np.array([sphVersCart(antennes[i]) for i in range(6)])
    
    nIterTheta = math.ceil(180 / pas)
    nIterPhi = math.ceil(360 / pas)
    phases = np.zeros((nIterTheta, nIterPhi, 6))
    
    theta =0
    for t in range(nIterTheta):
        phi=0
        for p in range(nIterPhi):
            source = np.array([r, rad(theta), rad(phi)])
            sourceCart = sphVersCart(source)
            distances = np.linalg.norm(antennesCart - sourceCart, axis=1)
            phases[t, p] = ((distances * np.pi * 2) / lambd)
            phi += pas
        theta += pas
        
    DPhases = np.zeros((nIterTheta, nIterPhi, 5))
    for i in range(5):
        DPhases[:, :, i] = (phases[:, :, i+1] - phases[:, :, 0]) % np.pi
    return np.around(DPhases, decimals=10)

def Abaque(pas: float,r: float, freq: int):

    DPhases = simulationPhases(pas, r, freq)
    fichier = open("AbaquePhase.txt", "w")
    for theta in range(0,180,pas):
        for phi in range(0,360,pas):
            fichier.write(str(DPhases[theta//pas][phi//pas][0]) + "," + str(DPhases[theta//pas][phi//pas][1]) + "," + str(DPhases[theta//pas][phi//pas][2]) + "," + str(DPhases[theta//pas][phi//pas][3]) + "," + str(DPhases[theta//pas][phi//pas][4]) +","+ str(theta) + "," + str(phi) + "\n")
    fichier.close()

def PhasesAleatoire(nombre: int, r: float, freq: int) -> np.array:

    Thetas = [np.random.uniform(0,180) for i in range(int(np.sqrt(nombre)))]
    Phis = [np.random.uniform(0,360) for i in range(int(np.sqrt(nombre)))]
    lambd = freq/c
    antennes = np.array([
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 0            ],
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 2 * np.pi / 3],
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 4 * np.pi / 3],
        [lambd / (5*np.sqrt(3)), 0            , 0            ],
        [lambd / (5*np.sqrt(3)), 2 * np.pi / 3, 0            ],
        [lambd / (5*np.sqrt(3)), 2 * np.pi / 3, np.pi        ]])
    antennesCart = np.array([sphVersCart(antennes[i]) for i in range(6)])
    fichier = open("ValeursTestPhase.txt", "w")
    for theta in Thetas:
        for phi in Phis:
            phases = np.zeros(5)
            source = np.array([r, rad(theta), rad(phi)])
            sourceCart = sphVersCart(source)
            distances = np.linalg.norm(antennesCart - sourceCart, axis=1)
            phases = ((distances * np.pi * 2) / lambd) % (2 * np.pi)
            DPhases = np.zeros(5)
            for i in range(5):
                DPhases[i] = phases[i+1] - phases[0]
            fichier.write(str(DPhases[0]) + "," + str(DPhases[1]) + "," + str(DPhases[2]) + "," + str(DPhases[3]) + "," + str(DPhases[4]) + "," + str(theta) + "," + str(phi) + "\n")
    fichier.close()
