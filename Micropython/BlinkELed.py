"""
UNIVERSIDAD DE GUANAJUATO
Teresa Cortes Magallon
Hello World
22/01/26
"""

import machine
import time

pin25 = machine.Pin(25, machine.Pin.OUT)

while True:
    pin25.value(1)
    print("ON")
    time.sleep(0.5)
    
    pin25.value(0)
    print("OFF")
    time.sleep(0.5)