from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations

def dessinerSphere(rayon)
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect("equal")