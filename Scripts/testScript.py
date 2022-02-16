import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=74)

chan = AnalogIn(ads, ADS.P0, ADS.P1)
while True:
    print(chan.value, chan.voltage)
    time.sleep(0.3)
print('voila')
