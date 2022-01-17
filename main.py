import get_weather
import time

def minute_sleep(n):
    time.sleep(n*60)

while True:
    get_weather.get_weather()
    minute_sleep(10)