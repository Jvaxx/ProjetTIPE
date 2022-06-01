import math
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
import timeit
from matplotlib import cm

lambd = 300/340


def selectionPoints(points, dephasages, tolerance=0.04, dimension=2):
    return points[np.all(
        (np.abs(points[:, dimension:] - dephasages) < tolerance) |
        (np.abs(-points[:, dimension:] - dephasages) < tolerance),
    axis=1)]


def plotPoints(points, antennes):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    #points correspondants
    isodphi = ax.scatter(
        points[:, 0],
        points[:, 1],
        color='black',
        # c=np.abs(points[:, 2]),
        # cmap=cm.coolwarm,
        marker='o',
        s=1,)

    #antennes
    ax.scatter(
        antennes[:, 0],
        antennes[:, 1],
        color='red',
        marker='x',
        s=50,
        label='Antennes')
    
    ax.axis('scaled')
    # fig.colorbar(isodphi, shrink=0.5, aspect=5)
    plt.ylabel('y (m)')
    plt.xlabel('x (m)')
    plt.xlim((-5, 5))
    plt.ylim((-5, 5))
    plt.legend(bbox_to_anchor=(1, 1), loc='upper right')
    plt.title('Localisation possible de la source pour\nun déphsage entre 2 antennes de 57° (tolérence: 0.5°)')
    plt.show()



def ajoutDephasage(points, antennes):
    """Renvoie les points en ajoutant les dephasages aux coords"""
    phases = []
    for antenne in antennes:
        distance = (np.linalg.norm(points - antenne, axis=1) % lambd)
        phases.append(normaliserAngleCentre(distance * 2 * np.pi / lambd))

    phases = np.array(phases) # entre -pi et pi
    dephasages = np.abs(np.diff(phases, axis=0)) # entre 0 et 2pi
    dephasages = np.abs(np.where(dephasages <= np.pi, dephasages, dephasages - 2*np.pi)) # entre 0 et pi
    
    return np.concatenate((points, dephasages.T), axis=1)


def genererPoints(nx, xmin=-5, xmax=5, dimension=2):
    xTable = np.linspace(xmin, xmax, nx)
    if dimension == 2:
        points = np.array(np.meshgrid(xTable, xTable)).T.reshape((-1, 2))
    elif dimension == 3:
        points = np.array(np.meshgrid(xTable, xTable, xTable)).T.reshape((-1, 3))

    return points


def normaliserAngleCentre(angles):
    res = np.zeros(len(angles))
    for i, angle in enumerate(angles):
        if 0 <= angle <= np.pi: res[i] = angle
        if angle >= np.pi: res[i] = angle - 2*np.pi
    return res


def sphVersCart(X):
    r, theta, phi = X
    rsin_theta = r * np.sin(theta)
    x = rsin_theta * np.cos(phi)
    y = rsin_theta * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


antennes = np.array([
    # [0.21*np.cos(np.pi*2/3), 0.4*np.sin(np.pi*2/3),],
    [0.21, 0,],
    # [0.21*np.cos(-np.pi*2/3), 0.4*np.sin(-np.pi*2/3),],
    [-0.21, 0,],
])

# points = np.array([
#     [1,4, 32, 38],
#     [1,4, 26, 43],
# ])

ptsAvcDeph = ajoutDephasage(genererPoints(1000, dimension=2), antennes)
pointsSlec = selectionPoints(ptsAvcDeph, np.array([1,]), dimension=2, tolerance=0.01)
plotPoints(pointsSlec, antennes)
k = 'hey'
