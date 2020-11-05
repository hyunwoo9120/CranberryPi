import os
import subprocess
import time
import datetime
import Adafruit_DHT as dht

onoff = "python3 irrp.py -p -g22 -fhome_aircon power"
up = "python3 irrp.py -p -g22 -fhome_aircon upTemperature"
down = "python3 irrp.py -p -g22 -fhome_aircon downTemperature"

'''
예상 시나리오
1. 에어컨 on
2. 에어컨 온도 내리기
3. 에어컨 온도 올리기
4. 에어컨 off
'''

pn = 0  # pn : person num
print(pn)

pn = 1
time.sleep(3)

if (pn == 1):
    print(pn)
    os.system(onoff)
    pn = 2
    time.sleep(7)

if (pn == 2):
    print(pn)
    os.system(down)
    time.sleep(1)
    os.system(down)
    pn = 1
    time.sleep(5)

if (pn == 1):
    print(pn)
    os.system(up)
    time.sleep(1)
    os.system(up)
    pn = 0
    time.sleep(5)

if (pn == 0):
    print(pn)
    os.system(onoff)
