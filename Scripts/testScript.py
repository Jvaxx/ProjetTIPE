import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=74)
"""
ADS 3 (73)  channel 0 ok, mal soudé
            channel 1 ok
            channel 2 ?
            channel 3 ok

ADS 2 (74)  channel 0 ok
            channel 1 ok
            channel 2 ?
            channel 3 ok

ADS 1 (  )  SDA mal soudé
"""
chan = AnalogIn(ads, ADS.P0, ADS.P1)
while True:
    print(chan.value, chan.voltage)
    time.sleep(0.3)
print('voila')
