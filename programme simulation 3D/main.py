import numpy as np
c= 3*10**8.
f = 10**8.
r=100.

pas = 1

lam = c/f
lamb = c/f
"""Antennes = np.array ( [
    [(lam / (8 * np.cos(np.pi/3))),0,np.pi/2],
    [(lam / (8 * np.cos(np.pi/3))),2*np.pi/3,np.pi/2],
    [(lam / (8 * np.cos(np.pi/3))),4*np.pi/3,np.pi/2],
    [(lam / (8 * np.cos(np.pi/3))),0,0],
    [(lam / (8 * np.cos(np.pi/3))),0,np.pi/2],
    [(lam / (8 * np.cos(np.pi/3))),np.pi,np.pi/2]
    ])"""

antennas = np.array([[lamb/8, 0, 0], [0, np.sqrt((3*lamb**2)/8), 0], [-lamb/8, 0, 0],
                    [0, 0, lamb/8], [0, -np.sqrt((3*lamb**2)/8), 0], [0, 0, -lamb/8]])

def sphVersCart(X):
    r = X[0]
    theta = X[1]
    phi = X[2]
    rsin_theta = r * np.sin(theta)
    x = rsin_theta * np.cos(phi)
    y = rsin_theta * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


def rad(angle):
    return (angle/360)*2*np.pi


def test(pas: int, r: float, lambd: int, antennes: np.array) -> np.array:
    nbIterTheta = int(360 // pas)
    nbIterPhi = int(180 // pas)
    phases = np.zeros((nbIterTheta, nbIterPhi, 6))

    for theta in range(0,360): #boucleSurTheta
        for phi in range(0,180): #boucleSurPhi
            source = sphVersCart(np.array([r, rad(theta), rad(phi)]))
            distances = np.linalg.norm(antennes - source, axis=1)
            phases[theta, phi] = (distances * np.pi * 2) / lambd % (2 * np.pi)
    return phases



Phases = test(1, 100, lamb, antennas)
print(Phases)