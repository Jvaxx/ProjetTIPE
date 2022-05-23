import numpy as np


MULTIPLIEUR_POSTMULT = 10
CAN_OFFSET = 0
LONGUEUR_ONDE = 1


def donneAngles(chans):
    dephasage1 = np.arccos((2*(chans[0].voltage + CAN_OFFSET)) /
        ((chans[2].voltage + CAN_OFFSET) * (chans[3].voltage + CAN_OFFSET)))
    dephasage2 = np.arccos((2*(chans[1].voltage + CAN_OFFSET)) /
        ((chans[2].voltage + CAN_OFFSET) * (chans[4].voltage + CAN_OFFSET)))
    
    theta1 = np.arcsin((-dephasage1 * LONGUEUR_ONDE) / np.pi)
    theta2 = np.arcsin((-dephasage2 * LONGUEUR_ONDE) / np.pi)

    return [theta1 + np.pi/3, -theta1 + np.pi/3, theta2 - np.pi/3, -theta2 - np.pi/3]


def trouverLaDirection(directions):
    marges = [
        abs(directions[2] - directions[0]),
        abs(directions[3] - directions[0]),
        abs(directions[2] - directions[1]),
        abs(directions[3] - directions[1]),
    ]
    minIndex = marges.index(min(marges))
    if minIndex == 0: return (directions[2]+directions[0])/2
    if minIndex == 1: return (directions[3]+directions[0])/2
    if minIndex == 2: return (directions[2]+directions[1])/2
    if minIndex == 3: return (directions[3]+directions[1])/2