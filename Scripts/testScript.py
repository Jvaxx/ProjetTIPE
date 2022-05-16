import time
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

"""
ADS 1 (72, adr->gnd)
    voie0: ok --> 1*2
    voie1: ok --> 1*3

ADS 2 (73, adr->vdd)
    voie2: ok --> crete 1
    voie3: ok --> crete 2

ADS 3 (74, adr->sda)
    voie4: ok --> crete 3
    voie5: ok
"""

MULTIPLIEUR_POSTMULT = 10
CAN_OFFSET = 0
LONGUEUR_ONDE = 1


i2c = busio.I2C(board.SCL, board.SDA)
ads1 = ADS.ADS1115(i2c, address=72)
ads2 = ADS.ADS1115(i2c, address=73)
ads3 = ADS.ADS1115(i2c, address=74)

chans = [
    AnalogIn(ads1, ADS.P0, ADS.P1), # 1*2
    AnalogIn(ads1, ADS.P2, ADS.P3), # 1*3
    AnalogIn(ads2, ADS.P0, ADS.P1), # cr 1
    AnalogIn(ads2, ADS.P2, ADS.P3), # cr2
    AnalogIn(ads3, ADS.P0, ADS.P1), # cr3
    AnalogIn(ads3, ADS.P2, ADS.P3)
]

def testAds(nVoie):
    print(chans[nVoie].voltage)

def donneAngles():
    dephasage1 = np.arccos((2*(chans[0].voltage + CAN_OFFSET)) /
                           ((chans[2].voltage + CAN_OFFSET) * (chans[3].voltage + CAN_OFFSET)))

    dephasage2 = np.arccos((2*(chans[1].voltage + CAN_OFFSET)) /
                           ((chans[2].voltage + CAN_OFFSET) * (chans[4].voltage + CAN_OFFSET)))

    theta1 = np.arcsin((-dephasage1 * LONGUEUR_ONDE) / np.pi)
    theta2 = np.arcsin((-dephasage2 * LONGUEUR_ONDE) / np.pi)

    return [theta1 + np.pi/3, -theta1 + np.pi/3, theta2 - np.pi/3, -theta2 - np.pi/3]


def trouveDroite():

    angles = donneAngles()
    distances = [angles[2] - angles[0], angles[3] - angles[1]]
    min_value = min(distances)
    min_index = distances.index(min_value)

    if min_index == 0:
        return (angles[2] + angles[0])/2

    if min_index == 1:
        return (angles[3] + angles[1])/2

while True:
    nVoie = int(input('Nvoie a tester: '))
    testAds(nVoie)