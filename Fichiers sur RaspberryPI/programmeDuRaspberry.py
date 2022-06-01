import time
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

"""
Branchement des CAN: (entre parenthèses l'adresse I2C de chaque CAN et le branchement correspondant)

    ADS 1 (72, adr->gnd)
        voie0 --> passeBas multiplieur 1*2
        voie1 --> passeBas multiplieur 1*3

    ADS 2 (73, adr->vdd)
        voie2 --> crete 1
        voie3 --> crete 2

    ADS 3 (74, adr->sda)
        voie4 --> crete 3
        voie5 --> Non assigné
"""

# Paramètres d'aquisition
CAN_OFFSET = 0.53
LONGUEUR_ONDE = 1.14


# Indexation des CAN
i2c = busio.I2C(board.SCL, board.SDA)
ads1 = ADS.ADS1115(i2c, address=72)
ads2 = ADS.ADS1115(i2c, address=73)
ads3 = ADS.ADS1115(i2c, address=74)

cannaux = [
    AnalogIn(ads1, ADS.P0, ADS.P1), # 1*2
    AnalogIn(ads1, ADS.P2, ADS.P3), # 1*3
    AnalogIn(ads2, ADS.P0, ADS.P1), # cr1
    AnalogIn(ads2, ADS.P2, ADS.P3), # cr2
    AnalogIn(ads3, ADS.P0, ADS.P1), # cr3
    AnalogIn(ads3, ADS.P2, ADS.P3)
]


def testAds(nVoie):
    """
    S'assure du bon fonctionnement d'un canal
    """
    print(cannaux[nVoie].voltage)


def donneAngles():
    """
    Renvoie les 4 directions possbiles (dont 2 se répètent)
    """
    dephasage1 = np.arccos((2*(cannaux[0].voltage + CAN_OFFSET)) /
                           ((cannaux[2].voltage + CAN_OFFSET) * (cannaux[3].voltage + CAN_OFFSET)))

    dephasage2 = np.arccos((2*(cannaux[1].voltage + CAN_OFFSET)) /
                           ((cannaux[2].voltage + CAN_OFFSET) * (cannaux[4].voltage + CAN_OFFSET)))

    theta1 = np.arcsin((-dephasage1 * LONGUEUR_ONDE) / np.pi)
    theta2 = np.arcsin((-dephasage2 * LONGUEUR_ONDE) / np.pi)

    return [theta1 + np.pi/3, -theta1 + np.pi/3, theta2 - np.pi/3, -theta2 - np.pi/3]


def trouveDroite():
    """
    Renvoie la direction se répétant parmis les 4 trouvées
    """
    angles = donneAngles()
    distances = [angles[2] - angles[0], angles[3] - angles[1]]
    min_value = min(distances)
    min_index = distances.index(min_value)

    if min_index == 0:
        return (angles[2] + angles[0])/2

    if min_index == 1:
        return (angles[3] + angles[1])/2


# Point d'entrée du script
while True:
    Input = input('Appuyer sur ENTRER pour trouver la direction')
    print(trouveDroite())