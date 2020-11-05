import datetime
import Adafruit_DHT as dht

h,t = dht.read_retry(dht.DHT11,14)
print(t)