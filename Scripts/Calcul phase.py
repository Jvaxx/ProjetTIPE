import numpy as np
import pickle
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads1 = ADS.ADS1115(i2c, address=72)
ads2 = ADS.ADS1115(i2c, address=73)
ads3 = ADS.ADS1115(i2c, address=74)

chan1 = AnalogIn(ads1, ADS.P0, ADS.P1)
chan2 = AnalogIn(ads1, ADS.P2, ADS.P3)
chan3 = AnalogIn(ads2, ADS.P0, ADS.P1)
chan4 = AnalogIn(ads2, ADS.P2, ADS.P3)
chan5 = AnalogIn(ads3, ADS.P0, ADS.P1)
chan6 = AnalogIn(ads3, ADS.P2, ADS.P3)

filename = 'resultats'
tours = 1000
delay = 0.1 #sec

'''
Output array des 2 sorties pbmult 
'''
with open(filename, 'w') as outfile:
    out = np.zeros((tours, 2))
    for i in range(tours):
        out[i, 1] = chan1.voltage
        out[i, 2] = chan2.voltage
        time.sleep(delay)
    pickle.dump(out, outfile)
