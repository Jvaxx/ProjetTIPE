#executer en tant que script ( ctrl + shit + E sur pyzo)
import os
from tkinter import N
from turtle import color
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
import math
import matplotlib.pyplot as plt
import fonctions as fc
import time

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
        [lambd / (2*np.sqrt(3)), np.pi / 2    , 0            ],
        [lambd / (2*np.sqrt(3)), np.pi / 2    , 2 * np.pi / 3],
        [lambd / (2*np.sqrt(3)), np.pi / 2    , 4 * np.pi / 3],
        [lambd / (2*np.sqrt(3)), 0            , 0            ],
        [lambd / (2*np.sqrt(3)), 2 * np.pi / 3, 0            ],
        [lambd / (2*np.sqrt(3)), 2 * np.pi / 3, np.pi        ]])
    antennesCart = np.array([sphVersCart(antennes[i]) for i in range(6)])
    
    nIterTheta = math.ceil(180 / pas)
    nIterPhi = math.ceil(360 / pas)
    phases = np.zeros((nIterTheta, nIterPhi, 6))
    
    theta =0
    for t in range(nIterTheta):
        phi=0
        for p in range(nIterPhi):
            sourceCart = sphVersCart(np.array([r, rad(theta), rad(phi)]))
            phases[t, p] = (np.linalg.norm(antennesCart - sourceCart, axis=1) % lambd) * (2 * np.pi / lambd)
            phi += pas
        theta += pas
    
    DPhases = np.zeros((nIterTheta, nIterPhi, 5))
    for i in range(5):
        DPhases[:, :, i] = (phases[:, :, i+1] - phases[:, :, 0]) % np.pi
    return np.around(DPhases, decimals=1)


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



def listeAbaque(pasGene, pasSecond, r, freq):
    lambd = freq/c
    antennes = np.array([
        [lambd / (2*np.sqrt(3)), np.pi / 2    , 0            ],
        [lambd / (2*np.sqrt(3)), np.pi / 2    , 2 * np.pi / 3],
        [lambd / (2*np.sqrt(3)), np.pi / 2    , 4 * np.pi / 3],
        [lambd / (2*np.sqrt(3)), 0            , 0            ],
        [lambd / (2*np.sqrt(3)), 2 * np.pi / 3, 0            ],
        [lambd / (2*np.sqrt(3)), 2 * np.pi / 3, np.pi        ]])
    antennesCart = np.array([sphVersCart(antennes[i]) for i in range(6)])
    nIterTheta = math.ceil(np.pi/pasGene)
    nIterPhi = math.ceil(2*np.pi/pasGene)
    nIterSousValeur = math.ceil(pasGene/pasSecond)
    
    phases = np.empty((nIterTheta, nIterPhi, nIterSousValeur, nIterSousValeur, 6))

    #pour 3D
    pointsTestes = np.empty((nIterTheta*nIterPhi*(nIterSousValeur**2), 2))

    i = 0
    theta = 0
    for t in range(nIterTheta):
        phi = 0
        for p in range(nIterPhi):
            deltaTheta = 0
            for sousIterTheta in range(nIterSousValeur):
                deltaPhi = 0
                for sousIterPhi in range(nIterSousValeur):

                    #pour 3D
                    pointsTestes[i] = [theta+deltaTheta, phi+deltaPhi]
                    i+=1

                    sourceCart = sphVersCart(np.array([r, theta+deltaTheta, phi+deltaPhi]))
                    phases[t, p, sousIterTheta, sousIterPhi] = (np.linalg.norm(antennesCart - sourceCart, axis=1) % lambd) * (2 * np.pi / lambd)
                    deltaPhi += pasSecond
                deltaTheta += pasSecond
            phi += pasGene
        theta += pasGene

    
    dephasages = np.empty((nIterTheta, nIterPhi, nIterSousValeur, nIterSousValeur, 5))
    for i in range(5):
        dephasages[:, :, :, :, i] = (phases[:, :, :, :, i+1] - phases[:, :, :, :, 0]) % np.pi
    
    pointsProches = np.empty((nIterTheta*nIterPhi*(nIterSousValeur**2), 2))
    i = 0
    theta = 0
    for t in range(nIterTheta):
        phi = 0
        for p in range(nIterPhi):
            for k in range(nIterSousValeur**2):
                pointsProches[i] = [theta, phi]
                i += 1
            phi += pasGene
        theta += pasGene

    return np.reshape(dephasages, (nIterTheta*nIterPhi*(nIterSousValeur**2), 5)), pointsProches, pointsTestes



# KNN jvz
def trouverLesKnn(xAbaque, xInconnue, k):
    distances = -2 * xAbaque@xInconnue.T + np.sum(xInconnue**2, axis=1) + np.sum(xAbaque**2, axis=1)[:, np.newaxis]
    distances[distances < 0] = 0

    indices = np.argsort(distances, 0)
    distances = np.sort(distances, 0)

    return indices[:k, :], distances[:k, :]

def knn_predictions(xTrain,yTrain,xTest,k=3):
    indices, distances = trouverLesKnn(xTrain,xTest,k)
    a, b = yTrain.shape
    yTrain = np.reshape(yTrain, (a, 2))
    rows, columns = indices.shape
    predictions = list()
    for j in range(columns):
        temp = list()
        for i in range(rows):
            cell = indices[i][j]
            temp.append(yTrain[cell].tolist())
        predictions.append(max(temp,key=temp.count))
    predictions=np.array(predictions)
    return predictions



def afficherCouleur(xAbaque, xInconnue, ptTest):
    """
    Affichage des distances en couleurs pour un tuple de phases
    """
    distances = -2 * xAbaque@xInconnue.T + np.sum(xInconnue**2, axis=1) + np.sum(xAbaque**2, axis=1)[:, np.newaxis]
    distances[distances < 2] = -10

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    u, v = ptTest[:, 1], ptTest[:, 0]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    sphere = ax.scatter(x, y, z, c=distances, cmap=cm.coolwarm)
    fig.colorbar(sphere, shrink=0.5, aspect=5)
    ax.scatter(0.7, 0.7, 0.7, color='red', marker='X')

    ax.set_xlim3d(-1, 1)
    ax.set_xlabel('X')
    ax.set_ylim3d(-1, 1)
    ax.set_ylabel('Y')
    ax.set_zlim3d(-1, 1)
    ax.set_zlabel('Z')
    ax.legend()


    plt.show()


"""affiche les distances knn sur sphere"""
deph, ptProche, ptTest = listeAbaque(0.20,0.020,1000,300)
test = np.array([[0.58, 2.16, 2.76, 0.75, 2.34]])
pred = knn_predictions(deph, ptProche, test)
print(pred)
afficherCouleur(deph, test, ptTest)

