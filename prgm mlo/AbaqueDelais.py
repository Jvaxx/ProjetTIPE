#executer en tant que script ( ctrl + shit + E sur pyzo)
import os
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

import numpy as np
import math
import matplotlib.pyplot as plt

c= 340.


def sphVersCart(X):
    r, theta, phi = X
    rsin_theta = r * np.sin(theta)
    x = rsin_theta * np.cos(phi)
    y = rsin_theta * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


def rad(angle):
    return (angle/360)*2*np.pi


def testRedondance(matrice: np.array):
    eleUniques, compte = np.unique(matrice, return_counts=True, axis=0)
    eleRedondants = eleUniques[compte > 1]
    nbRedondance = compte[compte > 1]
    return eleRedondants, nbRedondance


def simulationDelais(pas: float, r: float, freq: int) -> np.array:
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
    delais = np.zeros((nIterTheta, nIterPhi, 6))
    
    theta =0
    for t in range(nIterTheta):
        phi=0
        for p in range(nIterPhi):
            source = np.array([r, rad(theta), rad(phi)])
            sourceCart = sphVersCart(source)
            distances = np.linalg.norm(antennesCart - sourceCart, axis=1)
            delais[t, p] = distances / c
            phi += pas
        theta += pas
        
    DiffDelais = np.zeros((nIterTheta, nIterPhi, 5))
    for i in range(5):
        DiffDelais[:, :, i] = abs(delais[:, :, i+1] - delais[:, :, 0])
    return np.around(DiffDelais, decimals=10)

def Abaque(pas: float,r: float, freq: int):

    DiffDelais = simulationDelais(pas, r, freq)
    fichier = open("AbaqueDelais.txt", "w")
    for theta in range(0,180,pas):
        for phi in range(0,360,pas):
            fichier.write(str(DiffDelais[theta//pas][phi//pas][0]) + "," + str(DiffDelais[theta//pas][phi//pas][1]) + "," + str(DiffDelais[theta//pas][phi//pas][2]) + "," + str(DiffDelais[theta//pas][phi//pas][3]) + "," + str(DiffDelais[theta//pas][phi//pas][4]) +","+ str(theta) + "," + str(phi) + "\n")
    fichier.close()

def DelaisAleatoire(nombre: int, r: float, freq: int) -> np.array:

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
    fichier = open("ValeursTestDelais.txt", "w")
    for theta in Thetas:
        for phi in Phis:
            delais = np.zeros(5)
            source = np.array([r, rad(theta), rad(phi)])
            sourceCart = sphVersCart(source)
            distances = np.linalg.norm(antennesCart - sourceCart, axis=1)
            delais = distances /c
            DiffDelais = np.zeros(5)
            for i in range(5):
                DiffDelais[i] = abs(delais[i+1] - delais[0])
            fichier.write(str(DiffDelais[0]) + "," + str(DiffDelais[1]) + "," + str(DiffDelais[2]) + "," + str(DiffDelais[3]) + "," + str(DiffDelais[4]) + "," + str(theta) + "," + str(phi) + "\n")
    fichier.close()
