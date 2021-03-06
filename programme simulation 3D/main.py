import numpy as np
import matplotlib.pyplot as plt
c= 3*10**8.


def plotHi():
    nZ = 10
    nTheta = 10
    theta = np.linspace(0, 2*np.pi, nTheta)
    points = np.zeros((nZ*nTheta, 3))
    z = np.linspace(-1, 1, nZ)
    for i in range(nZ):
        points[nTheta * i:nTheta*(i+1), 2] = z[i]
        points[nTheta * i:nTheta*(i+1), 0] = np.cos(np.pi*z[i]/2)*np.cos(theta)
        points[nTheta * i:nTheta * (i + 1), 1] = np.cos(np.pi*z[i]/2) * np.sin(theta)
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.scatter(points[:, 0], points[:, 1], points[:, 2])
    plt.show()


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
        [lambd / (8 * np.cos(np.pi / 3)), np.pi / 2    , 0            ],
        [lambd / (8 * np.cos(np.pi / 3)), np.pi / 2    , 2 * np.pi / 3],
        [lambd / (8 * np.cos(np.pi / 3)), np.pi / 2    , 4 * np.pi / 3],
        [lambd / (8 * np.cos(np.pi / 3)), 0            , 0            ],
        [lambd / (8 * np.cos(np.pi / 3)), 2 * np.pi / 3, 0            ],
        [lambd / (8 * np.cos(np.pi / 3)), 2 * np.pi / 3, np.pi        ]])
    antennesCart = np.array([sphVersCart(antennes[i]) for i in range(6)])
    nIterTheta = int(360 // pas)
    nIterPhi = int(180 // pas)
    phases = np.zeros((nIterTheta, nIterPhi, 6))

    theta, phi = 0., 0.
    for t in range(nIterTheta):
        for p in range(nIterPhi):
            source = np.array([r, rad(theta), rad(phi)])
            sourceCart = sphVersCart(source)
            distances = np.linalg.norm(antennesCart - sourceCart, axis=1)
            phases[t, p] = ((distances * np.pi * 2) / lambd) % (2 * np.pi)
            phi += pas
        theta += pas
    DPhases = np.zeros((nIterTheta, nIterPhi, 5))
    for i in range(5):
        DPhases[:, :, i] = phases[:, :, i+1] - phases[:, :, i]
    return np.around(DPhases, decimals=2)


"""phases = simulationPhases(15, 100, 10**8)
a, b = testRedondance(troisDTo2D(phases))
print(phases)"""

plotHi()
