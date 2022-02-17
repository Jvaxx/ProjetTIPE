from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations


freq = 300 #hz
c = 340 #m/s
pas = 10 #degres
r = 1


def sphVersCart(X):
    r, theta, phi = X
    rsin_theta = r * np.sin(theta)
    x = rsin_theta * np.cos(phi)
    y = rsin_theta * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


def rad(angle):
    return (angle/360)*2*np.pi


lambd = freq/c
antennes = np.array([
    [lambd / (8 * np.cos(np.pi / 3)), np.pi / 2    , 0            ],
    [lambd / (8 * np.cos(np.pi / 3)), np.pi / 2    , 2 * np.pi / 3],
    [lambd / (8 * np.cos(np.pi / 3)), np.pi / 2    , 4 * np.pi / 3],
    [lambd / (8 * np.cos(np.pi / 3)), 0            , 0            ],
    [lambd / (8 * np.cos(np.pi / 3)), 2 * np.pi / 3, 0            ],
    [lambd / (8 * np.cos(np.pi / 3)), 2 * np.pi / 3, np.pi        ]])
antennesCart = np.array([sphVersCart(antennes[i]) for i in range(6)])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(antennesCart[:, 0], antennesCart[:, 1], antennesCart[:, 2], c='red')

nIterTheta = int(360 // pas)
nIterPhi = int(180 // pas)

sources = np.zeros((nIterTheta*nIterPhi, 3))
theta, phi = 0., 0.
q = 0
for t in range(nIterTheta):
    for p in range(nIterPhi):
        sources[q] = np.array([r, rad(theta), rad(phi)])
        phi += pas
        q += 1
    theta += pas

ax.scatter(sources[q] +)

plt.show()