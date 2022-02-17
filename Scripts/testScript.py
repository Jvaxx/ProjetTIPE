"""
ADS 3 (73)  channel 0 ok, mal soudé
            channel 1 ok
            channel 2 ?
            channel 3 ok

ADS 2 (74)  channel 0 ok
            channel 1 ok
            channel 2 ?
            channel 3 ok

ADS 1 (72)  SDA mal soudé
"""

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
#ads1 = ADS.ADS1115(i2c, address=72)
ads2 = ADS.ADS1115(i2c, address=73)
ads3 = ADS.ADS1115(i2c, address=74)

#chan1 = AnalogIn(ads1, ADS.P0, ADS.P1)
#chan2 = AnalogIn(ads1, ADS.P2, ADS.P3)
chan3 = AnalogIn(ads2, ADS.P0, ADS.P1)
chan4 = AnalogIn(ads2, ADS.P2, ADS.P3)
chan5 = AnalogIn(ads3, ADS.P0, ADS.P1)
chan6 = AnalogIn(ads3, ADS.P2, ADS.P3)
while True:
    print('Ch: (', chan3.value, ', ', chan3.voltage, ')')
    time.sleep(0.4)

