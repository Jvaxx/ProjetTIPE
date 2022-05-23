#executer en tant que script ( ctrl + shit + E sur pyzo)
import os
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

from math import *
import matplotlib.pyplot as plt
import numpy as np

c = 340

def sphVersCart(X):
    r, theta, phi = X
    rsin_theta = r * np.sin(theta)
    x = rsin_theta * np.cos(phi)
    y = rsin_theta * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


def rad(angle):
    return (angle/360)*2*np.pi
    
def GenerateurSignaux(EcartTypeBruit, frequence, DureeSignal, FrequenceEchantillonage, PositionSource): #PositionSource = 'r, theta, phi) en degré
    lambd = frequence/c
    antennes = np.array([
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 0            ],
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 2 * np.pi / 3],
        [lambd / (5*np.sqrt(3)), np.pi / 2    , 4 * np.pi / 3],
        [lambd / (5*np.sqrt(3)), 0            , 0            ],
        [lambd / (5*np.sqrt(3)), 2 * np.pi / 3, 0            ],
        [lambd / (5*np.sqrt(3)), 2 * np.pi / 3, np.pi        ]])
    antennesCart = np.array([sphVersCart(antennes[i]) for i in range(6)])
    sourceCart = sphVersCart((PositionSource[0], rad(PositionSource[1]), rad(PositionSource[2])))
    distances = np.linalg.norm(antennesCart - sourceCart, axis=1)
    delais = np.zeros(6)
    delais = distances / c
    Signaux = [[np.random.normal(0, EcartTypeBruit) + sin(2*pi*frequence*(k/FrequenceEchantillonage-delais[i])) for k in range(0,int(DureeSignal*FrequenceEchantillonage),1)] for i in range(6)]
    print([delais[i]-delais[0] for i in range(1,6)]) #a supr
    
    X = [k/FrequenceEchantillonage for k in range(0,int(DureeSignal*FrequenceEchantillonage),1)]
    plt.figure()
    for i in range(6):
        plt.plot(X, Signaux[i], 'b')
    plt.show()
    
    return Signaux
    