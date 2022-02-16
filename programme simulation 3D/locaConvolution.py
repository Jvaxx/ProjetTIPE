from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import numpy as np

c = 340
To = np.array([0, 0, 0])
Antennes = np.array([[1, 0, 0], [0, 1, 0], [2, 1, 0]])

def fonction(M):
    e1 = np.sqrt((M[0] - Antennes[0][0]) ** 2 + (M[1] - Antennes[0][1]) ** 2 + (M[2] - Antennes[0][2]) ** 2) - np.sqrt(
        (M[0] - Antennes[1][0]) ** 2 + (M[1] - Antennes[1][1]) ** 2 + (M[2] - Antennes[1][2]) ** 2) - c*To[0]

    e2 = np.sqrt((M[0] - Antennes[1][0]) ** 2 + (M[1] - Antennes[1][1]) ** 2 + (M[2] - Antennes[1][2]) ** 2) - np.sqrt(
        (M[0] - Antennes[2][0]) ** 2 + (M[1] - Antennes[2][1]) ** 2 + (M[2] - Antennes[2][2]) ** 2) - c * To[1]

    e3 = np.sqrt((M[0] - Antennes[2][0]) ** 2 + (M[1] - Antennes[2][1]) ** 2 + (M[2] - Antennes[2][2]) ** 2) - np.sqrt(
        (M[0] - Antennes[0][0]) ** 2 + (M[1] - Antennes[0][1]) ** 2 + (M[2] - Antennes[0][2]) ** 2) - c * To[2]

    return np.array([e1, e2, e3])

root = fsolve(fonction, np.array([0, 0, 0]))
print(root)