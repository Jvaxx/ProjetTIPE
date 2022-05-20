import time
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

MULTIPLIEUR_POSTMULT = 10
CAN_OFFSET = 0
LONGUEUR_ONDE = 1.14

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

