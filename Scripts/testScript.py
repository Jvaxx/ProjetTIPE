"""
ADS 1 (72, adr->gnd)

ADS 2 (73, adr->vdd)

ADS 3 (74, adr->sda)
"""

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads1 = ADS.ADS1115(i2c, address=72)
ads2 = ADS.ADS1115(i2c, address=73)
ads3 = ADS.ADS1115(i2c, address=74)

chans = [
    AnalogIn(ads1, ADS.P0, ADS.P1),
    AnalogIn(ads1, ADS.P2, ADS.P3),
    AnalogIn(ads2, ADS.P0, ADS.P1),
    AnalogIn(ads2, ADS.P2, ADS.P3),
    AnalogIn(ads3, ADS.P0, ADS.P1),
    AnalogIn(ads3, ADS.P2, ADS.P3)
]

def testAds(nVoie):
    print(chans[nVoie].voltage)

while True:
    nVoie = int(input('Nvoie a tester: '))
    testAds(nVoie)